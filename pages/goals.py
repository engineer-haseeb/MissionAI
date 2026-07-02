import streamlit as st
import datetime
from database import get_all_goals, add_goal, delete_goal

st.set_page_config(page_title="Strategic Goals", layout="wide", page_icon="🎯")

st.title("🎯 Strategic Goals & Milestone Anchors")
st.caption("Define long-term academic and funding targets. These drive your daily tasks.")

# Goal Insertion Form
with st.expander("➕ Launch New Strategic Goal", expanded=False):
    with st.form("goal_page_form", clear_on_submit=True):
        g_title = st.text_input("Strategic Target Objective")
        g_cat = st.selectbox("Strategic Category Focus", ["Research", "PhD", "Scholarship", "Learning", "Health", "Finance", "Personal"])
        g_prio = st.selectbox("Priority Class", ["Critical", "High", "Medium", "Low"])
        g_dead = st.date_input("Target Goal Deadline", value=datetime.date.today() + datetime.timedelta(days=90))
        
        if st.form_submit_button("Deploy Goal Asset"):
            if g_title:
                add_goal(g_title, g_cat, g_prio, g_dead)
                st.success("Goal successfully anchored!")
                st.rerun()

# Display Existing Goals
st.markdown("---")
goals_pool = get_all_goals()

if not goals_pool:
    st.info("No active strategic goals found. Add your first goal above!")
else:
    for goal in goals_pool:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"### {goal.title}")
                st.caption(f"🏷️ Category: `{goal.category}` | 📅 Deadline: {goal.deadline}")
                
            with col2:
                # Fixed Indentation & Star Mapping inside the layout block
                priority_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
                numeric_priority = priority_map.get(goal.priority, 1)
                priority_stars = "⭐" * numeric_priority
                st.markdown(f"**Priority:** {goal.priority}\n\n{priority_stars}")
                
            with col3:
                st.write("") # Padding
                if st.button("🗑️ Delete Goal", key=f"del_g_{goal.id}"):
                    delete_goal(goal.id)
                    st.success("Goal removed from active matrix.")
                    st.rerun()