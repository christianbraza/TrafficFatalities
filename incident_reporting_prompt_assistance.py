import streamlit as st
import openai

# Initialize OpenAI API key
openai.api_key = "OPEN-AI-KEY"

# Function to generate the incident report
def generate_report(driver_behavior, vehicle_info, risk_details, weather_conditions, location_details):
    prompt = (
        f"Create a detailed traffic incident report based on the following information:\n"
        f"1. Dangerous behavior witnessed: {driver_behavior}\n"
        f"2. Description of the vehicle involved: {vehicle_info}\n"
        f"3. Risk or injury details: {risk_details}\n"
        f"4. Weather conditions at the time: {weather_conditions}\n"
        f"5. Incident location details: {location_details}\n"
        f"Provide a structured and clear report with key details emphasized."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the latest chat-based model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes detailed and structured traffic incident reports."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,  # Increased token limit for additional details
        temperature=0.6  # Moderate creativity level for clarity
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit UI for reporting a dangerous driving incident
st.title("AI-Powered Incident Reporting")

# Guided input fields
st.header("Provide Details of the Dangerous Driving Incident")
driver_behavior = st.text_input("Describe the dangerous behavior you witnessed (e.g., speeding, aggressive lane change):")
vehicle_info = st.text_input("Describe the vehicle involved (make, model, color):")
risk_details = st.text_area("Was anyone at risk or injured? Provide any additional details if relevant:")
weather_conditions = st.text_input("What were the weather conditions at the time? (e.g., clear, rainy, foggy):")
location_details = st.text_input("Provide the location of the incident (e.g., intersection name, highway mile marker):")

# Submit Button and Report Generation
if st.button("Generate Incident Report"):
    # Check that required fields are filled
    if driver_behavior and vehicle_info and weather_conditions and location_details:
        # Generate the incident report using AI
        report = generate_report(driver_behavior, vehicle_info, risk_details, weather_conditions, location_details)
        
        # Display the AI-generated report
        st.subheader("Generated Incident Report:")
        st.text_area("Incident Report", report, height=200)
    else:
        st.error("Please complete all required fields to generate a report.")

# Add additional guidance for users
st.info("Ensure that you provide specific and clear details to enhance report accuracy.")
