import streamlit as st
import pandas as pd

def main():
    st.title("Eco-Event Scorer")
    st.write("Score how green your event is based on this checklist.")

    # Initialize session state
    if 'checklist' not in st.session_state:
        st.session_state.checklist = load_checklist()
    if 'custom_measures' not in st.session_state:
        st.session_state.custom_measures = []

    # Display checklist
    st.header("Checklist")
    for category, items in st.session_state.checklist.items():
        st.subheader(category)
        for i, item in enumerate(items):
            key = f"{category}_{i}"
            st.session_state.checklist[category][i] = (item[0], st.checkbox(item[0], value=item[1], key=key))

    # Custom measures
    st.header("Custom Measures")
    new_measure = st.text_input("Add a custom eco-friendly measure:")
    if st.button("Add Measure"):
        if new_measure:
            st.session_state.custom_measures.append((new_measure, False))

    # Display custom measures
    for i, (measure, checked) in enumerate(st.session_state.custom_measures):
        key = f"custom_{i}"
        st.session_state.custom_measures[i] = (measure, st.checkbox(measure, value=checked, key=key))

    # Calculate score
    total_items = sum(len(items) for items in st.session_state.checklist.values()) + len(st.session_state.custom_measures)
    checked_items = sum(item[1] for items in st.session_state.checklist.values() for item in items) + sum(item[1] for item in st.session_state.custom_measures)
    score = (checked_items / total_items) * 100

    st.header("Results")
    st.write(f"Your event's eco-score: {score:.2f}%")

    # Provide suggestions
    if score < 100:
        st.subheader("Suggestions for Improvement")
        for category, items in st.session_state.checklist.items():
            for item in items:
                if not item[1]:
                    st.write(f"- Consider implementing: {item[0]}")

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
            ("Select a place accessible by soft mobility", False),
            ("Consider a shuttle service", False),
            ("Collect information on participants' mode of transport", False)
        ],
        "Catering": [
            ("Choose a zero-waste provider", False),
            ("Provide reusable utensils", False),
            ("Offer waste-free drinks", False),
            ("Favor local, seasonal ingredients with vegetarian options", False),
            ("Provide adequate quantities to avoid waste", False)
        ],
        "Logistics and Equipment": [
            ("Ensure presence of recycling bins", False),
            ("Use reusable decorations", False),
            ("Rent or use reusable exhibition stands", False)
        ],
        "Hotels": [
            ("Look for eco-friendly hotels with certifications", False),
            ("Check for sustainable development charters", False)
        ],
        "Communication": [
            ("Inform guests of eco-friendly event participation", False),
            ("Encourage guests to bring their own water bottle/cup", False),
            ("Encourage eco-friendly transportation", False)
        ],
        "Carbon Footprint": [
            ("Send information to ESG team for carbon footprint assessment", False),
            ("Consider carbon offsetting", False)
        ]
    }

def generate_report(checklist, custom_measures, score):
    data = []
    for category, items in checklist.items():
        for item in items:
            data.append({"Category": category, "Measure": item[0], "Implemented": "Yes" if item[1] else "No"})
    
    for measure, implemented in custom_measures:
        data.append({"Category": "Custom Measures", "Measure": measure, "Implemented": "Yes" if implemented else "No"})
    
    df = pd.DataFrame(data)
    df = df.append({"Category": "Overall Score", "Measure": f"{score:.2f}%", "Implemented": ""}, ignore_index=True)
    return df.to_csv(index=False)

if __name__ == "__main__":
    main()
