import requests
from datetime import datetime
import smtplib

# change the variable to your lat and long

MY_LAT = "Your latitude"
MY_LONG = "Your longitude"


# Returns turn if the iss is close to you

def check_iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


# Return true if it is night

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    req = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    req.raise_for_status()
    time_data = req.json()
    sunrise = int(time_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(time_data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


# IF this does not work go https://myaccount.google.com/security and give access to less secured apps

my_email = "Your Email address"
password = "Your password"

# Runs if check_iss_location and is_night is True

if check_iss_location() and is_night():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="to email",
            msg=f"Subject:LOOK UP\n\n ISS IS ABOVE YOU IN SKY"
        )
