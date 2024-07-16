from PIL import Image
import streamlit as st
from furniture import detect_furniture, get_top_complementary_items, get_random_product_image

st.title("Furniture Detector and Recommender")
uploaded_file = st.file_uploader("Upload an image of your room", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Preprocess the image
    image = image.resize((640, 480))

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
