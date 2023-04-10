import csv

def extract_columns(filename, num_columns, *column_indices):
    # Read in the CSV file
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    # Extract the specified columns and remove duplicates
    extracted_data = set()
    for row in data[1:]:
        extracted_row = tuple(row[i] for i in column_indices)
        extracted_data.add(extracted_row)
    
    # Write the extracted data to a new CSV file
    with open('City.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data[0][i] for i in column_indices])
        for row in extracted_data:
            writer.writerow(row)
    
    print(f'{num_columns} columns extracted and written to extracted_data.csv')

# Example usage: extract columns 0 and 2 from example.csv
extract_columns('zomato.csv', 2, 2, 3)
