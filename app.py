import os
from datetime import datetime
from flask import Flask, abort, jsonify, render_template, request

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
    "Munnar": [
        {"name": "Tea Valley Retreat", "provider": "MakeMyTrip", "price": 3800, "rating": 4.5, "amenities": "Breakfast, Valley view, Wi-Fi"},
        {"name": "Misty Hills Stay", "provider": "Booking.com", "price": 3400, "rating": 4.3, "amenities": "Wi-Fi, Parking, Garden"},
        {"name": "Cardamom County", "provider": "Goibibo", "price": 4200, "rating": 4.6, "amenities": "Breakfast, Pool, Tea estate view"},
    ],
    "Varanasi": [
        {"name": "Ganga View Residency", "provider": "MakeMyTrip", "price": 3200, "rating": 4.4, "amenities": "Breakfast, Wi-Fi, River view"},
        {"name": "Kashi Heritage Inn", "provider": "Booking.com", "price": 2800, "rating": 4.2, "amenities": "Wi-Fi, Restaurant, Airport transfer"},
        {"name": "Assi Ghat Retreat", "provider": "Goibibo", "price": 3500, "rating": 4.5, "amenities": "Breakfast, Wi-Fi, Ghat access"},
    ],
    "Ladakh": [
        {"name": "Himalayan Haven", "provider": "MakeMyTrip", "price": 4600, "rating": 4.5, "amenities": "Breakfast, Wi-Fi, Mountain view"},
        {"name": "Leh Valley Camp", "provider": "Booking.com", "price": 4100, "rating": 4.3, "amenities": "Parking, Restaurant, Bonfire"},
        {"name": "Indus View Hotel", "provider": "Goibibo", "price": 4900, "rating": 4.6, "amenities": "Breakfast, Heating, Airport transfer"},
    ],
}

