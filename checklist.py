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
import json

def load_progress():
    try:
        with open("progress.json", "r") as f:
            content = f.read()
            if not content.strip():
                return {}  # Return empty dict if file is empty
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return empty dict if file is not found or has invalid JSON
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

    # Unique identifier for the event
    event_date = st.date_input("Event Date")
    event_id = f"{selected_event_type}_{event_date}"

    # Load checklist based on event type
    checklist = load_checklist(selected_event_type)

    # Load previous progress if it exists
    if event_id in st.session_state.progress:
        saved_checklist = st.session_state.progress[event_id]['checklist']
        # Merge saved progress with current checklist
        for category in checklist:
            for i, item in enumerate(checklist[category]):
                if category in saved_checklist and i < len(saved_checklist[category]):
                    checklist[category][i] = (item[0], saved_checklist[category][i][1], saved_checklist[category][i][2], item[3])
        custom_measures = st.session_state.progress[event_id]['custom_measures']
    else:
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
        display_eco_tips(selected_event_type)
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

def display_eco_tips(event_type):
    st.header(f"Eco-Tips for {event_type}")
    tips = load_eco_tips(event_type)
    for tip in tips:
        st.markdown(f"• {tip}")

def display_resources():
    st.header("Resources for Eco-Friendly Corporate Events")
    resources = [
        {"name": "Sustainable event planning - Berlin Convention Office", "url": "https://convention.visitberlin.de/en/sustainable-event-planning"},
        {"name": "The Importance of Eco-Friendly Events and How to Plan Them - Events Made Simple", "url": "https://www.eventsmadesimple.co.uk/the-importance-of-eco-friendly-events-and-how-to-plan-them/"},
        {"name": "Sustainability Tracking Software - Momentus Technologies", "url": "https://gomomentus.com/"},
        {"name": "Sustainable Event Planning: Beyond the Basics - The Event Planner Expo", "url": "https://www.theeventplannerexpo.com/sustainable-event-planning-beyond-the-basics/"},
        {"name": "10 Green Event Ideas That Can Make a Huge Difference - Cvent Blog", "url": "https://www.cvent.com/en/blog/events/green-event-ideas"},
    ]
    for resource in resources:
        st.markdown(f"• [{resource['name']}]({resource['url']})")

