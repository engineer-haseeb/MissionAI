import streamlit as st
from database import init_db, add_task, get_all_tasks, update_task_status

st.set_page_config(page_title="Mission Control OS", page_icon="🚀", layout="wide")

init_db()

st.title("🚀 Mission Control OS")
st.markdown("### Welcome back, Abdul Haseeb.")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Mission Score", "92%")
col2.metric("📄 Paper Submission", "89 Days")
col3.metric("🇺🇸 USA PhD Apps", "145 Days")
col4.metric("🏅 ANSO Deadline", "183 Days")
st.divider()

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("🎯 Today's Mission")
    with st.expander("➕ Add New Task", expanded=True):
        with st.form("task_form", clear_on_submit=True):
            title = st.text_input("Task Title")
            category = st.selectbox("Category", ["Research", "Cloud AI", "HSK4", "Gym"])
            if st.form_submit_button("Add Task") and title:
                add_task(title, category)
                st.rerun()

    tasks = get_all_tasks()
    if not tasks:
        st.info("No tasks added yet.")
    else:
        for task in tasks:
            chk = st.checkbox(f"**[{task.category}]** {task.title}", value=task.is_completed, key=f"t_{task.id}")
            if chk != task.is_completed:
                update_task_status(task.id, chk)
                st.rerun()

with right_col:
    st.subheader("💡 Progress Tracker")
    if tasks:
        comp = sum(1 for t in tasks if t.is_completed)
        st.progress(comp / len(tasks))
        st.write(f"{comp}/{len(tasks)} Completed")