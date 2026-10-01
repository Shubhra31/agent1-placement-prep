import streamlit as st

from app import placement_graph


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Placement Prep Agent",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------
st.title("🎯 AI Placement Assistant")

st.write(
    "Your AI assistant for placement preparation, "
    "interview practice, coding questions and academic calculations."
)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Student Information")

name = st.sidebar.text_input("Student Name")

branch = st.sidebar.text_input(
    "Branch",
    placeholder="Example: CSE"
)

year = st.sidebar.selectbox(
    "Year",
    [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year"
    ]
)

cgpa = st.sidebar.text_input(
    "CGPA",
    placeholder="Example: 8.2"
)


# -----------------------------
# Student Information
# -----------------------------
student_info = f"""
Name: {name if name else "Not provided"}
Branch: {branch if branch else "Not provided"}
Year: {year}
CGPA: {cgpa if cgpa else "Not provided"}
"""


# -----------------------------
# Mode Selection
# -----------------------------
mode = st.selectbox(
    "What do you want help with?",
    [
        "Placement Preparation",
        "Technical Interview",
        "Coding Questions",
        "HR Interview",
        "Skill Gap Analysis",
        "Mock Interview",
        "Percentage / CGPA Calculator"
    ]
)


# -----------------------------
# User Request
# -----------------------------
if mode == "Percentage / CGPA Calculator":

    question = st.text_area(
        "Enter your marks or CGPA",
        placeholder=(
            "Example: I scored 425 marks out of 500. "
            "Calculate my percentage."
        ),
        height=150
    )

else:

    question = st.text_area(
        "What would you like help with?",
        placeholder=(
            "Example: I have 2 months for placements. "
            "Create a preparation plan for me."
        ),
        height=150
    )


# -----------------------------
# Generate Button
# -----------------------------
if st.button("🚀 Generate", type="primary"):

    if not question.strip():

        st.warning("Please enter your request.")

    else:

        with st.spinner("🤖 Placement Agent is thinking..."):

            try:

                result = placement_graph.invoke(
                    {
                        "mode": mode,
                        "student_info": student_info,
                        "question": question,
                        "result": ""
                    }
                )

                st.subheader("📋 Your Result")

                st.markdown(result["result"][0]["text"])

            except Exception as e:

                st.error(
                    "Something went wrong while generating the response."
                )

                st.exception(e)