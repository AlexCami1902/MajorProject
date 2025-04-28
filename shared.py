import csv

names = [
        {"firstname": "Alex", "lastname": "Camilleri"},
        {"firstname": "Kath", "lastname": "Camilleri"},
        {"firstname": "Ben", "lastname": "Camilleri"},
]

with open('test.csv', mode='w') as csvfile:
    fieldnames = names[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in names:
        writer.writerow(row)
