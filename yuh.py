import requests
import csv
import time

def generate_grid_points(lat_start, lat_end, long_start, long_end, step=0.5):
    """Generate grid points within specified bounds with given step size."""
    grid_points = []
    lat = lat_start
    while lat <= lat_end:
        long = long_start
        while long <= long_end:
            grid_points.append({'lat': lat, 'lng': long})
            long += step
        lat += step
    return grid_points

def fetch_locations(lat, lng):
    """Fetch location data from the Starbucks API for given latitude and longitude."""
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'ux_exp_id=4d67b193-ec81-47cf-89be-75797709775f; tiWQK2tY=A_ZP_XOQAQAAe7RnE-BeiR1H4YEwNB2IC1zH3K-swCNDYrZAOlbRKhPBy3cDAWKsDREXTuopwH8AAEB3AAAAAA|1|0|8edde7a1d27628878bc54487f53e291d2df5ac12; ai_user=AUazC1+VNYJV+CO9tFEPRK|2024-07-02T15:08:19.928Z; _gcl_au=1.1.139510108.1719932900; fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef=BP71E28kn/TsDZFgLlNOXNXYrZcsxjE0onITshhQ9e8=; TAsessionID=ebbc149f-609b-41c7-8212-03387e0c6d51|EXISTING; _gid=GA1.2.878103380.1720470464; _dc_gtm_UA-82424379-1=1; notice_behavior=implied,us; notice_gdpr_prefs=0,1,2:; notice_preferences=2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; ai_session=xGcbh9r/HdI24l0CWWepvI|1720470463408|1720471361695; _ga=GA1.1.815480446.1719932901; _uetsid=881a61c03d6811ef93112f8dcf55820b; _uetvid=eb610ac0388411ef9a30a527cb8b4163; ZpO6ggvs; _ga_Q8JXK1T67J=GS1.1.1720470464.3.1.1720471372.0.0.0; _ga_VMTHZW7WSM=GS1.1.1720470464.3.1.1720471372.0.0.0',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMDc1MTkiLCJhcCI6IjI0NTQ5MzA1IiwiaWQiOiJiYjM0NGJiZjRkMGY0NmZjIiwidHIiOiI2MjBmZDdlYWNlZDJkMTcwODljYjU0ZjE5YmE1OWE1YiIsInRpIjoxNzIwNDcxMzcyMzM2LCJ0ayI6IjEzMDYzMTIifX0=',
    'priority': 'u=1, i',
    'referer': 'https://www.starbucks.com/store-locator?map=45.553737,-122.79793,11z',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-620fd7eaced2d17089cb54f19ba59a5b-bb344bbf4d0f46fc-01',
    'tracestate': '1306312@nr=0-1-1307519-24549305-bb344bbf4d0f46fc----1720471372336',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'lat': lat,
        'lng': lng,
    }
    url = 'https://www.starbucks.com/bff/locations'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data for coordinates (", lat, ",", lng, ") - Status Code:", response.status_code)
        return []

def write_to_csv(writer, data):
    """Write fetched data to CSV."""
    if not data:
        print("No data received for current request.")
    for entry in data:
        store = entry.get('store', {})
        address = store.get('address', {})
        coordinates = store.get('coordinates', {})
        name = store.get('name', 'No Name Provided')
        line1 = address.get('streetAddressLine1', '')
        line2 = address.get('streetAddressLine2', '')
        city = address.get('city', '')
        state = address.get('countrySubdivisionCode', '')
        postal_code = address.get('postalCode', '')
        latitude = coordinates.get('latitude', '')
        longitude = coordinates.get('longitude', '')
        writer.writerow([name, line1, line2, city, state, postal_code, latitude, longitude])
def main():
    # Define the bounds of the continental US
    lat_start, lat_end = 24.396308, 49.384358
    long_start, long_end = -125.001650, -66.934570
    step = 0.5

    # Generate grid points
    grid_points = generate_grid_points(lat_start, lat_end, long_start, long_end, step)

    # Open CSV file to store the results
    with open('starbucks_locations_usa.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Address Line 1', 'Address Line 2', 'City', 'State', 'Postal Code'])

        # Iterate over grid points and fetch location data
        for point in grid_points:
            print("Fetching data for latitude:", point['lat'], "longitude:", point['lng'])
            data = fetch_locations(point['lat'], point['lng'])
            write_to_csv(writer, data)
            time.sleep(1.3)
    
    print("Data extraction complete. CSV file is ready.")

if __name__ == "__main__":
    main()
