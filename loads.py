import csv
import json

def load_csv_data(file_path):
    data = {}
    with open(file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)
        for row in reader:
            reference_number = row[0]
            origin = f"{row[1]}, {row[2]}"
            destination = f"{row[3]}, {row[4]}"
            data[reference_number] = {
                "reference_number": reference_number,
                "origin": origin,
                "destination": destination,
                "equipment_type": row[5],
                "rate": row[6],
                "commodity": row[7]
            }
    return data

def lambda_handler(event, context):
    reference_number = event["pathParameters"]["reference_number"]
    load_data = load_csv_data('loads.csv')
    load_details = load_data.get(reference_number)
    
    if not load_details:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Load not found"})
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps(load_details),
    }
