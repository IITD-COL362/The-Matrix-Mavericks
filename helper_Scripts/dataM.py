import csv
with open('zomato.csv', 'r') as file:
	reader = csv.reader(file)
	cuisine_set = {""}
	for row in reader:
		cuisine_list =  [x.strip() for x in row[9].split(',')]
		for elem in cuisine_list:
			cuisine_set.add(elem)
	cuisine_set.remove("")
	print(cuisine_set)
	print(len(cuisine_set))