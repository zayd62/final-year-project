# takes a size eg: 1.50kg and splits into size (1.55) and unit (kg)

import csv
import re
import string

csv_input = open("products_org.csv")
csv_reader = csv.reader(csv_input)

csv_output = open("product_size_splitted.csv", "w")
csv_writer = csv.writer(csv_output)

headers = next(csv_reader)
headers.append("unit")
csv_writer.writerow(headers)

for i in csv_reader:
    size = i[5].strip(string.ascii_letters)
    unit = i[5].strip(string.digits + string.punctuation)
    i[5] = size
    i.append(unit)
    csv_writer.writerow(i)

print("helo")