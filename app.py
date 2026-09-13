import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

DESTINATIONS = [
    {"id": 1, "name": "Manali", "state": "Himachal Pradesh", "tag": "Mountains & Adventure", "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80", "description": "Snow peaks, pine forests and activities around Solang Valley.", "best_for": ["adventure", "nature", "family"], "budget": "medium", "rating": 4.8, "ideal_days": "4-5 days"},
    {"id": 2, "name": "Goa", "state": "Goa", "tag": "Beaches & Nightlife", "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80", "description": "Golden beaches, Portuguese heritage and vibrant local food.", "best_for": ["beach", "couple", "friends"], "budget": "medium", "rating": 4.7, "ideal_days": "3-4 days"},
    {"id": 3, "name": "Jaipur", "state": "Rajasthan", "tag": "Heritage & Culture", "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1200&q=80", "description": "Palaces, forts and bazaars in India’s Pink City.", "best_for": ["culture", "family", "budget"], "budget": "low", "rating": 4.6, "ideal_days": "2-3 days"},
    {"id": 4, "name": "Munnar", "state": "Kerala", "tag": "Tea Hills & Nature", "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80", "description": "Rolling tea gardens, misty viewpoints and calm stays.", "best_for": ["nature", "couple", "family"], "budget": "medium", "rating": 4.9, "ideal_days": "3-4 days"},
    {"id": 5, "name": "Varanasi", "state": "Uttar Pradesh", "tag": "Spiritual Heritage", "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80", "description": "Ancient ghats, Ganga aarti and a deeply cultural experience.", "best_for": ["culture", "spiritual", "budget"], "budget": "low", "rating": 4.5, "ideal_days": "2-3 days"},
    {"id": 6, "name": "Ladakh", "state": "Ladakh", "tag": "High Altitude Adventure", "image": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1200&q=80", "description": "Dramatic Himalayan landscapes, monasteries and road trips.", "best_for": ["adventure", "nature", "friends"], "budget": "high", "rating": 4.9, "ideal_days": "5-7 days"},
]

HOTELS = {
    "Manali": [
        {"name": "Snow Valley Retreat", "provider": "MakeMyTrip", "price": 4200, "rating": 4.5, "amenities": "Breakfast, Wi-Fi, Mountain view"},
        {"name": "Himalayan Lodge", "provider": "Booking.com", "price": 3900, "rating": 4.3, "amenities": "Wi-Fi, Parking, Balcony"},
        {"name": "Pine Crest Hotel", "provider": "Goibibo", "price": 4500, "rating": 4.7, "amenities": "Breakfast, Spa, Wi-Fi"},
    ],
    "Goa": [
        {"name": "Coastal Bay Resort", "provider": "MakeMyTrip", "price": 5100, "rating": 4.6, "amenities": "Pool, Breakfast, Beach access"},
        {"name": "Palm Grove Stay", "provider": "Booking.com", "price": 4700, "rating": 4.4, "amenities": "Wi-Fi, Pool, Parking"},
        {"name": "Sunset Sands Hotel", "provider": "Goibibo", "price": 4950, "rating": 4.5, "amenities": "Breakfast, Wi-Fi, Beach access"},
    ],
    "Jaipur": [
        {"name": "Pink City Haveli", "provider": "MakeMyTrip", "price": 2600, "rating": 4.5, "amenities": "Breakfast, Wi-Fi, Heritage decor"},
        {"name": "Amber Residency", "provider": "Booking.com", "price": 2350, "rating": 4.2, "amenities": "Wi-Fi, Parking, Restaurant"},
        {"name": "Royal Orchid Inn", "provider": "Goibibo", "price": 2900, "rating": 4.6, "amenities": "Breakfast, Pool, Wi-Fi"},
    ],
}

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    """Small health endpoint for a hosting provider's uptime checks."""
    return jsonify({"status": "ok", "service": "TravelTrail"})

@app.get("/api/destinations")
def destinations():
    return jsonify(DESTINATIONS)

@app.post("/api/recommend")
def recommend():
    data = request.get_json(force=True)
    interest, budget = data.get("interest", "nature"), data.get("budget", "medium")
    scored = []
    for item in DESTINATIONS:
        score = (5 if interest in item["best_for"] else 0) + (3 if budget == item["budget"] else 0) + item["rating"]
        scored.append({**item, "match_score": round(score, 1)})
    return jsonify(sorted(scored, key=lambda x: x["match_score"], reverse=True)[:3])

@app.post("/api/hotels")
def hotels():
    city = request.get_json(force=True).get("city", "Manali")
    items = HOTELS.get(city, HOTELS["Manali"])
    best = min(items, key=lambda x: x["price"])
    return jsonify({"city": city, "hotels": sorted(items, key=lambda x: x["price"]), "best_value": best["name"]})

@app.post("/api/bookings")
def create_booking():
    data = request.get_json(force=True)
    required = ["name", "email", "destination", "checkin", "guests"]
    if not all(data.get(k) for k in required):
        return jsonify({"error": "Please complete all booking fields."}), 400
    booking_id = f"TT{datetime.now().strftime('%y%m%d%H%M%S')}"
    return jsonify({"message": "Booking request received! We will contact you shortly.", "booking_id": booking_id})

@app.post("/api/chat")
def chat():
    message = request.get_json(force=True).get("message", "").lower()
    if any(word in message for word in ["cheap", "budget", "low cost"]):
        answer = "For a budget-friendly trip, I suggest Jaipur or Varanasi. Jaipur offers heritage sites and good hotels from about ₹2,350 per night."
    elif any(word in message for word in ["beach", "goa"]):
        answer = "Goa is a great beach choice. Visit from November to February for pleasant weather. I can also compare its hotel prices for you."
    elif any(word in message for word in ["mountain", "snow", "adventure", "trek"]):
        answer = "Choose Manali for a shorter mountain trip or Ladakh for a longer high-altitude adventure. Manali suits most first-time travellers."
    elif any(word in message for word in ["hello", "hi", "help"]):
        answer = "Hello! I am TripGuide AI. Ask me about places, budgets, beaches, mountains, hotel prices or trip planning."
    else:
        answer = "I can help you find a destination. Tell me your interest such as beach, mountains, culture or adventure, plus your budget."
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG") == "1")
