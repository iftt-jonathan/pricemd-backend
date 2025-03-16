import json
import pyathena

from query import query_handler


def search_handler(event, context):
    return query_handler(event, context)
    


def get_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "procedure_id": 3,
                "procedure_name": "Tonsil Tumor Removal",
                "insurance_id": 4,
                "insurance_name": "Medicare",
                "hospitals": [{"hospital_id": 66, "price": 55.00}],
                "statistics": {"avg_cost": 500000.00}
            }
        ),
    }
