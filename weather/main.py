# with open("./weather_data.csv") as weather_data:
#     data = weather_data.readlines()

# import csv
import pandas


# with open("./weather_data.csv") as data:
#     weather_data = csv.reader(data, delimiter="," )
#     # delimiter is the default value
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#
#     print(row)

data = pandas.read_csv("./2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
# print(type(data))
# print(data)
#
# data_dict = data.to_dict()
# print(data_dict)
#
# data_list = data["temp"].to_list()
# print (data_list)

a= len(data[data["Primary Fur Color"] == "Gray"])
b = len(data[data["Primary Fur Color"] == "Black"])
c= len(data[data["Primary Fur Color"] == "Cinnamon"])

data_dict = {
    "Fur Color": ["Gray", "Black", "Cinnamon"],
    "Count": [a, b, c]
}

df = pandas.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")