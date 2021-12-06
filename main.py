import os
import requests
from datetime import datetime, timezone
import smtplib
import time

MY_LAT = 42.960339  # Your latitude
MY_LONG = -7.734673  # Your longitude


def send_mail():
    sender = "Private Person <from@example.com>"
    receiver = "A Test User <to@example.com>"

    # the indentation is ignored in a multi-line string like this,
    # which causes mail to fail if it's not indented properly.
    # not sure how to get it working with the string indented
    message = f"""Subject: The ISS is nearby!
To: {receiver}
From: {sender}

Look up!"""
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("6e9cda1e96c233", os.environ.get("MAILTRAP_PASSWORD"))
        server.sendmail(sender, receiver, message)


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(f"mylat = {MY_LAT}, mylon = {MY_LONG}, isslat = {iss_latitude}, isslong = {iss_longitude}")

    #Your position is within +5 or -5 degrees of the ISS position.
    my_lat_low = MY_LAT - 5
    my_lat_high = MY_LAT + 5
    my_long_low = MY_LONG - 5
    my_long_high = MY_LONG + 5

    # test values
    # iss_latitude = 37.5644
    # iss_longitude = -72.4564

    # If the ISS is close to my current position
    if my_lat_low <= iss_latitude <= my_lat_high and my_long_low < iss_longitude < my_long_high:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    sunset_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sunset_response.raise_for_status()
    sunset_data = sunset_response.json()
    sunrise = int(sunset_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sunset_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc)
    current_hour = time_now.hour
    print(f"time = {current_hour}, sunrise = {sunrise}, sunset = {sunset}")

    # test value
    # current_hour = 3
    # and it is currently dark
    if current_hour >= sunset or current_hour <= sunrise:
        # BONUS: run the code every 60 seconds.
        return True

# print(is_night(), is_iss_overhead())

while True:
    if is_night() and is_iss_overhead():
        send_mail()
    time.sleep(60)





