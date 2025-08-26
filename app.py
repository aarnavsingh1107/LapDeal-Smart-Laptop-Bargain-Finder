
import streamlit as st
import pickle
import numpy as np
from resale import LaptopResaleCalculator   # import your OOP resale class
import requests
# Load model + categorical mappings
#https://github.com/aarnavsingh1107/LapDeal-Smart-Laptop-Bargain-Finder/blob/main/cat_mappings.pkl
url_model = "https://raw.githubusercontent.com/aarnavsingh1107/LapDeal-Smart-Laptop-Bargain-Finder/main/laptop_price_model.pkl"
url_mappings = "https://raw.githubusercontent.com/aarnavsingh1107/LapDeal-Smart-Laptop-Bargain-Finder/main/cat_mappings.pkl"

with open("laptop_price_model.pkl", "wb") as f:
    f.write(requests.get(url_model).content)

with open("cat_mappings.pkl", "wb") as f:
    f.write(requests.get(url_mappings).content)

# Now load from local files
model = pickle.load(open("laptop_price_model.pkl", "rb"))
mappings = pickle.load(open("cat_mappings.pkl", "rb"))

import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

add_bg_from_local("/Users/aarnavsingh/LaptopBargainer/Notion Page Cover.jpeg")

st.title("💻 LapDeal – Smart Laptop Bargain Finder")
st.write("Predict the price of a laptop and estimate its resale value based on usage & condition.")

# ----- Laptop Specs -----
company = st.selectbox("Company", list(mappings["Company"].keys()))
typename = st.selectbox("Type Name", list(mappings["TypeName"].keys()))
cpu_brand = st.selectbox("CPU Brand", list(mappings["Cpu_brand"].keys()))
gpu_brand = st.selectbox("GPU Brand", list(mappings["Gpu_brand"].keys()))
opsys = st.selectbox("Operating System", list(mappings["OpSys"].keys()))

ram = st.number_input("RAM (GB)", min_value=2, max_value=64, value=8)
weight = st.number_input("Weight (Kg)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
inches = st.number_input("Screen Size (Inches)", min_value=10.0, max_value=20.0, value=15.6, step=0.1)
has_ssd = st.radio("Has SSD?", [0, 1], index=1, format_func=lambda x: "Yes" if x == 1 else "No")
total_memory = st.number_input("Total Memory (GB)", min_value=128, max_value=2048, value=512, step=128)

# ----- Encode categorical -----
company_code = mappings["Company"][company]
typename_code = mappings["TypeName"][typename]
cpu_code = mappings["Cpu_brand"][cpu_brand]
gpu_code = mappings["Gpu_brand"][gpu_brand]
opsys_code = mappings["OpSys"][opsys]

input_data = np.array([[company_code, typename_code, ram, weight, inches,
                        cpu_code, gpu_code, opsys_code, has_ssd, total_memory]])

# ----- Extra resale inputs -----
years = st.slider("Years of Usage", min_value=0, max_value=10, value=2)
condition = st.selectbox("Condition", ["Excellent", "Good", "Average", "Poor"])

# ----- Prediction -----
if st.button("💰 Predict Price & Resale"):
    raw_prediction = model.predict(input_data)[0]

    # Convert log1p prediction back to actual price
    base_price = float(np.expm1(raw_prediction))  
    
    resale_calc = LaptopResaleCalculator(base_price)
    resale_price = resale_calc.calculate(years, condition)

    #st.success(f"Predicted Laptop Price (New): ₹{int(base_price)}")
    resale_price=resale_price*102
    st.info(f"Estimated Resale Price after {years} year(s) ({condition}): ₹{int(resale_price)}")
