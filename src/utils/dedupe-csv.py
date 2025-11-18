# some images represent more than one object, esp in 

import csv


seen = set()

hasdupes = "/tmp/img_segments/hasdupes.csv"
deduped = "/tmp/img_segments/deduped.csv"

# with open(hasdupes, 'r', newline='', encoding='utf-8') as input:
#     with open(deduped, 'w', newline='') as output:
#         writer = csv.writer(output)
#         reader = csv.reader(input)
#         header = next(reader)
#         writer.writerow(header)
#         for row in reader:
#             id = row[0]
#             if id in seen:
#                 continue
#             seen.add(id)
#             writer.writerow(row)
                 
records = {}

with open(hasdupes, 'r', newline='', encoding='utf-8') as input:
    reader = csv.DictReader(input)
    for record in reader:
        if records.get(record['id']):
            current_rec = records.get(record['id'])
            current_rec['represents'].append(record['represents'])
        else:
            tmp = record['represents']
            record['represents'] = []
            record['represents'].append(tmp)
            records[record['id']] = record


with open(deduped, 'w', newline='') as output:
    header = ['id', 'represents', 'caption', 'credits', 'uri', 'thumnail_url']
    writer = csv.writer(output)
    writer.writerow(header)
    for _,rec in records.items():
        rec['represents'] = ','.join(rec['represents'])
        writer.writerow(rec.values())
        
