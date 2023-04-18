import csv

# Open the input CSV file and create a list to store the corrected rows
with open('restaurant_cuisine.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = []
    for row in reader:
        if(row[1]!=''):
            rows.append(row)

# Open the output CSV file and write the corrected rows
with open('Restaurant_cuisine_final.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
