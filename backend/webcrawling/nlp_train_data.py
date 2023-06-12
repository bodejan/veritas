import csv
import time
from androidrank_crawler import get_ids_for_category
from playstore_crawler import get_name_logo_url_policy_by_id
from models import CATEGORIES

categories = CATEGORIES

def get_all_ids():
    id_list = []
    for c in categories.keys():
        start_time = time.time()
        id_list_category = get_ids_for_category(c, 500)
        

        # Export metrics
        end_time = time.time()
        row = []
        row.append(c)
        row.append(end_time - start_time)
        row.append(len(id_list_category))
        with open('backend/src/webcrawling/policy_export/all_ids_metrics.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Category', 'Execution Time', 'Ids'])
            writer.writerow(row)

        print(f'{c}: {len(id_list_category)}/500 in {end_time - start_time}s')

        for id in id_list_category: id_list.append(id)
        id_list = list(set(id_list))

        # Export the array to a file
        with open('backend/src/webcrawling/policy_export/all_ids.txt', 'w') as f:
            for id in id_list:
                f.write("%s\n" % id)
        
def get_all_policies():
    # Import the array from the file
    ids = []
    with open(f'backend/src/webcrawling/policy_export/all_ids.txt', 'r') as f:
        for line in f:
            ids.append(line.strip())

    # Get policy
    for i in range(1002, len(ids)):
        id = ids[i]
        start_time = time.time()
        success = get_name_logo_url_policy_by_id(id)
        end_time = time.time()
        if success: 
            print(f'{id} crawled successfully in {end_time-start_time}')
        else: 
            print(f'Unable to crawl {id}')
        # Export metrics
        row = []
        row.append(id)
        row.append(end_time - start_time)
        row.append(success)
        with open('backend/src/webcrawling/policy_export/all_policies_metric.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Id', 'Execution Time', 'Success'])
            writer.writerow(row)

# get_all_ids()
get_all_policies()

