# Key: Hospital name
_hospital_info = {}

def get_hospital_info(hospital_name):
    return _hospital_info.get(hospital_name.lower(), {})

def add_hospital_info(hospital_name, info):
    _hospital_info[hospital_name.lower()] = info

add_hospital_info('American Fork Hospital', {
    "address": "170 N 1100 E, American Fork, UT",
    "website": "https://web-ih-sc-prd-hdl-wus2.azurewebsites.net/locations/american-fork-hospital"
})
add_hospital_info('Placeholder', {
    "address": "331 North 400 West, Orem, UT",
    "website": "https://web-ih-sc-prd-hdl-wus2.azurewebsites.net/locations/orem-community-hospital"
})