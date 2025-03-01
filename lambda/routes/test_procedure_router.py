from procedure_router import get_handler, search_handler 
import json

def test_search_handler():
    result = search_handler("test", "test")
    assert result["statusCode"] == 200
    assert result["body"] is not None

    body =  json.loads(result["body"])
    first_result = body[0]
    
    assert first_result["procedure_id"] == 3
    assert first_result["procedure_name"] == "Tonsil Tumor Removal"


def test_get_handler():
    result = get_handler("test", "test")

    assert result["body"] is not None
    assert result["statusCode"] == 200

    body =  json.loads(result["body"])
    assert body["procedure_name"] == "Tonsil Tumor Removal"
    assert body["insurance_id"] == 4
    assert body["hospitals"] == [{"hospital_id": 66, "price": 55.00}]

# def test_failure():
#     assert False