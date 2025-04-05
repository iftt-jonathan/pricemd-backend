from lambdas.db import query_handler

def search_handler(event, context):
    name = event['startsWith'][0][1]
    query = f"SELECT * FROM hospitals.dummy_data WHERE procedure LIKE '%{name}%';"
    print("querying for: ", name)

    return query_handler(context, query)