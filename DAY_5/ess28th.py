import requests 

city = input("Enter your City: ")
API_KEY = "298b618796e8e0d288975fd775c7a230"

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q" : city,
    "appid" : API_KEY,
    "units" : "metric"
}

response = requests.get(url,params = params)

data = response.json()

for row in data:
    print(row,"",data[row])

if response.status_code == 200:
    print("\nWeather in", data["name"]) 
    print("Temperature:", data["main"]["temp"], "degree Celsius")
    print("Feels like:", data["main"]["feels_like"], "degree Celsius") 
    print("Humidity:", data["main"]["humidity"], "%") 

else:
    print("connection Failed")