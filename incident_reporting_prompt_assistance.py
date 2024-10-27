import streamlit as st
import openai

openai.api_key = "OPEN-AI-KEY"

def generate_report(driver_behavior, vehicle_info, risk_details):
    prompt = (
        f"Create a detailed incident report based on the following information:\n"
        f"1. Dangerous behavior witnessed: {driver_behavior}\n"
        f"2. Description of the vehicle involved: {vehicle_info}\n"
        f"3. Risk or injury details: {risk_details}\n"
        f"Provide a clear and comprehensive report."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the latest chat-based model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes incident reports."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # Adjust token limit based on the desired length
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

st.title("Report Dangerous Driving Incident")

st.header("Please provide the details of the incident")
driver_behavior = st.text_input("What kind of dangerous behavior did you witness? (e.g., speeding, aggressive lane change)")
vehicle_info = st.text_input("Can you describe the vehicle involved? (make, model, color)")
risk_details = st.text_area("Was anyone at risk or injured? Provide additional details if any:")

# Submit Button and Report Generation
if st.button("Generate Incident Report"):
    if driver_behavior and vehicle_info:
        # Generate the incident report using AI
        report = generate_report(driver_behavior, vehicle_info, risk_details)
        
        # Display the AI-generated report
        st.subheader("Generated Incident Report:")
        st.text(report)
    else:
        st.error("Please fill in all required fields.")

st.info("Please provide clear and concise answers to generate an accurate incident report.")