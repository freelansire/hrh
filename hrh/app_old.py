import streamlit as st
import openai
import pandas as pd
import numpy as np
from PIL import Image
import requests
import io



st.set_page_config(page_title="AI-Powered Logistics", layout="wide")

st.sidebar.title("Demo Features")
option = st.sidebar.radio("Select Feature", ["Automated Labeling", "Warehousing Optimization", "Logistics Route Planning"])

st.title("AI-Powered Export & Warehousing System")
st.write("This demo showcases AI solutions for labeling, warehousing, and logistics.")



if option == "Automated Labeling":
    st.header("AI-Powered Labeling System")
    
    uploaded_file = st.file_uploader("Upload a Product Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Simulated AI Label Extraction
        extracted_label = "Product: Milk | Expiry: 2025-06-30 | Weight: 1L"
        st.success(f"Extracted Label: {extracted_label}")

        # Simulated Translation
        translated_label = "Producto: Leche | Vencimiento: 30-06-2025 | Peso: 1L"
        st.info(f"Translated Label (Spanish): {translated_label}")



        if option == "Warehousing Optimization":st.header("AI-Based Warehousing Optimization")
    
    category = st.selectbox("Select Product Category", ["Frozen Goods", "Perishables", "Non-Food Items"])
    demand = st.slider("Demand Level (0 - 100)", 0, 100, 50)
    
    # AI-based Recommendation (Simplified)
    if category == "Frozen Goods":
        location = "Cold Storage Area"
    elif category == "Perishables":
        location = "Front Shelf (High Rotation)"
    else:
        location = "Back Storage"

    st.success(f"Recommended Storage Location: {location}")



if option == "Logistics Route Planning":
    st.header("AI-Based Logistics Route Optimization")

    origin = st.text_input("Enter Origin (e.g., London)")
    destination = st.text_input("Enter Destination (e.g., Paris)")

    if st.button("Find Best Route"):
        # Simulated AI Calculation
        route = f"Optimal Route: {origin} → Dover → Calais → {destination}"
        st.success(route)



