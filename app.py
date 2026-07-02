import streamlit as st
from database import init_db, create_user, authenticate_user, get_user_tasks, get_user_goals, add_task, update_task_status

st.set_page_config(page_title="MissionControlAI v1.0", page_icon="🚀", layout="wide")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================================
# GATEKEEPER LAYER
# ==========================================
if not st.session_state.logged_in:
    st.title("🔐 MissionControlAI Gatekeeper")
    st.markdown("##### Enterprise Goal Execution Operating System (GEOS)")
    st.divider()
    
    auth_tab, signup_tab = st.tabs(["🔑 Sign In", "📝 Create Secure Account"])
    
    with auth_tab:
        with st.form("login_form"):
            user_input = st.text_input("Username / Email")
            pass_input = st.text_input("Password", type="password")
            if st.form_submit_button("Authenticate"):
                user = authenticate_user(user_input, pass_input)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user.id
                    st.session_state.username = user.username
                    st.success(f"Handshake successful. Welcome {user.username}!")
                    st.rerun()
                else:
                    st.error("Access Denied. Invalid credentials.")
                    
    with signup_tab:
        with st.form("signup_form"):
            new_user = st.text_input("Choose Unique Username")
            new_pass = st.text_input("Secure Password", type="password")
            if st.form_submit_button("Register Core Account"):
                if new_user and new_pass:
                    success = create_user(new_user, new_pass)
                    if success:
                        st.success("Account provisioned! Switch to Sign In tab.")
                    else:
                        st.error("Username allocation conflict. Try another identifier.")

# ==========================================
# APP EXECUTION LOOP (POST LOGIN)
# ==========================================
else:
    st.sidebar.title("🤖 GEOS Engine")
    st.sidebar.markdown(f"`User: {st.session_state.username.upper()}`")
    st.sidebar.markdown("`Status: Multi-Tenant Active`")
    if st.sidebar.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.rerun()
        
    st.sidebar.divider()
    st.sidebar.write("💡 *AI Quote:*\n\"Abdul, execution counts over planning.\"")

    st.title("🚀 MissionControlAI")
    st.markdown(f"### Welcome back, {st.session_state.username}.")
    st.divider()

    tasks = get_user_tasks(st.session_state.user_id)
    goals = get_user_goals(st.session_state.user_id)

    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.is_completed)
    mission_score = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Mission Score", f"{mission_score}%")
    col2.metric("🎯 Active Goals", f"{len(goals)}")
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
                    add_task(t_title, t_cat, t_priority, st.session_state.user_id, g_id, t_time)
                    st.toast("Task provisioned into your secure space!")
                    st.rerun()

        if not tasks:
            st.info("No localized operational payload loaded.")
        else:
            for task in tasks:
                status_check = st.checkbox(f"**[{task.category}]** {task.title} — *({task.priority}, {task.estimated_time}h)*", value=task.is_completed, key=f"t_key_{task.id}")
                if status_check != task.is_completed:
                    update_task_status(task.id, status_check)
                    st.rerun()

    with right_col:
        st.subheader("📊 Execution Progress")
        if total_tasks > 0:
            st.progress(completed_tasks / total_tasks)
            st.write(f"**Completion:** {completed_tasks}/{total_tasks} Missions Cleared")
        else:
            st.progress(0.0)