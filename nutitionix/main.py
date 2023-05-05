# import requests
# import datetime as dt
# APP_ID = "253e08e5"
# API_KEY = "d4a84b802db07445006c96f06b3fd679"
# MY_EMAIL = "projects.with.pycharm@gmail.com"
# exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
# SHEETY_USERNAME = "50c19efe6fd03071a2c8f395e166d0b4"
#
# sheety_endpoint = "https://api.sheety.co/50c19efe6fd03071a2c8f395e166d0b4/untitledSpreadsheet/sheet1"
#
# exercises = input("Tell me which exercises you did: ")
# params = {
#     "query": exercises,
#     "gender": "male",
#     "weight_kg": 70,
#     "height_cm": 170,
#     "age": 25
#     }
# headers = {
#     "x-app-id": APP_ID,
#     "x-app-key": API_KEY,
#     "x-remote-user-id": "0"
#     }
#
# response = requests.post(exercise_endpoint, json=params, headers=headers)
# results = response.json()["exercises"]
#
# time_now = dt.datetime.now()
# today = time_now.strftime("%d/%m/%Y")
#
# for exercise in results["exercises"]:
#
#         "sheet1": {
#             "date": today,
#             "time": exercise["duration_min"],
#             "exercise": exercise["name"].title(),
#             "calories": exercise["nf_calories"]
#         "date": today,
#         "time": exercise["duration_min"],
#         "exercise": exercise["name"].title(),
#         "calories": exercise["nf_calories"]
#     }
#         }
#     sheet_response = requests.post(sheety_endpoint, json=body)
#     print(sheet_response.text)


import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 178
AGE = 25

APP_ID = "253e08e5"
API_KEY = "d4a84b802db07445006c96f06b3fd679"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/50c19efe6fd03071a2c8f395e166d0b4/untitledSpreadsheet/sheet1"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

################### Start of Step 4 Solution ######################

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

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

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

    print(sheet_response.text)

    print(sheet_response.status_code)