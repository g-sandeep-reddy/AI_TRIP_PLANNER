import httpx

from backend.models import WeatherData


def get_weather(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
    }

    response = httpx.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return WeatherData(
        temperature=current["temperature_2m"],
        humidity=current["relative_humidity_2m"],
        weather_code=current["weather_code"],
        wind_speed=current["wind_speed_10m"],
    )


if __name__ == "__main__":
    weather = get_weather(10.0889, 77.0595)
    print(weather)