
// "borrowed" from MDN's geolocation API example
function geoFindMe() {
  console.log("calling geofindme");
  const status = document.querySelector('#weatherStatus');

  function success(position) {
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    const latitude_input = document.querySelector("#latitude-input");
    const longitude_input = document.querySelector("#longitude-input");

    longitude_input.value = longitude;
    latitude_input.value = latitude;
    console.log(`${latitude}, ${longitude}`);
    status.textContent = "";
  }

  function error() {
    status.textContent = 'Unable to retrieve your location';
  }

  if (!navigator.geolocation) {
    status.textContent = 'Geolocation is not supported by your browser';
  } else {
    status.textContent = 'Locating…';
    navigator.geolocation.getCurrentPosition(success, error);
  }

}

WEATHER_CODES = {
  0: 'Clear sky',
  1: 'Mainly clear',
  2: 'Partly cloudy',
  3: 'Overcast',
  45: 'Fog',
  48: 'Depositing Rime fog',
  51: 'Light Drizzle',
  53: 'Moderate Drizzle',
  55: 'Dense Drizzle',
  57: 'Light Freezing Drizzle',
  57: 'Dense Freezing Drizzle',
  61: 'Slight Rain',
  63: 'Moderate Rain',
  65: 'Heavy Rain',
  66: 'Light Freezing Rain',
  67: 'Heavy Freezing Rain',
  71: 'Slight Snow fall',
  73: 'Moderate Snow fall',
  75: 'Heavy Snow fall',
  77: 'Snow grains',
  80: 'Slight Rain showers',
  81: 'Moderate Rain showers',
  82: 'Violent Rain showers',
  85: 'Slight Snow showers slight and heavy',
  86: 'Heavy Snow showers slight and heavy',
  95: 'Thunderstorm',
  96: 'Thunderstorm with slight hail',
  99: 'Thunderstorm with heavy hail',
}

function getWeather() {
  // read latitude and longitude - Is this fine? becuase in my intuition, I feel like I have to use geoFindMe function instead?
  const status = document.querySelector('#weatherStatus');

  function success(position) {
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    const latitude_input = document.querySelector("#latitude-input");
    const longitude_input = document.querySelector("#longitude-input");

    longitude_input.value = longitude;
    latitude_input.value = latitude;
    console.log(`${latitude}, ${longitude}`);
    status.textContent = "";

    // CALL API FUNCTIONS
    getWeatherAPI(latitude, longitude);
    getSunAPI(latitude, longitude);
  }

  function error() {
    status.textContent = 'Unable to retrieve your location';
  }

  if (!navigator.geolocation) {
    status.textContent = 'Geolocation is not supported by your browser';
  } else {
    status.textContent = 'Locating…';
    navigator.geolocation.getCurrentPosition(success, error);
  }

  // open-meteo web request
  async function getWeatherAPI(latitude, longitude) {
    console.log('getWeatherAPI', latitude, longitude);
    try {
      let res = await fetch("https://api.open-meteo.com/v1/forecast?latitude=" + latitude + "&longitude=" + longitude
        + "7&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=ms&timezone=America%2FChicago");
      if (res.ok) {
        let json = await res.json();
        // console.log(json); // check json
        let temperature = json.current_weather.temperature;
        let weathercode = json.current_weather.weathercode;
        let weather = WEATHER_CODES[weathercode];
        let tempUnit = ' Degrees F';
        // console.log(temperature, weather); // To check if runs simutaneously
        document.getElementById('temp-display').innerText = 'Temperature: ' + temperature + tempUnit;
        document.getElementById('cloud-cover-display').innerText = weather;

      } else {
        console.log('res not ok');
      }
    } catch (error) {
      document.getElementById('weatherStatus').innerText =
        document.getElementById('weatherStatus').innerText + 'getWeatherAPI Error: ' + error + "\n";
    }
  }

  // sunset-sunrise web request
  async function getSunAPI(latitude, longitude) {
    console.log('getSunAPI', latitude, longitude);
    try {
      let res = await fetch("https://api.sunrise-sunset.org/json?lat=" + latitude + "&lng=" + longitude + "&formatted=0");
      if (res.ok) {
        let json = await res.json();
        // console.log(json); // check json
        // referenced from hw description
        let sunrise = new Date(json.results.sunrise).toLocaleTimeString();
        let sunset = new Date(json.results.sunset).toLocaleTimeString();
        // console.log(sunrise, sunset); // To check if runs simutaneously
        document.getElementById('sunrise-display').innerText = 'Sunrise: ' + sunrise;
        document.getElementById('sunset-display').innerText = 'Sunset: ' + sunset;
      } else {
        console.log('res not ok');
      }
    } catch (error) {
      document.getElementById('weatherStatus').innerText =
        document.getElementById('weatherStatus').innerText + getSunAPI + error + '\n';
    }
  }
}

document.querySelector('#find-me').addEventListener('click', geoFindMe);
document.querySelector("#get-weather-btn").addEventListener('click', getWeather);
