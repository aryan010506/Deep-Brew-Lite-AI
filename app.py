from flask import Flask, render_template, request
import math
from recommender import recommend_drink
from stores import stores

app = Flask(__name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    drink = None
    nearby_stores = []

    if request.method == "POST":
        profile = {
            "preferred_type": request.form["type"],
            "sweetness": int(request.form["sweetness"]),
            "caffeine": int(request.form["caffeine"]),
            "milk": True if request.form["milk"] == "yes" else False
        }

        drink = recommend_drink(profile)

        user_lat = float(request.form["lat"])
        user_lon = float(request.form["lon"])

        for store in stores:
            dist = calculate_distance(
                user_lat, user_lon,
                store["lat"], store["lon"]
            )
            nearby_stores.append({
                "name": store["name"],
                "distance": dist,
                "lat": store["lat"],
                "lon": store["lon"]
            })

        nearby_stores = sorted(nearby_stores, key=lambda x: x["distance"])

    return render_template(
        "index.html",
        drink=drink,
        stores=nearby_stores
    )

if __name__ == "__main__":
    app.run(debug=True)
