import streamlit as st
from database import init_db, add_task, get_all_tasks, get_all_goals, update_task_status

st.set_page_config(page_title="MissionControlAI v1.0", page_icon="🚀", layout="wide")
init_db()

# Sidebar Setup
st.sidebar.title("🤖 GEOS Executive Engine")
st.sidebar.markdown("`User: ABDUL HASEEB`")
st.sidebar.markdown("`Status: Personal Assistant Active`")
st.sidebar.divider()
st.sidebar.write("💡 *Executive Directive:*\n\"Focus entirely on execution. Prune the backlog loops today.\"")

# Main Interface
st.title("🚀 MissionControlAI Dashboard")
st.markdown("##### Abdul Haseeb's Core Goal & Academic Operating System.")
st.divider()

# Load Global Datasets
tasks = get_all_tasks()
goals = get_all_goals()

# Analytics Telemetry
total_tasks = len(tasks)
completed_tasks = sum(1 for t in tasks if t.is_completed)
mission_score = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Personal Mission Score", f"{mission_score}%")
col2.metric("🎯 Strategic Goals", f"{len(goals)}")
col3.metric("📝 Pending Tasks", f"{total_tasks - completed_tasks}")
col4.metric("⏳ Spent Load", f"{sum(t.estimated_time for t in tasks if t.is_completed)} hrs")
st.divider()

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("🎯 Today's Execution Stack")
    with st.expander("➕ Deploy New Mission Task", expanded=False):
        with st.form("task_sub_form", clear_on_submit=True):
            t_title = st.text_input("Task Title")
            goal_options = {g.title: g.id for g in goals} if goals else {}
            selected_goal = st.selectbox("Link to Strategic Goal (Optional)", ["None"] + list(goal_options.keys()))
            
            c1, c2, c3 = st.columns(3)
            t_cat = c1.selectbox("Category", ["Research", "Cloud AI", "HSK4", "Gym", "Life Management"])
            t_priority = c2.selectbox("Priority", ["High", "Medium", "Low"])
            t_time = c3.number_input("Estimated Time (Hours)", min_value=0.5, max_value=12.0, value=1.0, step=0.5)
            
            if st.form_submit_button("Deploy Task") and t_title:
                g_id = goal_options[selected_goal] if selected_goal != "None" else None
                add_task(t_title, t_cat, t_priority, goal_id=g_id, est_time=t_time)
                st.toast("Task successfully registered into your control matrix!")
                st.rerun()

    if not tasks:
        st.info("No operational payload loaded in the execution stack.")
    else:
        for task in tasks:
            status_check = st.checkbox(f"**[{task.category}]** {task.title} — *({task.priority}, {task.estimated_time}h)*", value=task.is_completed, key=f"t_key_{task.id}")
            if status_check != task.is_completed:
                update_task_status(task.id, status_check)
                st.rerun()

with right_col:
    st.subheader("📊 Execution Vector Tracking")
    if total_tasks > 0:
        st.progress(completed_tasks / total_tasks)
        st.write(f"**Metrics:** {completed_tasks}/{total_tasks} Missions Closed")
    else:
        st.progress(0.0)