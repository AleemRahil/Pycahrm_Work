import time
import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 178
AGE = 25

NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_API_KEY = os.environ["NUTRITIONIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEETY_ENDPOINT"]


exercises_input = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

parameters = {
    "query": exercises_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
        "Authorization": f"Bearer {os.environ['YOUR_TOKEN']}"
    }
# define the condition for which rows should be deleted
condition = lambda row: row['exercise'] == 'Sexual Activity'

# retrieve all rows from the worksheet
response2 = requests.get(sheet_endpoint, headers=bearer_headers)
rows = response2.json()['sheet1']

# loop through the rows and delete the ones that match the condition
for row in rows:
    if condition(row):
        id = row['id']
        delete_url = f"{sheet_endpoint}/2/{id}"
        response2 = requests.delete(delete_url)
        # append a unique query string to force Sheety to update the cache
        timestamp = int(time.time() * 1000)
        query_string = f"?_={timestamp}"
        endpoint_with_query = f"{sheet_endpoint}/2" + query_string

        response = requests.get(endpoint_with_query)
        print(f"Row with ID {id} deleted.")

print('Rows deleted.')

for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)


