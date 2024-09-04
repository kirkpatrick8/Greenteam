import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Set page config for green theme
st.set_page_config(page_title="Corporate Eco-Event Scorer", page_icon="🌿", layout="wide")

# Custom CSS for green and white theme with icons
st.markdown("""
<style>
    .reportview-container { background-color: #f0f8f0; }
    .sidebar .sidebar-content { background-color: #e0f0e0; }
    .Widget>label { color: #2e7d32; }
    .stButton>button { color: #ffffff; background-color: #4caf50; border-color: #4caf50; }
    .stTextInput>div>div>input { color: #2e7d32; }
    .tooltip { position: relative; display: inline-block; border-bottom: 1px dotted #2e7d32; }
    .tooltip .tooltiptext {
        visibility: hidden; width: 250px; background-color: #555; color: #fff; text-align: center;
        border-radius: 6px; padding: 5px; position: absolute; z-index: 1; bottom: 125%; left: 50%;
        margin-left: -125px; opacity: 0; transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
    .icon { font-size: 1.5em; margin-right: 10px; }
    .implemented { color: #4caf50; }
    .not-implemented { color: #f44336; }
    .not-applicable { color: #9e9e9e; }
</style>
""", unsafe_allow_html=True)

# Load and save functions for progress tracking
def load_progress():
    try:
        with open("progress.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_progress(data):
    with open("progress.json", "w") as f:
        json.dump(data, f)

# Initialize session state
if 'progress' not in st.session_state:
    st.session_state.progress = load_progress()

def main():
    st.title("🌿 Corporate Eco-Event Scorer")
    
    st.markdown("""
    Welcome to the Corporate Eco-Event Scorer! This tool helps you assess and improve the environmental 
    friendliness of your corporate events. Select your event type, check off the measures you've implemented, 
    and get instant feedback on your event's sustainability score.

    Created by Mark Kirkpatrick (mark.kirkpatrick@aecom.com)
    """)

    # Event Type Selection
    event_types = [
        "Conference or Seminar",
        "Board Meeting",
        "Team Building Event",
        "Product Launch",
        "Annual General Meeting",
        "Trade Show or Exhibition",
        "Corporate Party or Celebration",
        "Other Corporate Event"
    ]
    selected_event_type = st.selectbox("Select your corporate event type:", event_types)

    # Unique identifier for the event (you might want to add more fields for a real unique identifier)
    event_date = st.date_input("Event Date")
    event_id = f"{selected_event_type}_{event_date}"

    # Load previous progress if it exists
    if event_id in st.session_state.progress:
        checklist = st.session_state.progress[event_id]['checklist']
        custom_measures = st.session_state.progress[event_id]['custom_measures']
    else:
        checklist = load_checklist()
        custom_measures = []

    # Sidebar for navigation
    page = st.sidebar.radio("Navigate", ["Checklist", "Custom Measures", "Results", "Eco-Tips", "Resources"])

    if page == "Checklist":
        checklist = display_checklist(checklist)
    elif page == "Custom Measures":
        custom_measures = display_custom_measures(custom_measures)
    elif page == "Results":
        display_results(checklist, custom_measures, selected_event_type)
    elif page == "Eco-Tips":
        display_eco_tips()
    else:
        display_resources()

    # Save progress
    st.session_state.progress[event_id] = {
        'checklist': checklist,
        'custom_measures': custom_measures,
        'date': str(datetime.now())
    }
    save_progress(st.session_state.progress)

    # Contact information
    st.sidebar.markdown("---")
    st.sidebar.subheader("Feedback & Suggestions")
    st.sidebar.markdown("""
    If you have any suggestions or feedback, please email Mark Kirkpatrick at mark.kirkpatrick@aecom.com.
    """)

def display_checklist(checklist):
    st.header("Eco-Friendly Checklist")
    for category, items in checklist.items():
        st.subheader(category)
        for i, item in enumerate(items):
            key = f"{category}_{i}"
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"{item[0]} <div class='tooltip'>ℹ️<span class='tooltiptext'>{item[3]}</span></div>", unsafe_allow_html=True)
            with col2:
                implemented = st.checkbox("Implemented", value=item[1], key=f"{key}_implemented")
            with col3:
                not_applicable = st.checkbox("N/A", value=item[2], key=f"{key}_na")
            
            # Visual feedback
            if implemented:
                st.markdown('<span class="icon implemented">✔️</span>', unsafe_allow_html=True)
            elif not_applicable:
                st.markdown('<span class="icon not-applicable">➖</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="icon not-implemented">❌</span>', unsafe_allow_html=True)
            
            checklist[category][i] = (item[0], implemented, not_applicable, item[3])
    return checklist

def display_custom_measures(custom_measures):
    st.header("Custom Eco-Friendly Measures")
    new_measure = st.text_input("Add a custom eco-friendly measure:")
    if st.button("Add Measure"):
        if new_measure:
            custom_measures.append((new_measure, False, False))
            st.success(f"Added: {new_measure}")

    if custom_measures:
        st.subheader("Your Custom Measures")
        for i, (measure, implemented, not_applicable) in enumerate(custom_measures):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(measure)
            with col2:
                implemented = st.checkbox("Implemented", value=implemented, key=f"custom_{i}_implemented")
            with col3:
                not_applicable = st.checkbox("N/A", value=not_applicable, key=f"custom_{i}_na")
            
            # Visual feedback
            if implemented:
                st.markdown('<span class="icon implemented">✔️</span>', unsafe_allow_html=True)
            elif not_applicable:
                st.markdown('<span class="icon not-applicable">➖</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="icon not-implemented">❌</span>', unsafe_allow_html=True)
            
            custom_measures[i] = (measure, implemented, not_applicable)
    return custom_measures

