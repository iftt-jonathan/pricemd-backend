import json
import boto3
import time

from lambdas.db.hospital_info import get_hospital_info

def query_handler(context, query):

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
    

def lambda_handler_for_athena(event, context):
    athena = boto3.client('athena', region_name='us-east-1')

    database = 'hospitals' 
    table = 'dummy_data'   

    query = event['query']

    # output location for query results
    output_location = 's3://428-ihc-clean-dummy-data/athena-query-results/'

    # Start the query execution
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': output_location
        }
    )

    # Get the QueryExecutionId
    query_execution_id = response['QueryExecutionId']

    # Function to check query status
    def check_query_status(query_execution_id):
        while True:
            response = athena.get_query_execution(QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                return status
            time.sleep(1)  

    # Wait for the query to complete
    status = check_query_status(query_execution_id)

    if status == 'SUCCEEDED':
        results = athena.get_query_results(QueryExecutionId=query_execution_id)
        
        # print results
        for row in results['ResultSet']['Rows']:
            print([field['VarCharValue'] for field in row['Data']])

        body = []
        for i, row in enumerate(results['ResultSet']['Rows']):
            if i == 0: continue
            data = [field['VarCharValue'] for field in row['Data']]
            
            item = {}
            item["hospital_name"] = data[2]  # Assuming hospital name is in the 3rd column
            item["procedure_cost"] = int(data[1])  # Assuming cost is in the 2nd column
            item["procedure_name"] = data[0]  # Assuming procedure name is in the 1st column
            item["id"] = i  # Assign a unique ID based on the row index
            item["coordinates"] = get_coordinates(data[2])  # Get coordinates for the hospital
            
            body.append(item)
        
        return_results = {}
        return_results["body"] = body
        print(return_results)
        return return_results
    else:
        print(f"Query failed with status: {status}")
        return status

def get_coordinates(hospital_name):
    # Predefined coordinates for known hospitals
    coordinates_map = {
        "Utah Valley Instacare": [40.24900997146722, -111.66523075629274],
        "Intermountain Health Orem Community Hospital": [40.30287501307659, -111.70813516775206],
        "LDS Hospital": [40.77844723816021, -111.88030670375836],
        "St. Mark's Hospital": [40.685998548414844, -111.85689976890043],
        "St. John's Health": [43.48072394467286, -110.74964222795302],
        "Mayo Clinic": [44.02086539653745, -92.48116116074746],
        "Cleveland Clinic": [41.502784288611196, -81.62076867122296],
        "Johns Hopkins": [39.29682300960482, -76.59263471125068],
    }

    # Default to marbLocation if the hospital is not found
    marb_location = [40.24683398116889, -111.64919394644316]
    return coordinates_map.get(hospital_name, marb_location)
