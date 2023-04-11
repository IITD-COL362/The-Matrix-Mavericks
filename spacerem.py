import csv

# Open the input CSV file and create a list to store the corrected rows
with open('Restaurant.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = []
    for row in reader:
        # Strip leading/trailing spaces from each field in the row
        corrected_row = [field.strip() for field in row]
        # Append the corrected row to the list
        rows.append(corrected_row)

# Open the output CSV file and write the corrected rows
with open('Restaurant_final.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
