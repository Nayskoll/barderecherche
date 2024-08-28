from flask import Flask, request, jsonify, send_file
import googlemaps
import folium
from geopy.geocoders import Nominatim
from statistics import mean
import os

app = Flask(__name__)

API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=API_KEY)
geolocator = Nominatim(user_agent="my_app")


def get_coordinates(address):
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude) if location else None


def get_nearby_bars(locations, num_bars=10):
    all_bars = []
    for loc in locations:
        places_result = gmaps.places_nearby(
            location=loc,
            rank_by='distance',
            type='bar',
            keyword='bar'
        )
        all_bars.extend(places_result['results'])

    sorted_bars = sorted(all_bars, key=lambda x: mean([
        gmaps.distance_matrix(loc, (x['geometry']['location']['lat'], x['geometry']['location']['lng']))['rows'][0][
            'elements'][0]['distance']['value']
        for loc in locations
    ]))

    return sorted_bars[:num_bars]


def create_map(locations, bars):
    center_lat = mean([loc[0] for loc in locations])
    center_lon = mean([loc[1] for loc in locations])

    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    for i, loc in enumerate(locations, 1):
        folium.Marker(
            loc,
            popup=f"Adresse {i}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    for i, bar in enumerate(bars, 1):
        place_details = gmaps.place(bar['place_id'])['result']
        rating = place_details.get('rating', 'N/A')
        reviews = place_details.get('user_ratings_total', 'N/A')
        description = place_details.get('editorial_summary', {}).get('overview', 'Pas de description disponible')

        popup_content = f"""
        <div style="font-family: Arial, sans-serif; font-size: 14px; width: 250px;">
            <h3 style="margin-bottom: 5px;">{bar['name']}</h3>
            <p style="margin-top: 0;"><strong>Note :</strong> {rating}/5 ({reviews} avis)</p>
            <p><strong>Adresse :</strong> {bar.get('vicinity', 'Non disponible')}</p>
            <p><strong>Description :</strong> {description}</p>
        </div>
        """

        folium.Marker(
            [bar['geometry']['location']['lat'], bar['geometry']['location']['lng']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='blue', icon='beer', prefix='fa')
        ).add_to(m)

    for i, loc in enumerate(locations, 1):
        for j, bar in enumerate(bars, 1):
            route = gmaps.directions(loc,
                                     (bar['geometry']['location']['lat'], bar['geometry']['location']['lng']),
                                     mode="walking")
            if route:
                path = [step['start_location'] for step in route[0]['legs'][0]['steps']]
                path.append(route[0]['legs'][0]['steps'][-1]['end_location'])
                folium.PolyLine(
                    locations=[(p['lat'], p['lng']) for p in path],
                    color=f"hsl({(i - 1) * 360 // len(locations)}, 50%, 50%)",
                    weight=2,
                    opacity=0.8
                ).add_to(m)

    return m


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/generate_map', methods=['POST'])
def generate_map():
    data = request.json
    addresses = data['addresses']

    coordinates = [get_coordinates(addr) for addr in addresses if get_coordinates(addr)]

    if coordinates:
        nearby_bars = get_nearby_bars(coordinates)
        if nearby_bars:
            map = create_map(coordinates, nearby_bars)
            map.save("bars_map.html")
            return jsonify({
                "status": "success",
                "message": "Carte générée avec succès",
                "bars": [{"name": bar['name'], "vicinity": bar.get('vicinity', 'Adresse non disponible')} for bar in
                         nearby_bars]
            })
        else:
            return jsonify({"status": "error", "message": "Impossible de trouver des bars à proximité"})
    else:
        return jsonify({"status": "error", "message": "Aucune adresse valide n'a été entrée"})


@app.route('/get_map')
def get_map():
    return send_file('bars_map.html')


if __name__ == '__main__':
    app.run(debug=True)