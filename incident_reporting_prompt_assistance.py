import streamlit as st
import openai

# Initialize OpenAI API key
openai.api_key = ""

# Optional integration for real-time weather and geolocation data
def fetch_weather_data(location):
    # Placeholder function to integrate a Weather API based on location
    # Implement API call to retrieve weather conditions for added incident context
    return "clear"  # Example return

def generate_report(driver_behavior, vehicle_info, risk_details, weather_conditions, location_details, time_of_incident):
    prompt = (
        f"Generate a comprehensive traffic incident report with the following details:\n"
        f"1. Dangerous behavior observed: {driver_behavior}\n"
        f"2. Vehicle description: {vehicle_info}\n"
        f"3. Risk and injury information: {risk_details}\n"
        f"4. Weather conditions: {weather_conditions}\n"
        f"5. Location: {location_details}\n"
        f"6. Time of incident: {time_of_incident}\n"
        f"Provide a structured, concise, and informative report that highlights key incident aspects."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that writes structured and detailed traffic reports."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,  # Increased token limit for a more detailed report
        temperature=0.5  # Moderate creativity for clarity and structure
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit UI for reporting a dangerous driving incident
st.title("AI-Powered Incident Reporting")

# Step-by-step input fields for reporting process
st.header("Step 1: Describe the Incident")
driver_behavior = st.text_input("Dangerous behavior observed (e.g., speeding, reckless driving):")
vehicle_info = st.text_input("Vehicle involved (make, model, color):")
time_of_incident = st.text_input("Time of incident (e.g., 3:30 PM)")

st.header("Step 2: Risk and Injury Details")
risk_details = st.text_area("Specify if anyone was at risk or injured:")

st.header("Step 3: Environmental and Location Context")
location_details = st.text_input("Incident location (e.g., street, highway mile marker):")
# Optional: Fetch real-time weather data if location provided
if location_details:
    weather_conditions = fetch_weather_data(location_details)
else:
    weather_conditions = st.text_input("Weather conditions during incident (e.g., clear, rainy):")

# Generate Report Button
if st.button("Generate Incident Report"):
    # Verify that all required fields are filled
    if all([driver_behavior, vehicle_info, location_details, time_of_incident]):
        # Generate the incident report using OpenAI
        report = generate_report(driver_behavior, vehicle_info, risk_details, weather_conditions, location_details, time_of_incident)
        
        # Display and allow user to refine the AI-generated report
        st.subheader("Generated Incident Report Preview")
        report_content = st.text_area("Incident Report", report, height=300)
        
        st.success("Review and edit the report if needed before submission.")
    else:
        st.error("Please complete all required fields to generate a report.")

# Optional integration section for map view (placeholder for future enhancement)
st.info("Future feature: Mapping and incident tracking for identifying high-risk areas.")
