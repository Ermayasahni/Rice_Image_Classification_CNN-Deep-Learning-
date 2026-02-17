import streamlit as st
import numpy as np
from keras.models import load_model
from PIL import Image
from database import (create_db,create_table,save_prediction,get_predictions)

# Create database & table once
# create_db()
# create_table()

# Load trained CNN model
model = load_model("rice_cnn_model.h5")

# Class labels
class_names = ["Arborio", "Basmati", "Ipsala", "Jasmine", "Karacadag"]

def predict(image):
    # Convert to grayscale
    img = image.convert("L")
    
    # Resize
    img = img.resize((200, 200))
    
    # Convert to array & normalize
    img_array = np.array(img) / 255.0
    
    # Add channel & batch dimensions
    img_array = img_array.reshape(1, 200, 200, 1)

    # Predict
    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    
    return class_names[class_index]

# Page title
st.title("🌾 Rice Grain Classification using CNN")
st.markdown("Upload a rice grain image to predict its type.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a rice image...",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Check Result"):
        result = predict(image)
        st.session_state.result = result
        save_prediction(result, uploaded_file.name)

if "result" in st.session_state:
    st.success(f"✅ Predicted Rice Type: **{st.session_state.result}**")

        
if st.checkbox("Show Prediction History"):
    data = get_predictions()

    if data:
        st.write("### 📊 Prediction History")
        st.table(data)


