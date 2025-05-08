import streamlit as st
import pandas as pd
import os
import altair as alt

MOCK_DATA = [
    {"Use Case": "Customer Support Chatbot", "Business Impact": 5, "Feasibility": 4, "Compliance Risk": 3, "User Readiness": 5},
    {"Use Case": "Automated Loan Summaries", "Business Impact": 4, "Feasibility": 4, "Compliance Risk": 2, "User Readiness": 4},
    {"Use Case": "Email Response Generator", "Business Impact": 3, "Feasibility": 5, "Compliance Risk": 3, "User Readiness": 5},
    {"Use Case": "Fraud Alert Explanation", "Business Impact": 5, "Feasibility": 3, "Compliance Risk": 2, "User Readiness": 3},
    {"Use Case": "Internal Knowledge Assistant", "Business Impact": 3, "Feasibility": 4, "Compliance Risk": 1, "User Readiness": 4},
    {"Use Case": "Code Doc Generator", "Business Impact": 2, "Feasibility": 5, "Compliance Risk": 1, "User Readiness": 5},
    {"Use Case": "Call Center Summary Tool", "Business Impact": 4, "Feasibility": 4, "Compliance Risk": 2, "User Readiness": 3},
    {"Use Case": "Contract Clause Extractor", "Business Impact": 3, "Feasibility": 3, "Compliance Risk": 4, "User Readiness": 2},
    {"Use Case": "AI Sales Coach", "Business Impact": 4, "Feasibility": 3, "Compliance Risk": 2, "User Readiness": 4},
    {"Use Case": "Meeting Notes Summarizer", "Business Impact": 3, "Feasibility": 5, "Compliance Risk": 1, "User Readiness": 5}
]

st.set_page_config(page_title="LLM Use Case Discovery", layout="wide")
st.title("🔍 LLM Use Case Discovery Framework")
st.write("Evaluate and prioritize GenAI use cases based on business value, feasibility, compliance, and readiness.")
if "name" not in st.session_state:
    st.session_state.name = ""
if "impact" not in st.session_state:
    st.session_state.impact = 1
if "feasibility" not in st.session_state:
    st.session_state.feasibility = 1
if "risk" not in st.session_state:
    st.session_state.risk = 1
if "readiness" not in st.session_state:
    st.session_state.readiness = 1

# Input form
with st.form("use_case_form"):
    name = st.text_input("Use Case Name")
    impact = st.slider("Business Impact (Revenue, Reach)", 1, 5, value=1)
    feasibility = st.slider("Technical Feasibility", 1, 5, value=1)
    risk = st.slider("Compliance / Risk Level", 1, 5, value=1)
    readiness = st.slider("User Readiness", 1, 5, value=1)

    submitted = st.form_submit_button("Add Use Case")

# Handle data storage
csv_path = "usecases.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(MOCK_DATA)
    df["Score"] = (
        df["Business Impact"] * 0.4 +
        df["Feasibility"] * 0.3 +
        (6 - df["Compliance Risk"]) * 0.2 +
        df["User Readiness"] * 0.1
    )
    df.to_csv(csv_path, index=False)

# Add new entry
if submitted:
    if name.strip() == "":
        st.warning("Please enter a use case name before submitting.")
    else:
        # Prevent duplicates
        existing_names = df["Use Case"].str.lower().tolist()
        if name.strip().lower() in existing_names:
            st.warning("This use case name already exists. Please enter a unique name.")
        else:
            score = (
                impact * 0.4 +
                feasibility * 0.3 +
                (6 - risk) * 0.2 +
                readiness * 0.1
            )

            new_entry = pd.DataFrame([{
                "Use Case": name.strip(),
                "Business Impact": impact,
                "Feasibility": feasibility,
                "Compliance Risk": risk,
                "User Readiness": readiness,
                "Score": score
            }])

            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(csv_path, index=False)
            st.success("Use case added!")

            # Reset all values
            st.rerun()

# Display table
# Display table
st.header("📊 Prioritized Use Cases")

if not df.empty:
    df_sorted = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    df_sorted.index = df_sorted.index + 1
    df_sorted.index.name = "ID"
    
    st.dataframe(df_sorted, use_container_width=True)

    # Show only last 10 added use cases
    last_10 = df.tail(10).copy()
    last_10 = last_10.set_index("Use Case")

    st.subheader("📈 Last 10 Submitted Use Cases by Score")
    
    bar_chart = alt.Chart(last_10.reset_index()).mark_bar().encode(
    x=alt.X("Use Case", sort="-y", title="Use Case"),
    y=alt.Y("Score", title="Total Score"),
    tooltip=["Use Case", "Score"]
    ).properties(
    width=700,
    height=400
    )
    st.altair_chart(bar_chart, use_container_width=True)

else:
    st.info("No use cases added yet.")