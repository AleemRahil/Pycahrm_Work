##################### Extra Hard Starting Project ######################
import random, pandas, datetime as dt, smtplib

# 1. Update the birthdays.csv
birth_data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in birth_data.iterrows()}
oriented_dict = birth_data.to_dict(orient="records")

# 2. Check if today matches a birthday in the birthdays.csv

today = dt.datetime.now()
today_tuple = (today.month, today.day)

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

if today_tuple in  birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]

# 4. Send the letter generated in step 3 to that person's email address.

    with open(f"./letter_templates/letter_{random.randint(1,3)}.txt") as file:
        letter = file.read()
        letter = letter.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user="XXXXXXXXXX", password="your_password")
                connection.sendmail(
                    from_addr="your_email",
                    to_addrs=birthday_person["email"],
                    msg=f"Subject:Happy Birthday\n\n{letter}"
                )


