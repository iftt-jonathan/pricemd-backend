import boto3
import time

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
            item["procedure"] = data[0]
            item["standard_charge"] = data[1]
            item["hospital"] = data[2]
            
            body.append(item)
        
        return_results = {}
        return_results["body"] = body
        print(return_results)
        return return_results
    else:
        print(f"Query failed with status: {status}")
        return status