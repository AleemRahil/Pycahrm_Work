import random
import smtplib
import datetime as dt

my_email = "XXXXXXXXXXXXX"
password = "XXXXXXXXXXXXX"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="XXXXXXXXXXXXX",
        msg="Subject:Hello\n\nThis is the body of my email"
    )
    connection.close()
    print("Email sent successfully")



now = dt.datetime.now()
year = now.year
month = now.month
day_of_week = now.weekday()

if day_of_week == 0:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)
        print(quote)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="XXXXXXXXXXXXX",
            msg=f"Subject:Monday Motivation\n\n{quote}"
        )
        connection.close()
        print("Email sent successfully")
date_of_birth = dt.datetime(year=1995, month=10, day=19, hour=0)