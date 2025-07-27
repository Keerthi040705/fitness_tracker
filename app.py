import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize session state
if 'fitness_data' not in st.session_state:
    st.session_state.fitness_data = pd.DataFrame(columns=['Date', 'Height', 'Age', 'Gender', 'Weight', 'Calories', 'Steps'])

st.title("Fitness Tracker")

# --- Input Form ---
st.subheader("Enter Your Details")

# Date input (choose manually, defaults to today)
entry_date = st.date_input("Date", datetime.now())
entry_date = pd.to_datetime(entry_date)  # Convert to datetime64 for compatibility

# Basic details
height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
age = st.number_input("Age", min_value=1, max_value=120, value=25)
gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])

# Daily details
weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=60.0)
calories = st.number_input("Calories Consumed", min_value=0, max_value=10000, value=2000)
steps = st.number_input("Steps Walked", min_value=0, max_value=100000, value=5000)

# Add entry button
if st.button("Add to List"):
    new_entry = pd.DataFrame([[entry_date, height, age, gender, weight, calories, steps]],
                              columns=['Date', 'Height', 'Age', 'Gender', 'Weight', 'Calories', 'Steps'])
    st.session_state.fitness_data = pd.concat([st.session_state.fitness_data, new_entry], ignore_index=True)
    st.success("Entry added!")

# --- Display Data ---
st.subheader("Your Data")
# Ensure Date column is datetime to avoid PyArrow error
st.session_state.fitness_data['Date'] = pd.to_datetime(st.session_state.fitness_data['Date'])
st.dataframe(st.session_state.fitness_data)

# --- Analysis ---
st.subheader("Analysis")
if not st.session_state.fitness_data.empty:
    st.write("### Latest Entry")
    st.write(st.session_state.fitness_data.tail(1))

    # Monthly summary
    st.write("### Monthly Averages")
    st.session_state.fitness_data['Month'] = st.session_state.fitness_data['Date'].dt.to_period('M')
    monthly_summary = st.session_state.fitness_data.groupby('Month')[['Weight', 'Calories', 'Steps']].mean()
    st.write(monthly_summary)

    # Yearly summary
    st.write("### Yearly Averages")
    st.session_state.fitness_data['Year'] = st.session_state.fitness_data['Date'].dt.year
    yearly_summary = st.session_state.fitness_data.groupby('Year')[['Weight', 'Calories', 'Steps']].mean()
    st.write(yearly_summary)

    # --- Graph ---
    st.write("### Progress Over Time")
    fig, ax = plt.subplots(figsize=(8, 5))
    st.session_state.fitness_data = st.session_state.fitness_data.sort_values('Date')

    ax.plot(st.session_state.fitness_data['Date'], st.session_state.fitness_data['Weight'], marker='o', label='Weight (kg)')
    ax.plot(st.session_state.fitness_data['Date'], st.session_state.fitness_data['Calories'], marker='o', label='Calories')
    ax.plot(st.session_state.fitness_data['Date'], st.session_state.fitness_data['Steps'], marker='o', label='Steps')

    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title('Fitness Progress')
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("No data added yet. Enter your details above.")
