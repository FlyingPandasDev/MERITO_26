from src.microservices.read_services import read_json, read_csv, read_microservice_config
from src.connectors.db_connector import get_products
import pandas as pd
from pathlib import Path

def microManager(route) :
    if route == "read_json":
        user_microservice_object = read_json()
        llm_microservice_value = str(user_microservice_object)
        userId = f"server_{route}"
    elif route == "read_csv":
        user_microservice_object = read_csv()
        llm_microservice_value = str(user_microservice_object)
        userId = f"server_{route}"
    else:
        config = read_microservice_config()
        microservices = config["microservices"]
        microservice_details = microservices.get(route)
        print(microservice_details)
        if microservice_details and microservice_details["active"]:
            sql = microservice_details["sql"]
            sql_data = get_products(sql)
            user_microservice_object = pd.DataFrame(sql_data)
            llm_microservice_value = str(user_microservice_object)
            print(user_microservice_object)
            userId = f"server_{route}"
        else:
            user_microservice_object = None
            llm_microservice_value = f"Microservice {route} not found or inactive."
            userId = f"server_{route}"
       
    return user_microservice_object, llm_microservice_value, userId



