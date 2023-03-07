import smtplib as sm
import time
from datetime import datetime

import requests

MY_LAT = 6.465422  # Your latitude
MY_LONG = 3.406448  # Your longitude
your_email = "t2637210@gmail.com"
your_password = "mgadvwlblerguhsu"
iss_latitude = 0
iss_longitude = 0


# Your position is within +5 or -5 degrees of the ISS position.
def position_checker():
    global iss_latitude, iss_longitude
    # Get the latitude and longitude from the ISS API.
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_data = response.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    # If the ISS is close to my current position, then return True.
    if (iss_latitude - 5) <= MY_LAT <= (iss_latitude + 5) and (iss_longitude - 5) <= MY_LONG <= (iss_longitude + 5):
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Use the sunrise-sunset API to get the sunrise and sunset in your location.
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # Get the hours from the sunrise and sunset datetime.
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    # If the current time is between the sunset and sunrise, then it is nighttime.
    current_time = datetime.now().hour
    if current_time >= sunset or current_time <= sunrise:
        return True

pro


while True:
    # ISS is close to my current position,
    # # and it is currently dark
    if position_checker() and is_night():
        # Then email me to tell me to look up.
        conn = sm.SMTP_SSL("smtp.gmail.com", 465)
        conn.login(user=your_email, password=your_password)
        conn.sendmail(from_addr=your_email, to_addrs="nweremizubruno@gmail.com",
                      msg="Subject:ISS LOCATED\n\nBruno!!!!!!!|")
    else:
        # print(MY_LAT, MY_LONG)
        print(iss_longitude, iss_latitude)
        print("ISS NOT CLOSE TO YOUR POSITION OR IT IS NOT DARK YET")
    # Run the code every 60 seconds.
    time.sleep(60)
