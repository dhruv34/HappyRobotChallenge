import json
import os
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    mc_number = event["pathParameters"]["mc_number"]
    url = "https://mobile.fmcsa.dot.gov/qc/services/carriers/docket-number/" + str(mc_number)
    web_key = os.getenv("FMCSA_KEY")
    try:
        response = http.request("GET", url, fields={"webKey": web_key})
        if response.status == 200:
            data = json.loads(response.data.decode("utf-8"))
            legal_name = data.get("content", [{}])[0].get("carrier", {}).get("legalName", "Unknown")
            allowed_to_operate = data.get("content", [{}])[0].get("carrier", {}).get("allowedToOperate", "Unknown")
            return {
                "statusCode": 200,
                "body": json.dumps({"name": legal_name, "allowedToOperate": allowed_to_operate})
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to fetch carrier info"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