def display_results(checklist, custom_measures, event_type):
    st.header(f"Results for {event_type}")

    # Calculate score
    total_applicable = 0
    implemented = 0
    for items in checklist.values():
        for item in items:
            if not item[2]:  # If not marked as N/A
                total_applicable += 1
                if item[1]:  # If implemented
                    implemented += 1
    
    for measure in custom_measures:
        if not measure[2]:  # If not marked as N/A
            total_applicable += 1
            if measure[1]:  # If implemented
                implemented += 1

    score = (implemented / total_applicable * 100) if total_applicable > 0 else 100

    # Display score with a progress bar
    st.subheader("Your Event's Eco-Score")
    st.progress(score / 100)
    st.write(f"Score: {score:.2f}%")
    st.write(f"Implemented measures: {implemented} out of {total_applicable} applicable measures")

    # Comparison feature (mock data - you'd need to implement actual data collection)
    avg_score = 75  # This would be calculated based on real data
    st.subheader("Score Comparison")
    st.write(f"Your score: {score:.2f}%")
    st.write(f"Average score for {event_type}: {avg_score:.2f}%")
    if score > avg_score:
        st.success(f"Great job! Your event is {score - avg_score:.2f}% more eco-friendly than average.")
    else:
        st.info(f"There's room for improvement. Your event is {avg_score - score:.2f}% less eco-friendly than average.")

    # Provide suggestions
    if score < 100:
        st.subheader("Suggestions for Improvement")
        for category, items in checklist.items():
            for item in items:
                if not item[1] and not item[2]:  # If not implemented and not N/A
                    st.write(f"- Consider implementing: {item[0]}")
                    st.write(f"  *Tip: {item[3]}*")

def display_eco_tips():
    st.header("Eco-Tips for Corporate Events")
    tips = [
        "Use digital invitations and event materials to reduce paper waste.",
        "Choose venues with natural lighting to reduce energy consumption.",
        "Offer plant-based meal options to reduce the event's carbon footprint.",
        "Use reusable name badges and collect them at the end of the event.",
        "Partner with local, sustainable businesses for event services and supplies.",
        "Implement a waste sorting system with clear signage for recycling and composting.",
        "Encourage attendees to bring their own reusable water bottles and provide water refill stations.",
        "Use energy-efficient equipment and turn off devices when not in use.",
        "Donate leftover food to local charities or food banks.",
        "Offset the carbon footprint of your event through reputable carbon offset programs."
    ]
    for tip in tips:
        st.markdown(f"• {tip}")

def display_resources():
    st.header("Resources for Eco-Friendly Corporate Events")
    resources = [
        {"name": "Sustainable Event Alliance", "url": "https://sustainable-event-alliance.org/"},
        {"name": "Green Meeting Industry Council", "url": "https://www.gmicglobal.org/"},
        {"name": "EcoVadis (Sustainability Ratings)", "url": "https://ecovadis.com/"},
        {"name": "ISO 20121 - Sustainable Events", "url": "https://www.iso.org/iso-20121-sustainable-events.html"},
        {"name": "Global Sustainable Tourism Council", "url": "https://www.gstcouncil.org/"},
    ]
    for resource in resources:
        st.markdown(f"• [{resource['name']}]({resource['url']})")

def load_checklist():
    return {
        "Venue Selection": [
            ("Choose a venue with green certifications", False, False, "Look for LEED, BREEAM, or other sustainability certifications."),
            ("Select a location accessible by public transport", False, False, "This reduces the carbon footprint of attendee travel."),
            ("Opt for venues with natural lighting", False, False, "This can significantly reduce energy consumption.")
        ],
        "Energy and Water": [
            ("Use energy-efficient lighting and equipment", False, False, "LED lights and Energy Star certified equipment can greatly reduce energy use."),
            ("Implement water-saving measures", False, False, "Use low-flow faucets and toilets, and avoid bottled water."),
            ("Offset energy use with renewable energy credits", False, False, "This can help neutralize your event's carbon footprint.")
        ],
        "Waste Management": [
            ("Provide clearly labeled recycling and composting bins", False, False, "Make it easy for attendees to dispose of waste properly."),
            ("Use digital materials instead of printed handouts", False, False, "This significantly reduces paper waste."),
            ("Choose reusable or compostable serving ware", False, False, "Avoid single-use plastics and opt for sustainable alternatives.")
        ],
        "Food and Beverage": [
            ("Offer plant-based and locally sourced food options", False, False, "This reduces the carbon footprint of your catering."),
            ("Use bulk dispensers for beverages", False, False, "This eliminates the need for individual bottles or cans."),
            ("Donate excess food to local charities", False, False, "This reduces food waste and supports the local community.")
        ],
        "Transportation": [
            ("Provide information on public transport options", False, False, "Encourage attendees to use eco-friendly transportation."),
            ("Offer virtual attendance options", False, False, "This can significantly reduce travel-related emissions."),
            ("Arrange shared transportation for off-site activities", False, False, "This is more efficient than individual transportation.")
        ]
    }

if __name__ == "__main__":
    main()
