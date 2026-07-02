import streamlit as st
from sqlmodel import Session, select
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine, Task, Goal
from ai_engine import ask_ai_coach

st.set_page_config(page_title="AI Control Room", page_icon="🤖", layout="wide")

st.title("🤖 AI Chief of Staff Control Room")
st.markdown("##### Dynamic schedule synthesis and execution optimization engine loops.")
st.divider()

# Prepare operational data for AI Context Injection
with Session(engine) as session:
    all_tasks = session.exec(select(Task)).all()
    all_goals = session.exec(select(Goal).where(Goal.is_archived == False)).all()

task_summary = [{"title": t.title, "cat": t.category, "completed": t.is_completed, "hours": t.estimated_time} for t in all_tasks]
goal_summary = [{"title": g.title, "cat": g.category, "priority_stars": g.priority} for g in all_goals]

system_data_context = f"Active Goals: {goal_summary}\nActive Tasks Stack: {task_summary}"

# Layout UI Division
col_chat, col_pre = st.columns([2, 1])

with col_chat:
    st.subheader("💬 Executive Handshake Protocol")
    st.caption("Feed telemetry or operational statements directly to the AI Coach.")
    
    # Initialize local session memory state for chat logs
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
        
    user_input = st.chat_input("Ask AI Planner or Coach (e.g., 'I have 3 hours today, build an execution block' or 'I missed my tasks')")
    
    if user_input:
        # User log update
        st.session_state.ai_chat_history.append({"role": "user", "text": user_input})
        
        # Trigger generation loop
        with st.spinner("Processing telemetry constraints via Gemini Engine..."):
            ai_response = ask_ai_coach(system_data_context, user_input)
            st.session_state.ai_chat_history.append({"role": "assistant", "text": ai_response})
            
    # Render chat loops reactively
    for msg in reversed(st.session_state.ai_chat_history):
        if msg["role"] == "user":
            st.chat_message("user", avatar="🎯").write(msg["text"])
        else:
            st.chat_message("assistant", avatar="🤖").write(msg["text"])

with col_pre:
    st.subheader("💡 Pre-set Action Macros")
    st.caption("Quick contextual vectors to trigger instant processing blocks.")
    
    if st.button("⚡ Generate Optimal Schedule for Today", use_container_width=True):
        with st.spinner("Analyzing priorities..."):
            res = ask_ai_coach(system_data_context, "I need a strict hourly execution plan based on my pending tasks for today. Give me time blocks.")
            st.session_state.ai_chat_history.append({"role": "user", "text": "Trigger Daily Schedule Macro"})
            st.session_state.ai_chat_history.append({"role": "assistant", "text": res})
            st.rerun()
            
    if st.button("🔋 Low Energy Protocol Adaptation", use_container_width=True):
        with st.spinner("Recalibrating load weights..."):
            res = ask_ai_coach(system_data_context, "I am feeling extremely tired and experiencing cognitive fatigue. Help me prune the task stack and select only the absolute non-negotiable mission critical item.")
            st.session_state.ai_chat_history.append({"role": "user", "text": "Trigger Low Energy Protocol"})
            st.session_state.ai_chat_history.append({"role": "assistant", "text": res})
            st.rerun()

        