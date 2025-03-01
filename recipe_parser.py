from ingredient_database import INGREDIENT_DATABASE
import re
import nltk
from nltk.tokenize import word_tokenize
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # If the model isn't installed, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Load a small LLM for ingredient extraction
try:
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
except:
    print("Warning: Could not load transformer model. LLM fallback will not be available.")
    tokenizer = None
    model = None

class RecipeParser:
    def __init__(self, ingredient_database=INGREDIENT_DATABASE):
        self.ingredient_database = ingredient_database
        self.ingredient_names = [item["name"].lower() for item in ingredient_database]
    
    def parse_recipe_text(self, text):
        """Parse recipe text into structured ingredients data using multiple methods."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        results = []
        
        for line in lines:
            # Try multiple parsing methods
            result = self._try_regex_parsing(line)
            
            if not result or result.get("quantity") is None or result.get("unit") is None:
                # Fallback to NLP-based parsing
                result = self._try_nlp_parsing(line)
            
            results.append(result)
        
        return results
    
    def _try_regex_parsing(self, line):
        """Try to parse the ingredient line using regex patterns."""
        # Pattern 1: Standard format with quantity, unit, and name
        pattern1 = r'^([\d/\.\s]+)\s+([\w\s]+?)\s+([\w\s,]+)$'
        # Pattern 2: Format with quantity directly followed by ingredient
        pattern2 = r'^([\d/\.\s]+)\s+([\w\s,]+)$'
        
        match = re.match(pattern1, line)
        if match:
            quantity_str, unit, name = match.groups()
            quantity = self._parse_quantity(quantity_str)
            return {
                "original": line,
                "quantity": quantity,
                "unit": unit.strip().lower(),
                "name": name.strip(),
                "is_header": False
            }
        
        match = re.match(pattern2, line)
        if match:
            quantity_str, name = match.groups()
            quantity = self._parse_quantity(quantity_str)
            # For eggs, the unit is 'eggs'
            if 'egg' in name.lower() and 'white' not in name.lower() and 'yolk' not in name.lower():
                return {
                    "original": line,
                    "quantity": quantity,
                    "unit": None,
                    "name": "eggs",
                    "is_header": False
                }
            
            return {
                "original": line,
                "quantity": quantity,
                "unit": None,
                "name": name.strip(),
                "is_header": False
            }
        
        # If no patterns match, it might be a header or unstructured text
        return {
            "original": line,
            "quantity": None,
            "unit": None,
            "name": line,
            "is_header": not bool(re.search(r'\d', line))  # Assume lines without numbers are headers
        }
    
    def _try_nlp_parsing(self, line):
        """Use NLP techniques to parse the ingredient line."""
        doc = nlp(line)
        
        # Extract numbers (quantities)
        quantities = []
        for token in doc:
            if token.like_num:
                quantities.append(token.text)
        
        # Extract potential units
        common_units = ["cup", "cups", "tablespoon", "tablespoons", "tbsp", 
                       "teaspoon", "teaspoons", "tsp", "oz", "ounce", "ounces", 
                       "lb", "pound", "pounds", "g", "gram", "grams", 
                       "ml", "milliliter", "milliliters"]
        
        units = []
        for token in doc:
            if token.text.lower() in common_units:
                units.append(token.text.lower())
        
        # Try to identify ingredient name
        ingredient_name = None
        for ingredient in self.ingredient_names:
            if ingredient in line.lower():
                ingredient_name = ingredient
                break
        
        # If we couldn't find a known ingredient, use the remaining words
        if not ingredient_name:
            # Remove quantity and unit words
            remaining_words = []
            skip_tokens = set(quantities + units)
            for token in doc:
                if token.text not in skip_tokens and not token.is_punct and not token.like_num:
                    remaining_words.append(token.text)
            
            ingredient_name = " ".join(remaining_words).strip()
        
        # Parse quantity
        quantity = None
        if quantities:
            quantity_str = " ".join(quantities)
            quantity = self._parse_quantity(quantity_str)
        
        # Determine unit
        unit = None
        if units:
            unit = units[0]  # Take the first unit found
        
        return {
            "original": line,
            "quantity": quantity,
            "unit": unit,
            "name": ingredient_name,
            "is_header": not quantities and not units  # If no quantities or units, assume it's a header
        }
    
    def _parse_quantity(self, quantity_str):
        """Convert a quantity string to a float value."""
        try:
            if '/' in quantity_str:
                # Handle fractions
                parts = quantity_str.split()
                if len(parts) > 1 and '/' in parts[1]:
                    # Mixed number (e.g., "1 1/2")
                    whole = float(parts[0])
                    numerator, denominator = map(int, parts[1].split('/'))
                    return whole + (numerator / denominator)
                else:
                    # Simple fraction (e.g., "1/2")
                    for part in parts:
                        if '/' in part:
                            numerator, denominator = map(int, part.split('/'))
                            return numerator / denominator
            else:
                return float(quantity_str)
        except Exception as e:
            print(f"Error parsing quantity '{quantity_str}': {str(e)}")
            return None
    
    def convert_to_grams(self, ingredient):
        """Convert ingredient to gram weight based on its quantity and unit."""
        if ingredient.get("is_header", False) or ingredient.get("quantity") is None:
            return None
        
        quantity = ingredient["quantity"]
        unit = ingredient["unit"]
        name = ingredient["name"]
        
        # Find the ingredient in the database
        ingredient_data = None
        for item in self.ingredient_database:
            if (name.lower() in item["name"].lower() or 
                item["name"].lower() in name.lower() or
                self._similarity_score(name.lower(), item["name"].lower()) > 0.7):
                ingredient_data = item
                break
        
        if not ingredient_data:
            # Try to match with tokens
            tokens = word_tokenize(name.lower())
            for token in tokens:
                if len(token) > 3:  # Only consider tokens with meaningful length
                    for item in self.ingredient_database:
                        if token in item["name"].lower():
                            ingredient_data = item
                            break
                    if ingredient_data:
                        break
        
        if not ingredient_data:
            return None  # Unknown ingredient
        
        # If unit is already grams, return the quantity
        if unit in ['g', 'gram', 'grams']:
            return round(quantity)
        
        # Handle special case for eggs
        if unit is None and (name.lower() == "eggs" or name.lower() == "egg"):
            return round(quantity * 50)  # Assume 50g per egg
        
        # Convert based on the unit
        if unit in ['cup', 'cups']:
            return round(quantity * ingredient_data.get("gram_per_cup", 0))
        elif unit in ['tablespoon', 'tablespoons', 'tbsp']:
            return round(quantity * ingredient_data.get("gram_per_tablespoon", 0))
        elif unit in ['teaspoon', 'teaspoons', 'tsp']:
            return round(quantity * ingredient_data.get("gram_per_teaspoon", 0))
        elif unit in ['oz', 'ounce', 'ounces']:
            return round(quantity * 28.35)  # 1 oz = 28.35g
        elif unit in ['lb', 'pound', 'pounds']:
            return round(quantity * 453.59)  # 1 lb = 453.59g
        elif unit in ['ml', 'milliliter', 'milliliters']:
            if ingredient_data["type"] == "liquid":
                return round(quantity)  # 1ml of water = 1g
            else:
                return round(quantity * ingredient_data.get("density", 1))
        else:
            return None  # Unknown unit
    
    def _similarity_score(self, text1, text2):
        """Calculate a simple similarity score between two strings."""
        # Simple Jaccard similarity
        set1 = set(text1.split())
        set2 = set(text2.split())
        
        if not set1 or not set2:
            return 0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union

# Update the PrecisionBakingApp class to use this new parser
def update_app_with_new_parser(app_class):
    """
    Update the PrecisionBakingApp class to use the new RecipeParser.
    This function demonstrates how to integrate the new parser.
    """
    parser = RecipeParser()
    
    # Replace the parse_recipe_text method
    app_class.parse_recipe_text = parser.parse_recipe_text
    
    # Replace the convert_to_grams method
    app_class.convert_to_grams = parser.convert_to_grams
    
    return app_class

# Example usage
if __name__ == "__main__":
    parser = RecipeParser()
    
    # Test with a simple recipe
    test_recipe = """2 cups all-purpose flour
1 cup white sugar
1 teaspoon baking powder
1/2 teaspoon salt
1 cup milk
1/4 cup butter, melted
2 eggs"""
    
    results = parser.parse_recipe_text(test_recipe)
    
    for item in results:
        item["gram_weight"] = parser.convert_to_grams(item)
        print(f"{item['name']}: {item['quantity']} {item['unit']} → {item['gram_weight']}g")
    
    total_weight = sum(item.get("gram_weight") or 0 for item in results)
    print(f"Total weight: {total_weight}g")