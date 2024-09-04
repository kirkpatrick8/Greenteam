import streamlit as st
import pandas as pd

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

    This tool helps you assess and improve the environmental friendliness of your events. Check off the measures you've implemented, mark those that aren't applicable to your event, and get instant feedback on your event's sustainability score.

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

    # Contact information
    st.sidebar.markdown("---")
    st.sidebar.subheader("Feedback & Suggestions")
    st.sidebar.markdown("""
    If you have any suggestions, feedback, or encounter any issues while using this app, 
    please email Mark Kirkpatrick at mark.kirkpatrick@aecom.com.
    
    Your input is valuable and will help improve this tool for everyone!
    """)

def display_checklist():
    st.header("Eco-Friendly Checklist")
    for category, items in st.session_state.checklist.items():
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
            st.session_state.checklist[category][i] = (item[0], implemented, not_applicable, item[3])

def display_custom_measures():
    st.header("Custom Eco-Friendly Measures")
    new_measure = st.text_input("Add a custom eco-friendly measure:")
    if st.button("Add Measure"):
        if new_measure:
            st.session_state.custom_measures.append((new_measure, False, False))
            st.success(f"Added: {new_measure}")

    if st.session_state.custom_measures:
        st.subheader("Your Custom Measures")
        for i, (measure, implemented, not_applicable) in enumerate(st.session_state.custom_measures):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(measure)
            with col2:
                implemented = st.checkbox("Implemented", value=implemented, key=f"custom_{i}_implemented")
            with col3:
                not_applicable = st.checkbox("N/A", value=not_applicable, key=f"custom_{i}_na")
            st.session_state.custom_measures[i] = (measure, implemented, not_applicable)

def display_results():
    st.header("Results")

    # Calculate score
    total_applicable = 0
    implemented = 0
    for items in st.session_state.checklist.values():
        for item in items:
            if not item[2]:  # If not marked as N/A
                total_applicable += 1
                if item[1]:  # If implemented
                    implemented += 1
    
    for measure in st.session_state.custom_measures:
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

    # Provide suggestions
    if score < 100:
        st.subheader("Suggestions for Improvement")
        for category, items in st.session_state.checklist.items():
            for item in items:
                if not item[1] and not item[2]:  # If not implemented and not N/A
                    st.write(f"- Consider implementing: {item[0]}")
                    st.write(f"  *Tip: {item[3]}*")

def load_checklist():
    return {
        "Location and Transportation": [
            ("Select a place accessible by soft mobility", False, False, "Choose venues near public transit or with good cycling/walking access."),
            ("Consider a shuttle service", False, False, "Organize shared transportation to reduce individual car use."),
            ("Collect information on participants' mode of transport", False, False, "This data helps in calculating the event's carbon footprint.")
        ],
        "Catering": [
            ("Choose a zero-waste provider", False, False, "Look for caterers who prioritize minimal packaging and composting."),
            ("Provide reusable utensils", False, False, "Use washable plates, cups, and cutlery instead of disposables."),
            ("Offer waste-free drinks", False, False, "Serve beverages in bulk containers or use refillable bottles."),
            ("Favor local, seasonal ingredients with vegetarian options", False, False, "This reduces transportation emissions and often has a lower environmental impact."),
            ("Provide adequate quantities to avoid waste", False, False, "Careful planning can significantly reduce food waste.")
        ],
        "Logistics and Equipment": [
            ("Ensure presence of recycling bins", False, False, "Clearly label bins for different types of waste to encourage proper disposal."),
            ("Use reusable decorations", False, False, "Invest in durable decorations that can be used for multiple events."),
            ("Rent or use reusable exhibition stands", False, False, "This reduces waste and can be more cost-effective in the long run.")
        ],
        "Hotels": [
            ("Look for eco-friendly hotels with certifications", False, False, "Certifications like LEED or Green Key indicate environmentally responsible practices."),
            ("Check for sustainable development charters", False, False, "Even without formal certifications, many hotels have their own sustainability initiatives.")
        ],
        "Communication": [
            ("Inform guests of eco-friendly event participation", False, False, "This raises awareness and can encourage attendees to support your initiatives."),
            ("Encourage guests to bring their own water bottle/cup", False, False, "This simple step can significantly reduce single-use plastic waste."),
            ("Encourage eco-friendly transportation", False, False, "Provide information on public transit options or organize carpooling.")
        ],
        "Carbon Footprint": [
            ("Send information to ESG team for carbon footprint assessment", False, False, "This helps quantify the event's environmental impact and identify areas for improvement."),
            ("Consider carbon offsetting", False, False, "While not a substitute for reduction efforts, offsetting can help mitigate unavoidable emissions.")
        ]
    }

if __name__ == "__main__":
    main()
