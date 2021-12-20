import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

API_key = os.environ.get("OW_KEY")
LAT = 38.722252
LONG = -9.139337
EXCLUDE = "minutely,current,daily"
ACCOUNT_SID = "AC0329c5dd35b3a0ba313a23847a936369"
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

PARAMETERS = {"lat": LAT, "lon": LONG, "appid": API_key, "exclude": EXCLUDE}
client = Client(ACCOUNT_SID, AUTH_TOKEN)

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=PARAMETERS)
response.raise_for_status()
weather_data = response.json()

today_weather = ([hour["weather"][0]["id"] for hour in weather_data["hourly"][0:12]])

will_rain = False

for code in today_weather:
    if code < 800:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
    client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=proxy_client)
    message = client.messages.create(
        from_="+19165367693",
        to="+64211898173",
        body="Remember to bring an umbrella☂"
    )
    print(message.status)
else:
    print("Remember to put on sunscreen")