# Curated destination data for the detail-page demo. Distances are approximate road distances.
DESTINATION_GUIDES = {
    "goa": {
        "name": "Goa", "state": "Goa, India", "tag": "Beaches, heritage & nightlife",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1800&q=85",
        "intro": "Goa combines palm-lined beaches, Portuguese-era neighbourhoods, seafood and relaxed coastal stays. Plan 3 to 5 days to balance North Goa's energy with South Goa's quieter beaches.",
        "best_time": "November to February for pleasant beach weather", "ideal_days": "3–5 days",
        "language": "Konkani, Marathi, Hindi and English", "currency": "Indian Rupee (₹)",
        "places": [
            {"name": "Baga & Calangute", "type": "North Goa beaches", "detail": "Popular for water sports, cafés, beach shacks and a lively evening scene."},
            {"name": "Fort Aguada", "type": "Heritage viewpoint", "detail": "A 17th-century fort with sweeping views of the Arabian Sea."},
            {"name": "Fontainhas, Panaji", "type": "Latin Quarter", "detail": "Walk colourful Portuguese-style lanes, galleries and small cafés."},
            {"name": "Palolem Beach", "type": "South Goa beach", "detail": "A scenic crescent beach suited to a slower day by the sea."},
            {"name": "Dudhsagar Falls", "type": "Nature excursion", "detail": "A dramatic monsoon-fed waterfall. Confirm seasonal access before leaving."},
            {"name": "Basilica of Bom Jesus", "type": "Heritage landmark", "detail": "One of Goa's best-known churches in Old Goa."},
        ],
        "foods": [["Goan fish curry rice", "A tangy coconut-based curry, often made with local fish."], ["Prawn balchão", "Spicy, pickled prawn preparation with a bold Goan flavour."], ["Xacuti", "A roasted-spice and coconut curry."], ["Bebinca", "A layered Goan dessert traditionally enjoyed after meals."]],
        "travel": [["Goa International Airport (Dabolim)", "to Panaji", "about 28 km · 45–60 min by road"], ["Manohar International Airport (Mopa)", "to Candolim", "about 31 km · 50–75 min by road"], ["Karmali Railway Station", "to Panaji", "about 12 km · 25–35 min by road"], ["Madgaon Railway Station", "to Palolem", "about 38 km · 60–75 min by road"]],
        "tips": ["Use app cabs or pre-agreed taxi fares for longer transfers.", "Carry sunscreen, water and modest cover-ups for churches and heritage sites.", "Ask about safety equipment and weather before booking water sports.", "Prices and travel times vary by season, traffic and pickup point."],
    }
    ,"manali": {
        "name":"Manali", "state":"Himachal Pradesh, India", "tag":"Mountains, snow & adventure", "image":"https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1800&q=85", "intro":"Manali is a Himalayan hill station known for pine forests, snowy viewpoints, riverside cafés and outdoor adventures around Solang Valley.", "best_time":"March to June for pleasant weather; December to February for snow", "ideal_days":"4–5 days", "language":"Hindi, English and Himachali dialects", "currency":"Indian Rupee (₹)",
        "places":[{"name":"Solang Valley","type":"Adventure valley","detail":"A popular base for seasonal snow activities, gondola rides and mountain views."},{"name":"Hadimba Temple","type":"Wooden temple","detail":"A serene pagoda-style temple surrounded by cedar forest."},{"name":"Old Manali","type":"Cafés & local lanes","detail":"Walk small streets with cafés, craft shops and riverside spots."},{"name":"Atal Tunnel","type":"Scenic drive","detail":"A high-altitude engineering landmark on the route towards Lahaul."},{"name":"Mall Road","type":"Town centre","detail":"Browse local shops, bakeries and evening street food."},{"name":"Jogini Waterfall","type":"Short trek","detail":"A scenic walk from the Vashisht side with waterfall views."}],
        "foods":[["Siddu","A steamed local bread, often served with ghee or chutney."],["Trout fish","A regional speciality available at many local restaurants."],["Dham","A traditional Himachali meal with rice, lentils and curries."],["Mittha","A sweet rice preparation with nuts and raisins."]],
        "travel":[["Bhuntar Airport","to Manali","about 50 km · 1.5–2 hr by road"],["Chandigarh Airport","to Manali","about 310 km · 8–10 hr by road"],["Joginder Nagar Railway Station","to Manali","about 160 km · 5–6 hr by road"],["Chandigarh Railway Station","to Manali","about 305 km · 8–10 hr by road"]],
        "tips":["Carry warm layers even in summer evenings.","Confirm road and weather conditions before high-altitude excursions.","Book snow activities only with verified operators.","Mountain travel times can change due to traffic and weather."]
    },
    "jaipur": {
        "name":"Jaipur", "state":"Rajasthan, India", "tag":"Heritage, forts & culture", "image":"https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1800&q=85", "intro":"Jaipur, the Pink City, offers royal forts, ornate palaces, busy bazaars and bold Rajasthani food in an easy city-break itinerary.", "best_time":"October to March for cooler sightseeing weather", "ideal_days":"2–3 days", "language":"Hindi, English and Rajasthani dialects", "currency":"Indian Rupee (₹)",
        "places":[{"name":"Amber Fort","type":"Hill fort","detail":"A grand fort complex with courtyards, mirrored halls and panoramic city views."},{"name":"Hawa Mahal","type":"City landmark","detail":"The iconic Palace of Winds façade overlooking the old city."},{"name":"City Palace","type":"Royal residence","detail":"Museums, courtyards and architecture in central Jaipur."},{"name":"Jantar Mantar","type":"Astronomical observatory","detail":"Historic outdoor instruments beside the City Palace."},{"name":"Nahargarh Fort","type":"Sunset viewpoint","detail":"A hilltop fort known for views over Jaipur."},{"name":"Johari Bazaar","type":"Local market","detail":"Browse jewellery, textiles and traditional crafts."}],
        "foods":[["Dal baati churma","The signature Rajasthani combination of baked wheat dumplings, lentils and a sweet side."],["Laal maas","A spicy traditional mutton curry."],["Pyaaz kachori","A crisp snack filled with spiced onion."],["Ghevar","A disc-shaped dessert popular in Rajasthan."]],
        "travel":[["Jaipur International Airport","to Hawa Mahal","about 12 km · 30–45 min by road"],["Jaipur Junction","to City Palace","about 5 km · 20–30 min by road"],["Jaipur Junction","to Amber Fort","about 13 km · 35–50 min by road"],["Jaipur International Airport","to Amber Fort","about 25 km · 50–70 min by road"]],
        "tips":["Start major forts early to avoid crowds and midday heat.","Wear comfortable shoes for fort steps and uneven paths.","Agree on auto-rickshaw fares or use a metered/app cab.","Keep water with you when sightseeing in warmer months."]
    },
    "munnar": {
        "name":"Munnar", "state":"Kerala, India", "tag":"Tea hills, waterfalls & nature", "image":"https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1800&q=85", "intro":"Munnar is a calm Western Ghats escape with rolling tea estates, misty viewpoints, waterfalls and wildlife-rich landscapes.", "best_time":"September to March for clear views and comfortable weather", "ideal_days":"3–4 days", "language":"Malayalam, Tamil, Hindi and English", "currency":"Indian Rupee (₹)",
        "places":[{"name":"Eravikulam National Park","type":"Wildlife reserve","detail":"Known for high grasslands and the endangered Nilgiri tahr."},{"name":"Tea Museum","type":"Tea heritage","detail":"Learn about the region's tea-growing history and processing."},{"name":"Mattupetty Dam","type":"Lake & viewpoints","detail":"A reservoir surrounded by hills, often included on local tours."},{"name":"Top Station","type":"Mountain viewpoint","detail":"A high viewpoint with valley scenery on clear days."},{"name":"Attukad Waterfalls","type":"Waterfall","detail":"A scenic cascade surrounded by forested slopes."},{"name":"Kolukkumalai","type":"Sunrise excursion","detail":"A high-altitude tea estate route best planned with a local operator."}],
        "foods":[["Kerala sadya","A vegetarian feast served on a banana leaf."],["Appam with stew","Soft rice pancakes served with a mild coconut curry."],["Puttu and kadala curry","Steamed rice cake with black chickpea curry."],["Fresh cardamom tea","A warming local tea choice after sightseeing."]],
        "travel":[["Cochin International Airport","to Munnar","about 110 km · 3.5–4.5 hr by road"],["Aluva Railway Station","to Munnar","about 110 km · 3.5–4.5 hr by road"],["Ernakulam Junction","to Munnar","about 130 km · 4–5 hr by road"],["Cochin International Airport","to Mattupetty","about 125 km · 4–5 hr by road"]],
        "tips":["Keep a light rain jacket because showers can arrive quickly.","Choose a stay near town if you prefer shorter transfers.","Start viewpoint trips early for better visibility.","Use a local driver for winding hill roads and remote viewpoints."]
    },
    "varanasi": {
        "name":"Varanasi", "state":"Uttar Pradesh, India", "tag":"Spiritual heritage & ghats", "image":"https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1800&q=85", "intro":"Varanasi is one of India's oldest living cities, centred on the Ganges ghats, morning boat rides, temples, music and the evening Ganga Aarti.", "best_time":"October to March for cooler walking weather", "ideal_days":"2–3 days", "language":"Hindi, Bhojpuri and English", "currency":"Indian Rupee (₹)",
        "places":[{"name":"Dashashwamedh Ghat","type":"Evening Aarti","detail":"A popular place to observe the Ganga Aarti from the ghat or a boat."},{"name":"Assi Ghat","type":"Riverside walk","detail":"A calmer southern ghat with cafés and morning activity."},{"name":"Kashi Vishwanath Temple","type":"Temple area","detail":"A major spiritual landmark. Check current entry guidance before visiting."},{"name":"Sarnath","type":"Buddhist heritage","detail":"A short excursion with stupas, museums and historical sites."},{"name":"Manikarnika Ghat","type":"Cultural landmark","detail":"An important riverside ghat; visitors should remain respectful and discreet."},{"name":"Banaras Hindu University","type":"Campus & temple","detail":"A large campus area with the New Vishwanath Temple."}],
        "foods":[["Kachori sabzi","A popular breakfast of fried bread with spiced potato curry."],["Banarasi paan","A famous after-meal betel-leaf preparation."],["Malaiyyo","A seasonal winter milk foam dessert."],["Lassi","Thick, sweet yoghurt drink often served in earthen cups."]],
        "travel":[["Lal Bahadur Shastri Airport","to Dashashwamedh Ghat","about 25 km · 60–90 min by road"],["Varanasi Junction","to Dashashwamedh Ghat","about 5 km · 20–35 min by road"],["Banaras Railway Station","to Assi Ghat","about 8 km · 30–45 min by road"],["Varanasi Junction","to Sarnath","about 10 km · 30–45 min by road"]],
        "tips":["Use a licensed boat operator and agree on the route and price beforehand.","The old city has narrow lanes, so walk where possible.","Dress respectfully near temples and ghats.","Allow extra time around Aarti and festival evenings."]
    },
    "ladakh": {
        "name":"Ladakh", "state":"Ladakh, India", "tag":"High-altitude roads & monasteries", "image":"https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1800&q=85", "intro":"Ladakh offers dramatic high-altitude landscapes, clear skies, Buddhist monasteries and unforgettable road journeys. Plan slowly to acclimatise safely.", "best_time":"May to September for most road access and sightseeing", "ideal_days":"5–7 days", "language":"Ladakhi, Hindi and English", "currency":"Indian Rupee (₹)",
        "places":[{"name":"Pangong Lake","type":"High-altitude lake","detail":"A striking lake best visited after acclimatisation and with weather-aware planning."},{"name":"Nubra Valley","type":"Sand dunes & valley","detail":"Known for dramatic landscapes, villages and Hunder's sand dunes."},{"name":"Shanti Stupa","type":"Leh viewpoint","detail":"A white-domed stupa with broad views of Leh."},{"name":"Leh Palace","type":"Historic palace","detail":"A former royal residence above the old town."},{"name":"Hemis Monastery","type":"Buddhist monastery","detail":"A major Ladakhi monastery with a museum and mountain setting."},{"name":"Magnetic Hill","type":"Roadside attraction","detail":"A popular stop on the Leh–Kargil road."}],
        "foods":[["Thukpa","A warming noodle soup, especially welcome in cold weather."],["Momos","Steamed dumplings with vegetarian or meat fillings."],["Skyu","A traditional Ladakhi pasta stew."],["Butter tea","A salty, high-altitude tea served in many local homes and cafés."]],
        "travel":[["Kushok Bakula Rimpochee Airport","to Leh Market","about 4 km · 15–20 min by road"],["Kushok Bakula Rimpochee Airport","to Shanti Stupa","about 6 km · 20–30 min by road"],["Leh bus stand","to Leh Palace","about 2 km · 10–15 min by road"],["Leh","to Pangong Lake","about 160 km · 5–6 hr by road"]],
        "tips":["Rest and hydrate for the first 24–48 hours to acclimatise.","Discuss altitude risks with a clinician if you have health concerns.","Carry layers, sun protection and basic medicines.","Confirm permits, road conditions and fuel availability before remote trips."]
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/destination/<slug>")
def destination_detail(slug):
    guide = DESTINATION_GUIDES.get(slug.lower())
    if not guide:
        abort(404)
    hotels = sorted(HOTELS.get(guide["name"], []), key=lambda hotel: hotel["price"])
    return render_template("destination.html", guide=guide, hotels=hotels)

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
