import requests
from PIL import Image
import streamlit as st
import os
import random
from furniture2 import get_random_product_image

st.title("Furniture Detector and Recommender")
uploaded_file = st.file_uploader("Upload an image of your room", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Preprocess the image
    image = image.resize((640, 480))

    # Save the image temporarily to send it to the FastAPI
    temp_image_path = "temp_image.jpg"
    image.save(temp_image_path)

    with st.spinner('Detecting furniture and generating recommendations...'):
        with open(temp_image_path, 'rb') as temp_file:
            files = {'file': temp_file}
            response = requests.post("http://localhost:8000/predict", files=files)

    # Delete the temporary file after processing
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    if response.status_code == 200:
        data = response.json()
        detected_furniture = data.get("detected_furniture", [])
        top_complementary_furniture = data.get("top_complementary_furniture", [])

        if detected_furniture:
            st.write("Detected Furniture: ", detected_furniture)
            st.write("Top 5 Suggested Complementary Furniture: ", top_complementary_furniture)

            st.subheader("Suggested Complementary Products:")
            for product_name in top_complementary_furniture:
                st.write(product_name.title())
                product_image = get_random_product_image(product_name)
                st.image(product_image, caption=product_name, width=200)  # Adjust width as needed
        else:
            st.write("No furniture detected in the image. Please try another image.")
    else:
        st.write("Error in detecting furniture. Please try again.")
