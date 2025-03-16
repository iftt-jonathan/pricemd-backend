import json

from athena_handler import lambda_handler_for_athena 

def query_handler(event, context):
    name = event['startsWith'][0][1]

    print("querying for: ", name)

    query = f"SELECT * FROM hospitals.dummy_data WHERE procedure LIKE '%{name}%';"
    
    event = {"query": query}
    
    result = lambda_handler_for_athena({"query": query}, context)

    if "body" in result:
        return {
            'statusCode': 200,
            'body': json.dumps(result["body"])
        }
    else:
        return {
            'statusCode': 500,
            'message': result
        }