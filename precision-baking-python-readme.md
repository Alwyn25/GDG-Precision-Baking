# Precision Baking: Python Measurement Converter

A Python desktop application that converts recipe measurements from cups, tablespoons, and teaspoons into precise gram weights for consistent baking results.

## Features

- **Text Analysis**: Parses recipe text to extract ingredients, quantities, and units
- **Precise Conversion**: Converts common baking measurements to exact gram weights
- **Comprehensive Database**: Includes density information for 30+ common baking ingredients
- **Export Options**: Save converted recipes as CSV files
- **User-Friendly GUI**: Built with Tkinter for a simple, intuitive interface

## Requirements

- Python 3.6+
- Tkinter (included with most Python installations)

## Installation

1. Clone the repository or download the source files
2. Ensure Python 3.6+ is installed on your system
3. Run the application:

```
python main.py
```

## Usage

1. Launch the application by running `main.py`
2. Enter your recipe in the text box on the left, with each ingredient on a separate line
3. Click "Convert to Grams" to process the recipe
4. View the converted measurements in the table on the right
5. Save the converted recipe as a CSV file by clicking "Save as CSV"

## Example Input

```
2 cups all-purpose flour
1/2 cup white sugar
1 teaspoon baking powder
1/2 teaspoon salt
1 cup milk
1/4 cup butter, melted
2 eggs
```

## How It Works

1. **Input Parsing**: The application uses regular expressions to extract quantity, unit, and ingredient name from each line of text.

2. **Ingredient Matching**: Each ingredient is matched against our database containing density information.

3. **Conversion Algorithm**: The application uses the following conversion logic:
   - For volume measurements (cups, tablespoons, teaspoons), it multiplies by the ingredient-specific density
   - For weight measurements (ounces, pounds), it uses standard weight conversions
   - For liquids measured in volume, it accounts for specific gravity
   - Special handling for eggs and other unique ingredients

4. **Output Formatting**: The converted recipe is displayed in a clear, tabular format with original and converted measurements side by side.

## Expanding the Database

To add new ingredients to the database, modify the `ingredient_database.py` file by adding new entries to the `INGREDIENT_DATABASE` list:

```python
{
    "name": "ingredient name",
    "type": "dry|liquid|semi-solid|solid",
    "density": 0.00,  # density in g/ml
    "gram_per_cup": 000,
    "gram_per_tablespoon": 00,
    "gram_per_teaspoon": 0.0
}
```

## Project Structure

- `precision-baking-converter-python.py` - Main application file with GUI and conversion logic
- `ingredient_database.py` - Database of ingredient densities and conversion factors

## Future Enhancements

- Recipe saving and loading
- Ability to adjust recipe servings
- Unit conversion for temperature and pan sizes
- Print functionality
- User-customizable ingredient database
- Image recognition for printed recipes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Data sources for ingredient density information:
  - King Arthur Flour Ingredient Weight Chart
  - USDA Food Composition Database
  - Professional baker community contributions