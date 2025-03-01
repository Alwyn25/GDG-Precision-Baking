# main.py
import re
import csv
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import webbrowser
from ingredient_database import INGREDIENT_DATABASE
from recipe_parser import RecipeParser, update_app_with_new_parser

class PrecisionBakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Precision Baking Converter")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(self.root, padding="20 20 20 0")
        header_frame.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(header_frame, text="Precision Baking", 
                 font=("Helvetica", 24, "bold")).pack()
        ttk.Label(header_frame, text="Convert recipe measurements to precise gram weights", 
                 font=("Helvetica", 12)).pack(pady=(5, 0))
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Enter Your Recipe", padding="20")
        input_frame.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)
        
        ttk.Label(input_frame, text="Paste your recipe with ingredient measurements below", 
                 wraplength=300).pack(anchor=tk.W, pady=(0, 10))
        
        self.recipe_input = scrolledtext.ScrolledText(input_frame, width=40, height=20)
        self.recipe_input.pack(fill=tk.BOTH, expand=True)
        self.recipe_input.insert(tk.END, """2 cups all-purpose flour
1/2 cup white sugar
1 teaspoon baking powder
1/2 teaspoon salt
1 cup milk
1/4 cup butter, melted
2 eggs""")
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=(10, 0), fill=tk.X)
        
        self.convert_button = ttk.Button(button_frame, text="Convert to Grams", 
                                       command=self.convert_recipe)
        self.convert_button.pack(side=tk.RIGHT)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", 
                                     command=lambda: self.recipe_input.delete(1.0, tk.END))
        self.clear_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Output frame
        self.output_frame = ttk.LabelFrame(self.root, text="Converted Recipe", padding="20")
        self.output_frame.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)
        
        # Initially hide the treeview and setup later when we have data
        self.setup_empty_output()
        
        # Footer
        footer_frame = ttk.Frame(self.root, padding="20 0 20 20")
        footer_frame.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(footer_frame, text="Precision Baking - AI-Powered Baking Measurement Tool",
                 font=("Helvetica", 10)).pack(side=tk.LEFT)
                 
        help_button = ttk.Button(footer_frame, text="Help", command=self.show_help)
        help_button.pack(side=tk.RIGHT)
    
    def setup_empty_output(self):
        # Clear any existing widgets
        for widget in self.output_frame.winfo_children():
            widget.destroy()
            
        # Add placeholder text
        empty_label = ttk.Label(self.output_frame, 
                              text="Enter a recipe and click 'Convert to Grams' to see results here.",
                              wraplength=300)
        empty_label.pack(expand=True)
    
    def setup_results_output(self, results):
        # Clear any existing widgets
        for widget in self.output_frame.winfo_children():
            widget.destroy()
            
        # Action buttons
        btn_frame = ttk.Frame(self.output_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        save_btn = ttk.Button(btn_frame, text="Save as CSV", 
                            command=lambda: self.save_as_csv(results))
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create treeview for results
        columns = ("ingredient", "original", "grams")
        tree = ttk.Treeview(self.output_frame, columns=columns, show="headings", selectmode="none")
        
        # Define column headings
        tree.heading("ingredient", text="Ingredient")
        tree.heading("original", text="Original Measurement")
        tree.heading("grams", text="Weight (g)")
        
        # Define column widths
        tree.column("ingredient", width=150)
        tree.column("original", width=150)
        tree.column("grams", width=100)
        
        # Add data to the treeview
        total_weight = 0
        for item in results:
            if item.get("is_header", False):
                tree.insert("", tk.END, values=(item["original"], "", ""), tags=("header",))
            else:
                gram_weight = item.get("gram_weight", None)
                gram_str = f"{gram_weight}g" if gram_weight is not None else "N/A"
                tree.insert("", tk.END, values=(item["name"], item["original"], gram_str))
                total_weight += gram_weight if gram_weight is not None else 0
        
        # Add total row
        tree.insert("", tk.END, values=("", "", ""))
        tree.insert("", tk.END, values=("TOTAL WEIGHT", "", f"{total_weight}g"), tags=("total",))
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.map("Treeview", background=[("selected", "#f0f0f0")])
        
        # Configure tag styles
        tree.tag_configure("header", background="#f0f0f0", font=("Helvetica", 10, "bold"))
        tree.tag_configure("total", background="#e6e6e6", font=("Helvetica", 10, "bold"))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Notes section
        notes_frame = ttk.LabelFrame(self.output_frame, text="Precision Baking Notes")
        notes_frame.pack(fill=tk.X, pady=(10, 0))
        
        notes_text = """• For best results, use a digital scale with 1g precision.
• Room temperature for ingredients is assumed to be 21°C (70°F).
• Weight conversions are approximate and based on standard densities."""
        
        ttk.Label(notes_frame, text=notes_text, justify=tk.LEFT, wraplength=400).pack(
            anchor=tk.W, padx=10, pady=10)
    
    def convert_recipe(self):
        # Get recipe text
        recipe_text = self.recipe_input.get(1.0, tk.END).strip()
        
        if not recipe_text:
            messagebox.showwarning("Empty Recipe", "Please enter a recipe to convert.")
            return
        
        try:
            # Parse the recipe
            ingredients = self.parse_recipe_text(recipe_text)
            
            # Convert each ingredient to grams
            for item in ingredients:
                if not item.get("is_header", False) and item.get("quantity") is not None:
                    item["gram_weight"] = self.convert_to_grams(item)
            
            # Show results
            self.setup_results_output(ingredients)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while converting: {str(e)}")
    
    def parse_recipe_text(self, text):
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        results = []
        
        for line in lines:
            # Regular expression to match quantity, unit, and ingredient
            regex = r'^(?:(\d+(?:\.\d+)?(?:\s+\d+\/\d+)?|\d+\/\d+)\s+)?([a-zA-Z]+(?:\s+[a-zA-Z]+)?)?\s+(?:of\s+)?(.+)$'
            match = re.match(regex, line)
            
            if not match:
                results.append({
                    "original": line,
                    "quantity": None,
                    "unit": None,
                    "name": line,
                    "is_header": not bool(re.search(r'\d', line))  # Assume lines without numbers are headers
                })
                continue
            
            quantity, unit, name = match.groups()
            
            # Convert quantity to float
            if quantity:
                if '/' in quantity:
                    # Handle fractions
                    parts = quantity.split()
                    if len(parts) == 2:
                        # Mixed number (e.g., "1 1/2")
                        whole = float(parts[0])
                        numerator, denominator = map(int, parts[1].split('/'))
                        quantity = whole + (numerator / denominator)
                    else:
                        # Simple fraction (e.g., "1/2")
                        numerator, denominator = map(int, quantity.split('/'))
                        quantity = numerator / denominator
                else:
                    quantity = float(quantity)
            
            results.append({
                "original": line,
                "quantity": quantity,
                "unit": unit.lower() if unit else None,
                "name": name.strip(),
                "is_header": False
            })
        
        return results
    
    def convert_to_grams(self, ingredient):
        if ingredient.get("is_header", False) or ingredient.get("quantity") is None:
            return None
        
        quantity = ingredient["quantity"]
        unit = ingredient["unit"]
        name = ingredient["name"]
        
        # Find the ingredient in the database
        ingredient_data = None
        for item in INGREDIENT_DATABASE:
            if name.lower() in item["name"].lower() or item["name"].lower() in name.lower():
                ingredient_data = item
                break
        
        if not ingredient_data:
            return None  # Unknown ingredient
        
        # If unit is already grams, return the quantity
        if unit in ['g', 'gram', 'grams']:
            return quantity
        
        # Convert based on the unit
        if unit in ['cup', 'cups']:
            return round(quantity * ingredient_data["gram_per_cup"])
        elif unit in ['tablespoon', 'tablespoons', 'tbsp']:
            return round(quantity * ingredient_data["gram_per_tablespoon"])
        elif unit in ['teaspoon', 'teaspoons', 'tsp']:
            return round(quantity * ingredient_data["gram_per_teaspoon"])
        elif unit in ['oz', 'ounce', 'ounces']:
            return round(quantity * 28.35)  # 1 oz = 28.35g
        elif unit in ['lb', 'pound', 'pounds']:
            return round(quantity * 453.59)  # 1 lb = 453.59g
        elif unit in ['ml', 'milliliter', 'milliliters']:
            if ingredient_data["type"] == "liquid":
                return round(quantity)  # 1ml of water = 1g
            else:
                return round(quantity * ingredient_data.get("density", 1))
        elif unit is None and name.lower() in ["egg", "eggs"]:
            # Handle eggs as a special case
            return round(quantity * 50)  # Assume 50g per egg
        else:
            return None  # Unknown unit
    
    def save_as_csv(self, results):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Recipe as CSV"
        )
        
        if not filename:
            return  # User cancelled
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Ingredient", "Original Measurement", "Weight (g)"])
                
                for item in results:
                    if item.get("is_header", False):
                        writer.writerow([item["original"], "", ""])
                    else:
                        gram_weight = item.get("gram_weight")
                        gram_str = f"{gram_weight}" if gram_weight is not None else "N/A"
                        writer.writerow([item["name"], item["original"], gram_str])
                
                # Add total weight
                total = sum(item.get("gram_weight", 0) or 0 for item in results)
                writer.writerow(["", "", ""])
                writer.writerow(["TOTAL WEIGHT", "", total])
            
            messagebox.showinfo("Success", f"Recipe saved to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def show_help(self):
        help_text = """Precision Baking - Usage Instructions

1. Enter your recipe in the text box on the left.
2. Each ingredient should be on a separate line.
3. Use standard measurements like cups, tablespoons, etc.
4. Click "Convert to Grams" to see the precise gram weights.
5. Save your converted recipe as a CSV file using the "Save as CSV" button.

Example format:
2 cups all-purpose flour
1/2 cup sugar
1 teaspoon salt

The app handles most common baking ingredients and units of measurement."""

        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x350")
        help_window.resizable(False, False)
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        
        close_button = ttk.Button(help_window, text="Close", command=help_window.destroy)
        close_button.pack(pady=(0, 20))

if __name__ == "__main__":
    root = tk.Tk()
    app = PrecisionBakingApp(root)
    app = update_app_with_new_parser(app)
    
    # Set the theme
    style = ttk.Style()
    style.theme_use('clam')  # Use a nicer theme than default
    
    # Configure colors
    style.configure('TFrame', background='#f9f5f0')
    style.configure('TLabelframe', background='#f9f5f0')
    style.configure('TLabelframe.Label', background='#f9f5f0', font=('Helvetica', 11, 'bold'))
    style.configure('TButton', background='#9a3b3b', foreground='#ffffff')
    style.map('TButton', background=[('active', '#7e2c2c')])
    
    root.configure(bg='#f9f5f0')
    root.mainloop()