def load_checklist(event_type):
    # Common checklist items for all event types
    common_checklist = {
        "Venue Selection": [
            ("Choose a venue with green certifications", False, False, "Look for LEED, BREEAM, or other sustainability certifications."),
            ("Select a location accessible by public transport", False, False, "This reduces the carbon footprint of attendee travel."),
            ("Opt for venues with natural lighting", False, False, "This can significantly reduce energy consumption."),
            ("Choose a venue with efficient HVAC systems", False, False, "This can significantly reduce energy consumption for heating and cooling.")
        ],
        "Energy and Water": [
            ("Use energy-efficient lighting and equipment", False, False, "LED lights and Energy Star certified equipment can greatly reduce energy use."),
            ("Implement water-saving measures", False, False, "Use low-flow faucets and toilets, and avoid bottled water."),
            ("Offset energy use with renewable energy credits", False, False, "This can help neutralize your event's carbon footprint."),
            ("Use smart power strips and timers", False, False, "This can help reduce standby power consumption.")
        ],
        "Waste Management": [
            ("Provide clearly labeled recycling and composting bins", False, False, "Make it easy for attendees to dispose of waste properly."),
            ("Use digital materials instead of printed handouts", False, False, "This significantly reduces paper waste."),
            ("Choose reusable or compostable serving ware", False, False, "Avoid single-use plastics and opt for sustainable alternatives."),
            ("Partner with local recycling and composting facilities", False, False, "Ensure proper disposal of waste after the event.")
        ],
        "Food and Beverage": [
            ("Offer plant-based and locally sourced food options", False, False, "This reduces the carbon footprint of your catering."),
            ("Use bulk dispensers for beverages", False, False, "This eliminates the need for individual bottles or cans."),
            ("Donate excess food to local charities", False, False, "This reduces food waste and supports the local community."),
            ("Choose organic and fair trade options when possible", False, False, "This supports sustainable agriculture and fair labor practices.")
        ],
        "Transportation": [
            ("Provide information on public transport options", False, False, "Encourage attendees to use eco-friendly transportation."),
            ("Offer virtual attendance options", False, False, "This can significantly reduce travel-related emissions."),
            ("Arrange shared transportation for off-site activities", False, False, "This is more efficient than individual transportation."),
            ("Encourage carpooling among attendees", False, False, "Set up a carpooling system to reduce individual car use.")
        ]
    }

    # Event-specific checklist items
    event_specific_items = {
        "Conference or Seminar": {
            "Technology": [
                ("Use energy-efficient audiovisual equipment", False, False, "Choose equipment with power-saving modes."),
                ("Offer virtual attendance options", False, False, "This can significantly reduce travel-related emissions."),
                ("Provide digital conference materials", False, False, "Use apps or websites instead of printed programs."),
                ("Implement a conference app for networking", False, False, "This can reduce the need for printed business cards and schedules.")
            ],
            "Session Planning": [
                ("Include sustainability-focused sessions", False, False, "Educate attendees about sustainability in your industry."),
                ("Use interactive polling to reduce paper use", False, False, "Digital polling can engage attendees without wasting paper."),
                ("Offer workshops on sustainable practices", False, False, "Provide practical sustainability skills to attendees.")
            ]
        },
        "Board Meeting": {
            "Paper Reduction": [
                ("Use digital voting systems", False, False, "Eliminate paper ballots for board decisions."),
                ("Implement paperless document sharing", False, False, "Use secure digital platforms for sharing confidential documents."),
                ("Provide tablets or laptops for document viewing", False, False, "This eliminates the need for printed documents during the meeting.")],
            "Meeting Efficiency": [
                ("Use video conferencing for remote participants", False, False, "This reduces travel-related emissions."),
                ("Implement a strict agenda to reduce meeting time", False, False, "Shorter meetings consume less energy."),
                ("Choose energy-efficient meeting room equipment", False, False, "Use low-power projectors and screens.")
            ]
        },
        "Team Building Event": {
            "Sustainable Activities": [
                ("Choose eco-friendly team building activities", False, False, "Consider activities like park clean-ups or sustainable craft workshops."),
                ("Use reusable name tags and team identifiers", False, False, "Avoid disposable items for team identification."),
                ("Opt for outdoor activities when possible", False, False, "This can reduce energy consumption for indoor spaces."),
                ("Incorporate sustainability education into activities", False, False, "Use the event as an opportunity to teach about environmental issues.")
            ],
            "Eco-friendly Rewards": [
                ("Offer sustainable prizes or rewards", False, False, "Choose eco-friendly or locally made items as prizes."),
                ("Provide digital certificates of participation", False, False, "Avoid printing paper certificates."),
                ("Plant trees or donate to environmental causes in participants' names", False, False, "This creates a lasting positive impact.")
            ]
        },
        "Product Launch": {
            "Sustainable Promotion": [
                ("Use eco-friendly promotional materials", False, False, "Choose recyclable or plantable promotional items."),
                ("Highlight the product's sustainability features", False, False, "Educate attendees about the product's environmental impact."),
                ("Implement digital product demonstrations", False, False, "Use screens or AR/VR to showcase products instead of physical samples."),
                ("Offer sustainable packaging options", False, False, "If products are distributed, use minimal, recyclable packaging.")
            ],
            "Venue Setup": [
                ("Use modular, reusable booth designs", False, False, "This reduces waste from single-use displays."),
                ("Implement energy-efficient lighting for product displays", False, False, "Use LED lights to highlight products."),
                ("Create a recycling plan for promotional materials", False, False, "Ensure that any distributed materials can be easily recycled.")
            ]
        },
        "Annual General Meeting": {
            "Shareholder Engagement": [
                ("Offer online participation options", False, False, "Reduce travel emissions by allowing remote attendance and voting."),
                ("Provide sustainability reports digitally", False, False, "Avoid printing large reports by offering digital versions."),
                ("Use an event app for agenda and voting", False, False, "This can replace printed materials and paper ballots."),
                ("Stream the meeting live for remote shareholders", False, False, "This allows participation without travel.")
            ],
            "Sustainable Presentations": [
                ("Use energy-efficient presentation equipment", False, False, "Choose projectors and screens with low power consumption."),
                ("Provide digital access to all meeting documents", False, False, "Allow shareholders to view documents on their own devices."),
                ("Include a sustainability progress report in the agenda", False, False, "Highlight the company's environmental initiatives.")
            ]
        },
        "Trade Show or Exhibition": {
            "Booth Design": [
                ("Use sustainable materials for booth construction", False, False, "Choose recyclable or reusable booth materials."),
                ("Implement energy-efficient lighting in booths", False, False, "Use LED lights and minimize unnecessary lighting."),
                ("Design modular booth elements for reuse", False, False, "Create booth components that can be reconfigured for future events."),
                ("Use digital displays instead of printed banners", False, False, "This allows for easy updates and reduces waste.")
            ],
            "Exhibitor Guidelines": [
                ("Provide exhibitors with sustainability guidelines", False, False, "Encourage all exhibitors to follow eco-friendly practices."),
                ("Offer incentives for sustainable booth designs", False, False, "Recognize and reward exhibitors who prioritize sustainability."),
                ("Implement a waste reduction competition among exhibitors", False, False, "Encourage innovative ways to minimize waste."),
                ("Facilitate booth material recycling post-event", False, False, "Provide clear guidelines and services for material disposal.")
            ]
        },
        "Corporate Party or Celebration": {
            "Sustainable Decorations": [
                ("Use reusable or biodegradable decorations", False, False, "Avoid single-use plastic decorations."),
                ("Choose local and seasonal flowers or plants", False, False, "Reduce transportation emissions and support local businesses."),
                ("Implement energy-efficient mood lighting", False, False, "Use LED string lights or solar-powered options."),
                ("Create decorations from recycled materials", False, False, "Engage employees in creating unique, sustainable decor.")
            ],
            "Entertainment": [
                ("Choose local entertainers to reduce travel", False, False, "This supports the local community and reduces transportation emissions."),
                ("Opt for acoustic performances when possible", False, False, "This can reduce energy use for sound systems."),
                ("Implement a sustainability theme in activities", False, False, "Incorporate eco-friendly messages into party games or performances."),
                ("Use digital photo booths instead of printed photos", False, False, "Allow guests to receive photos electronically.")
            ]
        }
    }

    # Combine common checklist with event-specific items
    if event_type in event_specific_items:
        common_checklist.update(event_specific_items[event_type])
    
    return common_checklist

