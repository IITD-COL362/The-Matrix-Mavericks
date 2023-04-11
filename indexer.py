import csv

# open the input file for reading and output file for writing
with open('Food.csv', 'r') as input_file, open('Food_final.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # write the header row with a modified first column
    header = next(reader)
    header[0] = 'Index'
    writer.writerow(header)

    # write the remaining rows with an index column
    index = 1
    for row in reader:
        row[0] = index
        writer.writerow(row)
        index += 1
