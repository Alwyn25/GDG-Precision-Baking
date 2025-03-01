# ingredient_database.py

INGREDIENT_DATABASE = [
    # Flours
    {
        "name": "all-purpose flour",
        "type": "dry",
        "density": 0.53,
        "gram_per_cup": 125,
        "gram_per_tablespoon": 8,
        "gram_per_teaspoon": 2.6
    },
    {
        "name": "bread flour",
        "type": "dry",
        "density": 0.55,
        "gram_per_cup": 130,
        "gram_per_tablespoon": 8.1,
        "gram_per_teaspoon": 2.7
    },
    {
        "name": "cake flour",
        "type": "dry",
        "density": 0.4,
        "gram_per_cup": 114,
        "gram_per_tablespoon": 7.1,
        "gram_per_teaspoon": 2.4
    },
    {
        "name": "whole wheat flour",
        "type": "dry",
        "density": 0.53,
        "gram_per_cup": 120,
        "gram_per_tablespoon": 7.5,
        "gram_per_teaspoon": 2.5
    },
    {
        "name": "rye flour",
        "type": "dry",
        "density": 0.5,
        "gram_per_cup": 102,
        "gram_per_tablespoon": 6.4,
        "gram_per_teaspoon": 2.1
    },
    
    # Sugars
    {
        "name": "granulated sugar",
        "type": "dry",
        "density": 0.85,
        "gram_per_cup": 200,
        "gram_per_tablespoon": 12.5,
        "gram_per_teaspoon": 4.2
    },
    {
        "name": "white sugar",
        "type": "dry",
        "density": 0.85,
        "gram_per_cup": 200,
        "gram_per_tablespoon": 12.5,
        "gram_per_teaspoon": 4.2
    },
    {
        "name": "brown sugar",
        "type": "dry",
        "density": 0.75,
        "gram_per_cup": 220,
        "gram_per_tablespoon": 13.8,
        "gram_per_teaspoon": 4.6
    },
    {
        "name": "powdered sugar",
        "type": "dry",
        "density": 0.56,
        "gram_per_cup": 120,
        "gram_per_tablespoon": 7.5,
        "gram_per_teaspoon": 2.5
    },
    {
        "name": "confectioners sugar",
        "type": "dry",
        "density": 0.56,
        "gram_per_cup": 120,
        "gram_per_tablespoon": 7.5,
        "gram_per_teaspoon": 2.5
    },
    
    # Dairy
    {
        "name": "butter",
        "type": "solid",
        "density": 0.96,
        "gram_per_cup": 227,
        "gram_per_tablespoon": 14.2,
        "gram_per_teaspoon": 4.7
    },
    {
        "name": "milk",
        "type": "liquid",
        "density": 1.03,
        "gram_per_cup": 240,
        "gram_per_tablespoon": 15,
        "gram_per_teaspoon": 5
    },
    {
        "name": "heavy cream",
        "type": "liquid",
        "density": 0.98,
        "gram_per_cup": 238,
        "gram_per_tablespoon": 14.9,
        "gram_per_teaspoon": 5
    },
    {
        "name": "sour cream",
        "type": "semi-solid",
        "density": 1.05,
        "gram_per_cup": 230,
        "gram_per_tablespoon": 14.4,
        "gram_per_teaspoon": 4.8
    },
    {
        "name": "cream cheese",
        "type": "semi-solid",
        "density": 1.01,
        "gram_per_cup": 227,
        "gram_per_tablespoon": 14.2,
        "gram_per_teaspoon": 4.7
    },
    {
        "name": "yogurt",
        "type": "semi-solid",
        "density": 1.03,
        "gram_per_cup": 245,
        "gram_per_tablespoon": 15.3,
        "gram_per_teaspoon": 5.1
    },
    
    # Oils
    {
        "name": "vegetable oil",
        "type": "liquid",
        "density": 0.92,
        "gram_per_cup": 218,
        "gram_per_tablespoon": 13.6,
        "gram_per_teaspoon": 4.5
    },
    {
        "name": "olive oil",
        "type": "liquid",
        "density": 0.91,
        "gram_per_cup": 216,
        "gram_per_tablespoon": 13.5,
        "gram_per_teaspoon": 4.5
    },
    {
        "name": "coconut oil",
        "type": "semi-solid",
        "density": 0.92,
        "gram_per_cup": 218,
        "gram_per_tablespoon": 13.6,
        "gram_per_teaspoon": 4.5
    },
    
    # Nuts and seeds
    {
        "name": "almonds",
        "type": "dry",
        "density": 0.64,
        "gram_per_cup": 150,
        "gram_per_tablespoon": 9.4,
        "gram_per_teaspoon": 3.1
    },
    {
        "name": "walnuts",
        "type": "dry",
        "density": 0.55,
        "gram_per_cup": 120,
        "gram_per_tablespoon": 7.5,
        "gram_per_teaspoon": 2.5
    },
    
    # Leavening agents
    {
        "name": "baking powder",
        "type": "dry",
        "density": 0.9,
        "gram_per_cup": 230,
        "gram_per_tablespoon": 14.4,
        "gram_per_teaspoon": 4.8
    },
    {
        "name": "baking soda",
        "type": "dry",
        "density": 0.9,
        "gram_per_cup": 230,
        "gram_per_tablespoon": 14.3,
        "gram_per_teaspoon": 4.8
    },
    {
        "name": "yeast",
        "type": "dry",
        "density": 0.75,
        "gram_per_cup": 150,
        "gram_per_tablespoon": 9.4,
        "gram_per_teaspoon": 3.1
    },
    
    # Salt and spices
    {
        "name": "salt",
        "type": "dry",
        "density": 1.2,
        "gram_per_cup": 273,
        "gram_per_tablespoon": 17,
        "gram_per_teaspoon": 5.7
    },
    {
        "name": "cinnamon",
        "type": "dry",
        "density": 0.56,
        "gram_per_cup": 120,
        "gram_per_tablespoon": 7.5,
        "gram_per_teaspoon": 2.5
    },
    {
        "name": "cocoa powder",
        "type": "dry",
        "density": 0.5,
        "gram_per_cup": 100,
        "gram_per_tablespoon": 6.3,
        "gram_per_teaspoon": 2.1
    },
    
    # Sweeteners
    {
        "name": "honey",
        "type": "liquid",
        "density": 1.42,
        "gram_per_cup": 340,
        "gram_per_tablespoon": 21.3,
        "gram_per_teaspoon": 7.1
    },
    {
        "name": "maple syrup",
        "type": "liquid",
        "density": 1.37,
        "gram_per_cup": 320,
        "gram_per_tablespoon": 20,
        "gram_per_teaspoon": 6.7
    },
    
    # Eggs
    {
        "name": "egg",
        "type": "whole",
        "density": 1.03,
        "gram_per_cup": 243,
        "gram_per_tablespoon": 15.2,
        "gram_per_teaspoon": 5.1,
        "gram_per_unit": 50  # Average weight of one large egg
    },
    {
        "name": "egg white",
        "type": "liquid",
        "density": 1.03,
        "gram_per_cup": 243,
        "gram_per_tablespoon": 15.2,
        "gram_per_teaspoon": 5.1,
        "gram_per_unit": 30  # Average weight of one large egg white
    },
    {
        "name": "egg yolk",
        "type": "semi-solid",
        "density": 1.03,
        "gram_per_cup": 243,
        "gram_per_tablespoon": 15.2,
        "gram_per_teaspoon": 5.1,
        "gram_per_unit": 18  # Average weight of one large egg yolk
    },
    
    # Fruits
    {
        "name": "raisins",
        "type": "dry",
        "density": 0.64,
        "gram_per_cup": 165,
        "gram_per_tablespoon": 10.3,
        "gram_per_teaspoon": 3.4
    },
    {
        "name": "chocolate chips",
        "type": "dry",
        "density": 0.68,
        "gram_per_cup": 170,
        "gram_per_tablespoon": 10.6,
        "gram_per_teaspoon": 3.5
    }
]
