import streamlit as st
import numpy as np
import joblib

model = joblib.load("Smart_Nutrition_Prediction.pkl")
scaler = joblib.load("Scale.pkl")

labels = {
    0: "None",
    1: "Iron",
    2: "VitaminB12",
    3: "VitaminD",
    4: "Calcium"}

st.set_page_config( page_title = "Nutrition Deficiency Predictor", page_icon ="🥗",layout='wide')

st.header("🥗 Smart Nutrition Deficiency Predictor")
st.markdown("Enter your diet and lifestyle information to predict possible nutrition Deficiencies")

st.divider()


# USer - Input
st.sidebar.header("👨‍⚕ Personal Information")
age = st.sidebar.slider("Age",10,80,20)
gender = st.sidebar.selectbox("Gender",["Male","Female"])
bmi = st.sidebar.number_input("BMI",10.0,40.0,22.0)

st.sidebar.divider()

st.sidebar.header("🍽 Nutrition Intake")
iron = st.sidebar.number_input("Iron Intake (mg/day)",0.0,40.0, 0.0,help='Range: 1 - 40')#8-18 ~8 #veg
b12 = st.sidebar.number_input("Vitamin B12 Intake (mcg/day)",0.0,10.0, 0.0, help='Range: 1 - 10')#2.4 ~2 #Meat #Dairy
vitd = st.sidebar.number_input("Vitamin D Intake (mcg/day)",0.0,30.0,0.0, help='Range: 1 - 30')#15 ~10 sunlight ~ 1
cal = st.sidebar.number_input("Calcium Intake (mg/day)",200,1500,200,help='Range: 200 - 1500')#1000 ~700 dairy ~1

st.sidebar.divider()

st.sidebar.header("🥗 Food Habits")
dairy = st.sidebar.slider("Dairy servings",0,5,2)
vegetables = st.sidebar.slider("Vegetables servings",0,6,3)
meat = st.sidebar.slider("Meat serving/day",0,5,1)

st.sidebar.divider()

st.sidebar.header("🔆 LifeStyle")   
sunlight = st.sidebar.slider("Sunlight (hours/Day)",0.0,8.0,1.5)

gender_val = 1 if gender == "Male" else 0


# Page Content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Health Summary")

    st.metric("BMI", bmi)
    st.metric("Iron Intake", f"{iron} mg")
    st.metric("Vitamin D Intake", f"{vitd} mcg")

with col2:
    st.subheader("🌱 Lifestyle Overview")

    st.write("🥛 Dairy Intake")
    st.progress(dairy / 5)

    st.write("🥦 Vegetable Intake")
    st.progress(vegetables / 6)

    st.write("🔆 Sunlight Exposure")
    st.progress(sunlight / 8)


st.divider()

    
if st.button("🔎 Check My Nutrition"):
    input_data = np.array([[age, gender_val, bmi, iron, b12, vitd,
                            cal, dairy, vegetables, sunlight, meat]])

    # Prediction 
    input_scale = scaler.transform(input_data)
    pred = model.predict(input_scale)[0]
    prediction = labels[pred]
    
    deficiencies = []
    
    if prediction != "None":
        deficiencies.append(prediction)

    
    if iron < 8 and "Iron" not in deficiencies:
        deficiencies.append("Iron")

    if b12 < 2.4 and "VitaminB12" not in deficiencies:
        deficiencies.append("VitaminB12")

    if vitd < 15 and "VitaminD" not in deficiencies:
        deficiencies.append("VitaminD")

    if cal < 700 and "Calcium" not in deficiencies:
        deficiencies.append("Calcium")
        
    st.divider()


    # Result
    st.subheader("📊 Result")
    if len(deficiencies) == 0:
        st.balloons()
        st.write("🎉 No deficiency detected.")
        st.write("🏆 Excellent! Your nutrition looks balanced.")    
    else:
        st.warning("⚠ Possible deficiencies detected:")
        for d in deficiencies:
            st.write(f"• {d}")

      
    st.divider()

    # Recommentation
    st.subheader("🥗 Recommended Foods")
    if "Iron" in deficiencies:
        st.write("🩸 Increase iron-rich foods:")
        st.write("• Spinach")
        st.write("• Lentils")
        st.write("• Red meat")
        st.write("• Beans")
        st.write("• Pumpkin seeds")
        st.write("")
        st.write("")
        
    if "VitaminB12" in deficiencies:
        st.write("💊 Increase Vitamin B12 rich foods:")
        st.write("• Eggs")
        st.write("• Milk and dairy products")
        st.write("• Fish")
        st.write("• Chicken")
        st.write("• Fortified cereals")
        st.write("")
        st.write("")
        
    if "VitaminD" in deficiencies:
        st.write("☀️ Improve Vitamin D levels with:")
        st.write("• Fatty fish (salmon, tuna)")
        st.write("• Egg yolk")
        st.write("• Mushrooms")
        st.write("• Fortified milk")
        st.write("Try to get more sunlight exposure daily.☀️")
        st.write("")
        st.write("")
        
    if "Calcium" in deficiencies:
        st.write("🦴 Increase calcium rich foods:")
        st.write("• Milk")
        st.write("• Yogurt")
        st.write("• Cheese")
        st.write("• Almonds")
        st.write("• Leafy green vegetables")
        st.write("")
        st.write("")
        
    st.divider()


    # Random Tips
    import random
    tips = [
    "💧 Drink at least 2–3 liters of water daily.",
    "🥗 Include colorful vegetables in your meals.",
    "🚶 Walk at least 30 minutes every day.",
    "🌞 Morning sunlight improves Vitamin D.",
    "🥜 Nuts and seeds improve mineral intake."
    ]
    st.subheader("🎁 Daily Health Tip")
    st.info(random.choice(tips))


    
    st.divider()
    st.caption("ML Project | Smart Nutrition Deficiency Predictor | Ashna Ansari")



    

