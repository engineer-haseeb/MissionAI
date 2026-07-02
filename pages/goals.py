import streamlit as st
from sqlmodel import Session, select
import sys
import os

# Root directory se structures connect karne ke liye setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine, Goal, Task, add_goal, delete_goal, get_all_goals

st.set_page_config(page_title="Strategic Goals Hub", page_icon="🎯", layout="wide")

st.title("🎯 Strategic Goals & Milestones")
st.markdown("##### Abdul Haseeb's High-Level Objective Mapping Engine.")
st.divider()

# ==========================================
# 1. GOAL CREATION FORM (SINGLE-USER)
# ==========================================
with st.expander("🚀 Formulate New Strategic Goal", expanded=False):
    with st.form("goal_creation_form", clear_on_submit=True):
        g_title = st.text_input("Goal Objective Title", placeholder="e.g., Graduate Master's in Computer Science")
        
        c1, c2 = st.columns(2)
        g_cat = c1.selectbox("Strategic Domain", ["Research", "Cloud AI", "HSK4", "Gym", "Career", "Personal"])
        g_priority = c2.slider("Priority Alignment (Stars)", min_value=1, max_value=5, value=3)
        
        if st.form_submit_button("Initialize Goal") and g_title:
            add_goal(g_title, g_cat, g_priority)
            st.toast("New strategic milestone synchronized!", icon="🎯")
            st.rerun()

# ==========================================
# 2. DATA QUERY LAYER (GLOBAL FETCH)
# ==========================================
active_goals = get_all_goals()

if not active_goals:
    st.info("No long-term strategic goals initialized yet. Expand the panel above to deploy your first target.")
else:
    for goal in active_goals:
        with Session(engine) as session:
            goal_tasks = session.exec(select(Task).where(Task.goal_id == goal.id)).all()
        
        total_gt = len(goal_tasks)
        completed_gt = sum(1 for t in goal_tasks if t.is_completed)
        progress_percentage = (completed_gt / total_gt) if total_gt > 0 else 0.0
        
        with st.container():
            col_meta, col_prog, col_act = st.columns([2, 3, 1])
            
            with col_meta:
                priority_stars = "⭐" * goal.priority
                st.markdown(f"### {goal.title}")
                st.markdown(f"`Domain: {goal.category}` | {priority_stars}")
            
            with col_prog:
                st.write(f"**Execution Status:** {completed_gt}/{total_gt} Tasks Closed")
                st.progress(progress_percentage)
                st.caption(f"Calculated Target Vector Completion: {int(progress_percentage * 100)}%")
            
            with col_act:
                st.write("") 
                if st.button("Archive Goal", key=f"arch_{goal.id}"):
                    delete_goal(goal.id)
                    st.rerun()
                    
        st.divider()