import streamlit as st
from database import init_db, add_task, get_all_tasks, update_task_status, get_all_goals

# Page Config Layout
st.set_page_config(page_title="MissionControlAI v1.0", page_icon="🚀", layout="wide")

# Database Initialization
init_db()

# Sidebar Configuration
st.sidebar.title("🤖 GEOS Engine")
st.sidebar.markdown("`Status: Active (Cloud)`")
st.sidebar.divider()
st.sidebar.write("💡 *AI Quote of the Day:*\n\"Abdul, execution counts over planning. Clear today's backlog!\"")

# Main Header
st.title("🚀 MissionControlAI")
st.markdown("##### Goal Execution Operating System (GEOS)")
st.divider()

# Core Data Fetching
tasks = get_all_tasks()
goals = get_all_goals()

# Analytics Metric Layer Calculations
total_tasks = len(tasks)
completed_tasks = sum(1 for t in tasks if t.is_completed)
mission_score = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 100

# Metric Row Display
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Mission Score", f"{mission_score}%")
col2.metric("🎯 Total Active Goals", f"{len(goals)}")
col3.metric("📝 Pending Tasks", f"{total_tasks - completed_tasks}")
col4.metric("⏳ Total Focus Hours", f"{sum(t.estimated_time for t in tasks if t.is_completed)} hrs")

st.divider()

# Layout Distribution Columns
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("🎯 Today's Execution Stack")
    
    # Task Submission Box
    with st.expander("➕ Deploy New Mission Task", expanded=False):
        with st.form("task_sub_form", clear_on_submit=True):
            t_title = st.text_input("Task Title", placeholder="e.g., Read Section 3 of Edge Computing Paper")
            
            # Map with goals dynamically if available
            goal_options = {g.title: g.id for g in goals} if goals else {}
            selected_goal = st.selectbox("Link to Strategic Goal (Optional)", ["None"] + list(goal_options.keys()))
            
            c1, c2, c3 = st.columns(3)
            t_cat = c1.selectbox("Category", ["Research", "Cloud AI", "HSK4", "Gym", "Life Management"])
            t_priority = c2.selectbox("Priority", ["High", "Medium", "Low"])
            t_time = c3.number_input("Estimated Time (Hours)", min_value=0.5, max_value=12.0, value=1.0, step=0.5)
            
            if st.form_submit_button("Deploy Task") and t_title:
                g_id = goal_options[selected_goal] if selected_goal != "None" else None
                add_task(t_title, t_cat, t_priority, g_id, t_time)
                st.toast("Mission task deployed successfully!", icon="🚀")
                st.rerun()

    # Tasks Rendering Logic
    if not tasks:
        st.info("System operational. No tasks added yet.")
    else:
        for task in tasks:
            status_check = st.checkbox(
                f"**[{task.category}]** {task.title} — *({task.priority} Priority, {task.estimated_time}h)*", 
                value=task.is_completed, 
                key=f"task_key_{task.id}"
            )
            if status_check != task.is_completed:
                update_task_status(task.id, status_check)
                st.rerun()

with right_col:
    st.subheader("📊 Execution Progress")
    if total_tasks > 0:
        st.progress(completed_tasks / total_tasks)
        st.write(f"**Completion Analytics:** {completed_tasks}/{total_tasks} Missions Cleared")
    else:
        st.progress(0.0)
        st.write("No operational tracking payload loaded.")