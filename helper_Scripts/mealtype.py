import csv

# Open the input CSV file and create a set to store the incorrect values
with open('Food.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    incorrect_values = set()
    for row in reader:
        # Check if the 8th column is one of the 9 types
        if row[8] not in ['Fruits', 'Wheat based', 'Rice based', 'Meat based', 'Sea food based', 'Salad based', 'Milk based', 'Junk food', 'Vegetarian based','Beverage','Dessert','Egg based']:
            incorrect_values.add(row[8])

# Print the incorrect values
if len(incorrect_values) > 0:
    print('The following values in column 8 are incorrect:')
    for value in incorrect_values:
        print(value)
else:
    print('All values in column 8 are correct.')

