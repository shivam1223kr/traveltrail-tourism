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
    import random

    message = request.get_json(force=True).get("message", "").lower().strip()

    responses = {
        "greeting": [
            "Hello! 👋 I'm TripGuide AI. I can help you plan trips, choose destinations, compare hotels and suggest budgets.",
            "Hi! 🌍 Welcome to TravelTrail. Tell me where you'd like to travel or what kind of trip you enjoy.",
            "Hey! ✈️ I'm your TravelTrail trip assistant. Ask me about beaches, mountains, culture, hotels or budgets."
        ],
        "budget": [
            "For a budget-friendly trip, Jaipur and Varanasi are great choices. Jaipur is especially good for heritage, food and affordable stays.",
            "If you want to save money, consider Jaipur, Varanasi or Rishikesh. You can enjoy a good trip without a luxury budget.",
            "For a low-cost holiday, I'd suggest Jaipur or Varanasi. If you tell me your approximate budget and number of days, I can suggest a better plan."
        ],
        "beach": [
            "Goa is a popular beach destination with beaches, water activities and nightlife. November to February is generally a pleasant period to visit.",
            "If beaches are your priority, Goa is an excellent option. For a quieter experience, you could also consider coastal destinations such as Kerala.",
            "For a beach vacation, Goa is a strong choice. You can combine beaches with local food, sightseeing and water activities."
        ],
        "mountain": [
            "Manali is a great choice for a shorter mountain trip, while Ladakh is better suited to a longer high-altitude adventure.",
            "If you love mountains, Manali offers snow, valleys and adventure activities. Ladakh is ideal if you want dramatic landscapes and a more adventurous trip.",
            "For a mountain holiday, I'd compare Manali and Ladakh. Manali is easier for a shorter trip; Ladakh is better for a high-altitude experience."
        ],
        "culture": [
            "For culture and heritage, Jaipur is a fantastic option. You can explore forts, palaces, markets and traditional Rajasthani food.",
            "If you enjoy history and culture, consider Jaipur or Varanasi. Both offer very different but memorable experiences.",
            "Jaipur is a great cultural destination with forts, palaces, local markets and traditional cuisine."
        ],
        "hotel": [
            "I can help you compare hotels by price, rating and amenities. Try the Hotel Compare section and select your destination.",
            "For hotel selection, compare price, rating, location and amenities rather than choosing only by the lowest price.",
            "TravelTrail's Hotel Compare feature can help you check different providers and identify the best-value option."
        ],
        "trip": [
            "I'd be happy to help plan your trip! Tell me your destination, number of days, approximate budget and what you enjoy doing.",
            "Let's plan it step by step. Tell me whether you prefer beaches, mountains, culture, nature or adventure.",
            "For a personalized trip plan, share your destination, trip duration and budget. I can then suggest what to see and how to structure the trip."
        ],
        "thanks": [
            "You're welcome! 😊 Have a wonderful journey.",
            "Happy to help! ✈️ Enjoy planning your TravelTrail adventure.",
            "Anytime! 🌍 Let me know if you need help choosing your next destination."
        ]
    }

    if any(word in message for word in ["hello", "hi", "hey", "namaste"]):
        category = "greeting"
    elif any(word in message for word in ["thank", "thanks", "thx"]):
        category = "thanks"
    elif any(word in message for word in ["cheap", "budget", "low cost", "affordable", "money", "price"]):
        category = "budget"
    elif any(word in message for word in ["beach", "sea", "goa", "coast"]):
        category = "beach"
    elif any(word in message for word in ["mountain", "snow", "adventure", "trek", "hiking", "hill"]):
        category = "mountain"
    elif any(word in message for word in ["culture", "heritage", "history", "fort", "palace", "temple"]):
        category = "culture"
    elif any(word in message for word in ["hotel", "stay", "room", "resort", "accommodation"]):
        category = "hotel"
    elif any(word in message for word in ["trip", "plan", "itinerary", "travel", "days", "vacation", "holiday"]):
        category = "trip"
    else:
        answer = (
            "I can help with TravelTrail! 🌍 You can ask me things like: "
            '"Where should I go for a beach trip?", '
            '"Suggest a budget destination", '
            '"Which is better, Manali or Ladakh?", '
            '"Help me plan a 5-day trip", or '
            '"How can I compare hotels?"'
        )
        return jsonify({"answer": answer})

    answer = random.choice(responses[category])
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG") == "1")
