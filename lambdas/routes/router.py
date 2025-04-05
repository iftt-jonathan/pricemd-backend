from lambdas.db.athena_handlers import query_handler

def search_handler(event, context):
    name = event['startsWith'][0][1]
    query = f"SELECT * FROM hospitals.dummy_data WHERE procedure LIKE '%{name}%';"
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