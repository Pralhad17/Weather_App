from django.shortcuts import render
import urllib.request
import json
from urllib.error import HTTPError

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city', '')  # Get city from POST data
        if city:
            try:
                api_key = '4f1e0cf70b1773e34d30c5d1965fcc26'  # Replace with your actual API key
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
                source = urllib.request.urlopen(url).read()
                list_of_data = json.loads(source)

                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                    "temp": str(list_of_data['main']['temp']) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                    "main": str(list_of_data['weather'][0]['main']),
                    "description": str(list_of_data['weather'][0]['description']),
                    "icon": list_of_data['weather'][0]['icon'],
                }
            except HTTPError as e:
                error_message = f"Error fetching data: {e}"
                return render(request, "main/index.html", {"error_message": error_message})
            except KeyError:
                error_message = f"Data for {city} not found. Please enter a valid city name."
                return render(request, "main/index.html", {"error_message": error_message})
            except Exception as e:
                error_message = f"Unexpected error: {e}"
                return render(request, "main/index.html", {"error_message": error_message})
        else:
            data = {}
            error_message = "Please enter a city name."
            return render(request, "main/index.html", {"error_message": error_message})

    else:
        data = {}

    return render(request, "main/index.html", data)
 