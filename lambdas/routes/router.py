from lambdas.db.athena_handlers import query_handler
import json

def search_handler(event, context):
    # Parse the body from the event
    body = json.loads(event['body'])

    # Extract the search term
    name = body['startsWith'][0][1]

    query = f"SELECT * FROM hospitals.dummy_data WHERE LOWER(procedure) LIKE LOWER('%{name}%');"
    print("querying for: ", name)

    return query_handler(context, query)

def get_handler(event, context):
    procedure_id = event['pathParameters']['procedureId']
    insurance_id = event['pathParameters']['insuranceId']

    # query = f"SELECT * FROM hospitals.dummy_data WHERE procedure = '{procedure_id}' AND insurance = '{insurance_id}';"
    # print(f"Querying for procedure: {procedure_id}, insurance: {insurance_id}")

    query = f"SELECT * FROM hospitals.dummy_data WHERE procedure = '{procedure_id}';"
    print(f"Querying for procedure: {procedure_id}")

    return query_handler(context, query)