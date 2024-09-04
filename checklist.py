import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config for green theme
st.set_page_config(
    page_title="Eco-Event Scorer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for green and white theme
st.markdown("""
<style>
    .reportview-container {
        background-color: #f0f8f0;
    }
    .sidebar .sidebar-content {
        background-color: #e0f0e0;
    }
    .Widget>label {
        color: #2e7d32;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4caf50;
        border-color: #4caf50;
    }
    .stTextInput>div>div>input {
        color: #2e7d32;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #2e7d32;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 250px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -125px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

def send_email(subject, body):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = "mark.kirkpatrick@aecom.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def main():
    st.title("🌿 Eco-Event Scorer")
    
    st.markdown("""
    ## Welcome to the Eco-Event Scorer!

    In today's world, it's crucial to ensure that all events, regardless of their size, are as eco-friendly as possible. Here's why:

    1. **Environmental Impact**: Even small events can have a significant cumulative impact on the environment. By making conscious choices, we can reduce waste, energy consumption, and carbon emissions.

    2. **Resource Conservation**: Eco-friendly practices help conserve valuable resources like water and energy, contributing to long-term sustainability.

    3. **Awareness and Education**: Hosting green events raises awareness among attendees and can inspire them to adopt eco-friendly practices in their daily lives.

    4. **Cost Efficiency**: Many eco-friendly options can lead to cost savings in the long run, such as using reusable materials or energy-efficient equipment.

    5. **Reputation and Responsibility**: Demonstrating environmental responsibility can enhance your organization's reputation and appeal to environmentally conscious stakeholders.

    This tool helps you assess and improve the environmental friendliness of your events. Simply check off the measures you've implemented, add any custom eco-friendly actions, and get instant feedback on your event's sustainability score.

    Created by Mark Kirkpatrick (mark.kirkpatrick@aecom.com)
    """)

    # Initialize session state
    if 'checklist' not in st.session_state:
        st.session_state.checklist = load_checklist()
    if 'custom_measures' not in st.session_state:
        st.session_state.custom_measures = []

    # Sidebar for navigation
    page = st.sidebar.radio("Navigate", ["Checklist", "Custom Measures", "Results"])

    if page == "Checklist":
        display_checklist()
    elif page == "Custom Measures":
        display_custom_measures()
    else:
        display_results()

    # Suggestion box
    st.sidebar.markdown("---")
    st.sidebar.subheader("Feedback & Suggestions")
    suggestion = st.sidebar.text_area("Have any suggestions or found a bug? Let us know!")
    if st.sidebar.button("Send Feedback"):
        if suggestion:
            if send_email("Eco-Event Scorer Feedback", suggestion):
                st.sidebar.success("Thank you for your feedback!")
            else:
                st.sidebar.error("Failed to send feedback. Please try again later.")
        else:
            st.sidebar.warning("Please enter your feedback before sending.")

def display_checklist():
    st.header("Eco-Friendly Checklist")
    for category, items in st.session_state.checklist.items():
        st.subheader(category)
        for i, item in enumerate(items):
            key = f"{category}_{i}"
            col1, col2 = st.columns([4, 1])
            with col1:
                checked = st.checkbox(item[0], value=item[1], key=key)
            with col2:
                st.markdown(f'<div class="tooltip">ℹ️<span class="tooltiptext">{item[2]}</span></div>', unsafe_allow_html=True)
            st.session_state.checklist[category][i] = (item[0], checked, item[2])

def display_custom_measures():
    st.header("Custom Eco-Friendly Measures")
    new_measure = st.text_input("Add a custom eco-friendly measure:")
    if st.button("Add Measure"):
        if new_measure:
            st.session_state.custom_measures.append((new_measure, False))
            st.success(f"Added: {new_measure}")

    if st.session_state.custom_measures:
        st.subheader("Your Custom Measures")
        for i, (measure, checked) in enumerate(st.session_state.custom_measures):
            key = f"custom_{i}"
            st.session_state.custom_measures[i] = (measure, st.checkbox(measure, value=checked, key=key))

def display_results():
    st.header("Results")

    # Calculate score
    total_items = sum(len(items) for items in st.session_state.checklist.values()) + len(st.session_state.custom_measures)
    checked_items = sum(item[1] for items in st.session_state.checklist.values() for item in items) + sum(item[1] for item in st.session_state.custom_measures)
    score = (checked_items / total_items) * 100

    # Display score with a progress bar
    st.subheader("Your Event's Eco-Score")
    st.progress(score / 100)
    st.write(f"Score: {score:.2f}%")

    # Provide suggestions
    if score < 100:
        st.subheader("Suggestions for Improvement")
        for category, items in st.session_state.checklist.items():
            for item in items:
                if not item[1]:
                    st.write(f"- Consider implementing: {item[0]}")
                    st.write(f"  *Tip: {item[2]}*")

    # Download report
    if st.button("Download Report"):
        report = generate_report(st.session_state.checklist, st.session_state.custom_measures, score)
        st.download_button(
            label="Download Report as CSV",
            data=report,
            file_name="eco_event_report.csv",
            mime="text/csv"
        )

def load_checklist():
    return {
        "Location and Transportation": [
            ("Select a place accessible by soft mobility", False, "Choose venues near public transit or with good cycling/walking access."),
            ("Consider a shuttle service", False, "Organize shared transportation to reduce individual car use."),
            ("Collect information on participants' mode of transport", False, "This data helps in calculating the event's carbon footprint.")
        ],
        "Catering": [
            ("Choose a zero-waste provider", False, "Look for caterers who prioritize minimal packaging and composting."),
            ("Provide reusable utensils", False, "Use washable plates, cups, and cutlery instead of disposables."),
            ("Offer waste-free drinks", False, "Serve beverages in bulk containers or use refillable bottles."),
            ("Favor local, seasonal ingredients with vegetarian options", False, "This reduces transportation emissions and often has a lower environmental impact."),
            ("Provide adequate quantities to avoid waste", False, "Careful planning can significantly reduce food waste.")
        ],
        "Logistics and Equipment": [
            ("Ensure presence of recycling bins", False, "Clearly label bins for different types of waste to encourage proper disposal."),
            ("Use reusable decorations", False, "Invest in durable decorations that can be used for multiple events."),
            ("Rent or use reusable exhibition stands", False, "This reduces waste and can be more cost-effective in the long run.")
        ],
        "Hotels": [
            ("Look for eco-friendly hotels with certifications", False, "Certifications like LEED or Green Key indicate environmentally responsible practices."),
            ("Check for sustainable development charters", False, "Even without formal certifications, many hotels have their own sustainability initiatives.")
        ],
        "Communication": [
            ("Inform guests of eco-friendly event participation", False, "This raises awareness and can encourage attendees to support your initiatives."),
            ("Encourage guests to bring their own water bottle/cup", False, "This simple step can significantly reduce single-use plastic waste."),
            ("Encourage eco-friendly transportation", False, "Provide information on public transit options or organize carpooling.")
        ],
        "Carbon Footprint": [
            ("Send information to ESG team for carbon footprint assessment", False, "This helps quantify the event's environmental impact and identify areas for improvement."),
            ("Consider carbon offsetting", False, "While not a substitute for reduction efforts, offsetting can help mitigate unavoidable emissions.")
        ]
    }

def generate_report(checklist, custom_measures, score):
    data = []
    for category, items in checklist.items():
        for item in items:
            data.append({"Category": category, "Measure": item[0], "Implemented": "Yes" if item[1] else "No", "Tip": item[2]})
    
    for measure, implemented in custom_measures:
        data.append({"Category": "Custom Measures", "Measure": measure, "Implemented": "Yes" if implemented else "No", "Tip": "Custom measure"})
    
    df = pd.DataFrame(data)
    df = df.append({"Category": "Overall Score", "Measure": f"{score:.2f}%", "Implemented": "", "Tip": ""}, ignore_index=True)
    return df.to_csv(index=False)

if __name__ == "__main__":
    main()
