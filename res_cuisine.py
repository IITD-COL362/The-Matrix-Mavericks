import csv

def generate_csv(input_file, output_file, col1_index, col2_index):
    # Read the input file into a list
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    
    # Extract the specified columns
    col1 = [row[col1_index] for row in data]
    col2 = [row[col2_index] for row in data]
    
    # Split the second column into a list of strings
    col2_split = [row.split(',') for row in col2]
    
    # Generate rows with first column and every entry in the split second column
    new_rows = []
    for i in range(len(data)):
        for item in col2_split[i]:
            new_row = [col1[i], item.strip()]
            new_rows.append(new_row)
    
    # Write the new rows to a new CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['col1', 'col2'])
        writer.writerows(new_rows)
    
    print(f'New CSV file written to {output_file}')

# Example usage: generate a new CSV file with rows from columns 0 and 1 of input.csv
# where every entry in column 1 is split by "," and repeated with column 0
generate_csv('zomato.csv', 'restaurant_cuisine.csv', 0, 9)