def load_eco_tips(event_type):
    common_tips = [
        "Use digital invitations and event materials to reduce paper waste.",
        "Choose venues with natural lighting to reduce energy consumption.",
        "Offer plant-based meal options to reduce the event's carbon footprint.",
        "Use reusable name badges and collect them at the end of the event.",
        "Partner with local, sustainable businesses for event services and supplies.",
        "Implement a comprehensive recycling and composting program.",
        "Educate attendees about the event's sustainability initiatives.",
        "Choose venues that have strong sustainability policies in place.",
        "Minimize swag and opt for useful, sustainable items if necessary.",
        "Conduct a post-event sustainability assessment to improve future events."
    ]

    event_specific_tips = {
        "Conference or Seminar": [
            "Encourage speakers to use digital presentations instead of handouts.",
            "Set up a dedicated app for the conference to reduce printed materials.",
            "Offer virtual attendance options to reduce travel-related emissions.",
            "Implement a 'green speaker' certification for presenters who follow sustainable practices.",
            "Organize networking sessions around sustainability themes."
        ],
        "Board Meeting": [
            "Implement a bring-your-own-device policy to reduce the need for printing.",
            "Use video conferencing for board members who can't attend in person.",
            "Choose a meeting venue close to where most board members are based.",
            "Provide reusable water bottles or glasses instead of disposable options.",
            "Implement paperless voting systems for board decisions."
        ],
        "Team Building Event": [
            "Choose outdoor locations to reduce energy consumption.",
            "Incorporate sustainability challenges into team building activities.",
            "Use eco-friendly materials for any team building supplies or equipment.",
            "Partner with local environmental organizations for volunteer activities.",
            "Provide sustainable transportation options for team members."
        ],
        "Product Launch": [
            "Use virtual or augmented reality for product demonstrations to reduce physical waste.",
            "Offer digital goodie bags instead of physical ones.",
            "Highlight the product's sustainability features in the launch presentation.",
            "Use energy-efficient lighting and sound systems for the event.",
            "Implement a product packaging return or recycling program at the launch."
        ],
        "Annual General Meeting": [
            "Provide digital voting options to reduce paper use.",
            "Stream the meeting live for shareholders who can't attend in person.",
            "Offer incentives for shareholders who choose digital over printed materials.",
            "Include a presentation on the company's sustainability initiatives.",
            "Choose a central, easily accessible location to minimize travel."
        ],
        "Trade Show or Exhibition": [
            "Design modular, reusable booth elements to reduce waste.",
            "Use QR codes for information sharing instead of printed brochures.",
            "Implement a 'green exhibitor' certification program.",
            "Organize a sustainability award for the most eco-friendly booth.",
            "Provide centralized recycling stations throughout the exhibition area."
        ],
        "Corporate Party or Celebration": [
            "Choose venues that support local communities and sustainable practices.",
            "Opt for e-tickets or app-based guest lists instead of paper tickets.",
            "Use locally-sourced, seasonal ingredients for catering.",
            "Implement a zero-waste policy for the event.",
            "Donate leftover food to local charities or food banks."
        ],
        "Other Corporate Event": [
            "Consider the unique aspects of your event and how to make them more sustainable.",
            "Engage employees in brainstorming eco-friendly ideas for the event.",
            "Implement a sustainability pledge for all event participants.",
            "Create a green team to oversee the event's environmental initiatives.",
            "Conduct a carbon footprint analysis and offset emissions."
        ]
    }

    return common_tips + event_specific_tips.get(event_type, [])

if __name__ == "__main__":
    main()
