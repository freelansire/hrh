import streamlit as st
import numpy as np
from PIL import Image
import pytesseract
from googletrans import Translator
from deep_translator import GoogleTranslator
from sklearn.cluster import KMeans
import requests



st.set_page_config(page_title="HRH Logistics", layout="wide")

st.sidebar.title("Features")
option = st.sidebar.radio("Select Feature", ["Automated Labeling and Translation", "Warehousing Optimization", "Logistics Route Planning"])

st.title("HRH AI-Powered Export & Warehousing System")
st.write("AI solutions for labeling, warehousing, and logistics.")



API_KEY = "helloworld"  # Free tier OCR.space API key

# Function to extract text from image using OCR.space API
def extract_text_from_image(image):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": API_KEY,
        "language": "eng",
        "isOverlayRequired": False
    }
    files = {"file": image}
    
    response = requests.post(url, files=files, data=payload)
    result = response.json()
    
    if "ParsedResults" in result:
        return result["ParsedResults"][0]["ParsedText"]
    else:
        return "Error: Could not extract text."

# Function to translate text
def translate_text(text, target_language):
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)

# Streamlit UI
if st.title("AI-Based Labelling and Transalation"):
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Language selection
languages = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
}
selected_language = st.selectbox("Select Target Language", list(languages.keys()))

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    extracted_text = extract_text_from_image(uploaded_file)
    st.subheader("Extracted Text:")
    st.write(extracted_text)

    if extracted_text and extracted_text != "Error: Could not extract text.":
        translated_text = translate_text(extracted_text, languages[selected_language])
        st.subheader("Translated Text:")
        st.write(translated_text)



elif option == "Warehousing Optimization":
    st.header("AI-Based Warehousing Optimization")
    
    # Step 1: Select Product Category
    category = st.selectbox("Select Product Category", ["Frozen Goods", "Perishables", "Non-Food Items"])
    
    # Step 2: Select Product Details
    volume = st.number_input("Enter Product Volume (in cubic meters)", min_value=0.01, value=0.5)
    weight = st.number_input("Enter Product Weight (in kilograms)", min_value=0.1, value=10.0)
    shelf_life = st.slider("Select Shelf Life (in days)", min_value=1, max_value=365, value=30)
    
    # Step 3: Demand Slider for space allocation
    demand = st.slider("Demand Level (0 - 100)", 0, 100, 50)
    
    # Warehouse Zones (with additional features like temperature sensitivity, space optimization)
    warehouse_zones = [
        {"zone": "Cold Storage", "temperature": "Low", "space_factor": 0.8},
        {"zone": "High Rotation Area", "temperature": "Room Temp", "space_factor": 1.2},
        {"zone": "Standard Shelving", "temperature": "Room Temp", "space_factor": 1.0},
        {"zone": "Overflow Storage", "temperature": "Room Temp", "space_factor": 0.5},
    ]
    
    # Simulating AI model: Product categorization and demand prediction
    # Including product volume, weight, and shelf life into clustering
    features = np.array([[volume, weight, shelf_life, demand]])  # Example feature set
    kmeans = KMeans(n_clusters=4, random_state=42)
    
    # Example data for clustering (volume, weight, shelf life, demand)
    demand_data = np.array([[0.1, 2, 7, 10], [0.5, 10, 30, 50], [1.2, 20, 90, 100], [0.3, 5, 15, 30], [0.8, 15, 60, 70]])
    kmeans.fit(demand_data)

    # Step 4: Predict optimal storage based on clustering
    cluster_prediction = kmeans.predict(features)
    cluster_id = cluster_prediction[0]

    # Step 5: Assign optimal warehouse zone
    selected_zone = warehouse_zones[cluster_id]
    
    st.success(f"Recommended Storage Location: {selected_zone['zone']}")
    st.info(f"Zone Temperature: {selected_zone['temperature']} | Space Efficiency Factor: {selected_zone['space_factor']}")

    # Display additional information on storage optimization based on product characteristics
    st.write(f"Product Volume: {volume} cubic meters")
    st.write(f"Product Weight: {weight} kg")
    st.write(f"Shelf Life: {shelf_life} days")

    
    # Optional: Display suggestions based on shelf life or temperature sensitivity
    if category == "Frozen Goods" and selected_zone["temperature"] != "Low":
        st.warning("Frozen goods should be stored in Cold Storage to maintain quality.")
    elif category == "Perishables" and shelf_life < 30:
        st.warning("Consider storing perishables with short shelf life in High Rotation Area.")




# import googlemaps

# # Initialize Google Maps API
# gmaps = googlemaps.Client(key="AIzaSyD5u__9Aq77-7q4hrGp3glsxbfmuLZRXGY")

# if option == "Logistics Route Planning":
#     st.header("AI-Based Logistics Route Optimization")

#     origin = st.text_input("Enter Origin (e.g., London)")
#     destination = st.text_input("Enter Destination (e.g., Paris)")

#     if st.button("Find Best Route"):
#         try:
#             directions = gmaps.directions(origin, destination, mode="driving")
#             route = directions[0]["legs"][0]

#             distance = route["distance"]["text"]
#             duration = route["duration"]["text"]
#             start_address = route["start_address"]
#             end_address = route["end_address"]

#             st.success(f"Optimal Route: {start_address} → {end_address}")
#             st.info(f"Distance: {distance} | Estimated Time: {duration}")
#         except:
#             st.error("Invalid locations. Please enter valid city names.")



import googlemaps
from geopy.distance import geodesic  # To calculate maritime distances

# Initialize Google Maps API
gmaps = googlemaps.Client(key="AIzaSyD5u__9Aq77-7q4hrGp3glsxbfmuLZRXGY")

if option == "Logistics Route Planning":
    st.header("AI-Based Logistics Route Optimization")
    
    origin = st.text_input("Enter Origin (e.g., London)")
    destination = st.text_input("Enter Destination (e.g., Dublin)")

    if st.button("Find Best Route"):
        try:
            # Get driving route using Google Maps API
            directions = gmaps.directions(origin, destination, mode="driving")
            route = directions[0]["legs"][0]

            # Fetch the road-based route details
            distance = route["distance"]["text"]
            duration = route["duration"]["text"]
            start_address = route["start_address"]
            end_address = route["end_address"]

            # For shipping, calculate the maritime route (e.g., using geodesic)
            # Using approximate coordinates for ports (this would need real data)
            origin_coords = (40.7128, -74.0060)  # Example: Port of New York
            dest_coords = (34.0522, -118.2437)   # Example: Port of Los Angeles
            shipping_distance = geodesic(origin_coords, dest_coords).kilometers

            st.success(f"Optimal Route: {start_address} → {end_address}")
            st.info(f"Road Distance: {distance} | Estimated Time: {duration}")
            st.info(f"Shipping Distance (via sea): {shipping_distance:.2f} km")

            # For actual shipping lane data, integrate MarineTraffic API or other data sources here

        except Exception as e:
            st.error(f"Error: {str(e)}")
