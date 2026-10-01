import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


# Load environment variables
load_dotenv()


# -----------------------------
# Gemini Configuration
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
    temperature=0.7,
)


# -----------------------------
# Agent State
# -----------------------------
class PlacementState(TypedDict):
    mode: str
    student_info: str
    question: str
    result: str


# -----------------------------
# Placement Preparation
# -----------------------------
def placement_node(state: PlacementState):

    mode = state["mode"]
    student_info = state["student_info"]
    question = state["question"]

    prompt = f"""
You are an AI Placement Preparation Agent for college students.

Your job is to help students prepare for campus placements.

Student Information:
{student_info}

Selected Mode:
{mode}

Student Request:
{question}

Give a practical and structured response.

Depending on the selected mode:

1. Placement Preparation
   - Create a realistic preparation roadmap.
   - Include technical skills, coding, aptitude, communication and interview preparation.

2. Technical Interview
   - Generate technical interview questions.
   - Include answers and short explanations.
   - Cover appropriate subjects based on the student's background.

3. Coding Questions
   - Generate coding problems.
   - Include difficulty level.
   - Include the expected approach and explanation.
   - Give code when appropriate.

4. HR Interview
   - Generate HR interview questions.
   - Provide sample answers.
   - Give tips for answering professionally.

5. Skill Gap Analysis
   - Identify skills the student should improve.
   - Divide them into beginner, intermediate and advanced areas.
   - Create a roadmap.

6. Mock Interview
   - Act as an interviewer.
   - Ask realistic placement interview questions.
   - Do not provide all questions at once.
   - Start with one appropriate question.

Keep the answer simple, clear and useful for a college student.

Use headings, bullet points and numbered lists where appropriate.
"""


    response = llm.invoke(prompt)

    return {
        "result": response.content
    }


# -----------------------------
# Percentage / CGPA Calculator
# -----------------------------
def calculation_node(state: PlacementState):

    question = state["question"]

    prompt = f"""
You are an academic marks and percentage calculator.

Student request:
{question}

Perform the calculation carefully.

If the student provides:
- Marks obtained and total marks → calculate percentage.
- Subject-wise marks → calculate total marks and percentage.
- CGPA → explain the calculation clearly.
- Multiple subjects → show the calculation step by step.

Use mathematical calculations rather than guessing.

Do not invent missing numbers.

If information is missing, tell the student exactly what information is required.

Show the formula and final answer clearly.
"""


    response = llm.invoke(prompt)

    return {
        "result": response.content
    }


# -----------------------------
# Router
# -----------------------------
def router(state: PlacementState):

    mode = state["mode"]

    if mode == "Percentage / CGPA Calculator":
        return "calculator"

    return "placement"


# -----------------------------
# Create LangGraph
# -----------------------------
graph = StateGraph(PlacementState)

graph.add_node("placement", placement_node)
graph.add_node("calculator", calculation_node)


# Decide which node should run
graph.add_conditional_edges(
    START,
    router,
    {
        "placement": "placement",
        "calculator": "calculator",
    },
)


# End of workflows
graph.add_edge("placement", END)
graph.add_edge("calculator", END)


# Compile the agent
placement_graph = graph.compile()