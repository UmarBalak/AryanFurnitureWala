import numpy as np
from PIL import Image
import streamlit as st
from AryanFurnitureWala.furniture import detect_furniture, complementary_items
import os
import random

furniture_classes_list = [
    "bench", "chair", "couch", "potted plant", 
    "bed", "dining table", "clock", "vase"
]

# Dictionary with ranking/counts for each complementary item
complementary_items = {
    "bench": [("vase", 5), ("potted plant", 4), ("clock", 3), ("cabinet", 2), ("shelf", 1), ("sideboard", 1)],
    "chair": [("dining table", 5), ("potted plant", 4), ("vase", 3), ("desk", 2), ("shelf", 1), ("wing_chair", 1)],
    "couch": [("vase", 5), ("potted plant", 4), ("bench", 3), ("sideboard", 2), ("tv_bench", 1), ("chaise", 1)],
    "potted plant": [("bench", 5), ("couch", 4), ("dining table", 3), ("shelf", 2), ("cabinet", 1), ("desk", 1)],
    "bed": [("vase", 5), ("clock", 4), ("shelf", 3), ("cabinet", 2), ("sideboard", 1), ("sleeper", 1)],
    "dining table": [("chair", 5), ("vase", 4), ("potted plant", 3), ("sideboard", 2), ("cabinet", 1), ("bench", 1)],
    "clock": [("bench", 5), ("couch", 4), ("vase", 3), ("shelf", 2), ("desk", 1), ("tv_bench", 1)],
    "vase": [("couch", 5), ("dining table", 4), ("bench", 3), ("shelf", 2), ("desk", 1), ("sideboard", 1)]
}

IMAGE_FOLDER = '../Aryan Russia Project/furniture data'

def get_random_product_image(product_name):
    product_folder = os.path.join(IMAGE_FOLDER, product_name)
    if os.path.exists(product_folder):
        images = os.listdir(product_folder)
        if images:
            image_filename = random.choice(images)
            image_path = os.path.join(product_folder, image_filename)
            return Image.open(image_path)
    # Return a placeholder image if no images found or folder doesn't exist
    return Image.new('RGB', (200, 200), color='white')

def get_top_complementary_items(detected_items):
    item_counts = {}
    for item in detected_items:
        if item in complementary_items:
            for comp_item, count in complementary_items[item]:
                if comp_item in item_counts:
                    item_counts[comp_item] += count
                else:
                    item_counts[comp_item] = count
    
    # Remove detected items from suggestions to avoid redundancy
    for item in detected_items:
        if item in item_counts:
            del item_counts[item]

    # Sort items by count and return the top 5
    sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items[:5]]


st.title("Furniture Detector and Recommender")
uploaded_file = st.file_uploader("Upload an image of your room", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Preprocess the image
    image = image.resize((640, 480))

    # Detect furniture
    # detected_furniture = detect_furniture(image)

    # Detect furniture
    with st.spinner('Detecting furniture...'):
        detected_furniture = detect_furniture(image)

    if detected_furniture:
        st.write("Detected Furniture: ", detected_furniture)

        # Generate complementary items
        with st.spinner('Generating recommendations...'):
            top_complementary_furniture = get_top_complementary_items(detected_furniture)

        st.write("Top 5 Suggested Complementary Furniture: ", top_complementary_furniture)

        # Display images of suggested products
        st.subheader("Suggested Complementary Products:")
        for product_name in top_complementary_furniture:
            st.write(product_name.title())
            product_image = get_random_product_image(product_name)
            st.image(product_image, caption=product_name, width=480)
    else:
        st.write("No furniture detected in the image. Please try another image.")
