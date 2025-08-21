
import requests

# Your GoMaps.pro API Key
API_KEY = 'AlzaSyjcindTC8jO69hD_jto9xdMOMU1mkqQvKz'

BASE_URL = "https://maps.gomaps.pro/maps/api"  # Replace with the correct base URL if different

def get_user_location(lat, lng):
    """
    Reverse geocode to get the location details from coordinates using GoMaps.pro API.
    """
    url = f"{BASE_URL}/geocode/json?latlng={lat},{lng}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            return data["results"][0]
        else:
            print("No results found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_nearby_places(lat, lng, radius=50000, place_types=['restaurant', 'tourist_attraction']):
    """
    Fetch nearby places (restaurants, tourist attractions, etc.) based on location.
    """
    combined_results = []
    for place_type in place_types:
        url = f"{BASE_URL}/place/nearbysearch/json?location={lat},{lng}&keyword=tourist_attraction&radius=50000&key={API_KEY}"
        '''params = {
            'lat': lat,
            'lng': lng,
            'radius': 5000000,
            'keyword': 'tourist_attraction',
            'key': API_KEY
        }'''
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('results', [])
            combined_results.extend(results)
        else:
            print(f"Error fetching {place_type}: {response.status_code} - {response.text}")
    
    # Remove duplicates based on unique 'place_id'
    unique_results = {place['place_id']: place for place in combined_results}.values()
    return list(unique_results)

def get_place_image(photo_reference, max_width=300):
    """
    Fetch the image URL of a place using the photo reference from GoMaps.pro API.
    """
    url = f"https://maps.gomaps.pro/maps/api/place/photo"
    params = {
        'photoreference': photo_reference,
        'maxwidth': max_width,
        'key': API_KEY
    }
   
    response = requests.get(url, params=params, allow_redirects=False)
    if response.status_code == 302:
        # The API redirects to the actual image URL
        return response.headers['Location']
        print(f"Image URL: {photo_reference}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return None