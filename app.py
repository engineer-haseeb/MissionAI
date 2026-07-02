import streamlit as st
import datetime
from database import init_db, get_all_goals, add_goal, get_all_tasks, add_task, update_kanban_status, get_accountability_log, set_morning_checkin, set_night_review

st.set_page_config(page_title="MissionControlAI v4.0", layout="wide", page_icon="🚀")
init_db()

today_str = datetime.date.today().strftime("%Y-%m-%d")

# ==========================================
# HEADER SCOREBOARD
# ==========================================
all_tasks = get_all_tasks()
done_tasks = [t for t in all_tasks if t.kanban_status == "Done"]
todo_tasks = [t for t in all_tasks if t.kanban_status == "Todo"]

mission_score = int((len(done_tasks) / len(all_tasks) * 100)) if all_tasks else 100

st.title("🚀 MissionControlAI — AI Chief of Staff Terminal")
st.caption("Integrated Core: Strategic Planning, Cross-Border Scholarship Operations & Adaptive Accountability Engines")

# Metrics Banner
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("🎯 Mission Score Formula", f"{mission_score}%", delta=f"{len(done_tasks)} Done")
m_col2.metric("📋 Active Core Backlog", f"{len(todo_tasks)} Tasks", "Pending")
m_col3.metric("🔥 System Consistency Streak", "14 Days", "Target: 30")
m_col4.metric("💡 AI Strategic Command", "Continuous Momentum", "Optimal")

st.markdown("---")

# ==========================================
# STRATEGIC ACCOUNTABILITY ENGINE
# ==========================================
st.subheader("🛡️ Strategic Accountability Engine")
acc_col1, acc_col2 = st.columns(2)

current_log = get_accountability_log(today_str)

with acc_col1:
    with st.expander("🌅 Morning Alignment Check-in", expanded=not bool(current_log)):
        with st.form("morning_form"):
            sleep_h = st.slider("Sleep Duration (Hours)", 4.0, 12.0, 7.0, step=0.5)
            mood_s = st.select_slider("Current Mood State", options=[1, 2, 3, 4, 5], value=4)
            energy_s = st.select_slider("Energy Vitality Index", options=[1, 2, 3, 4, 5], value=4)
            free_h = st.number_input("Available Velocity Today (Free Hours)", min_value=1.0, max_value=16.0, value=5.0)
            
            if st.form_submit_button("Log Morning Metrics"):
                set_morning_checkin(today_str, sleep_h, mood_s, energy_s, free_h)
                st.success("Daily velocity profile locked into AI memory!")
                st.rerun()

with acc_col2:
    with st.expander("🌃 Night Execution Review", expanded=False):
        with st.form("night_form"):
            completed_c = st.number_input("Confirmed Executed Tasks", min_value=0, step=1)
            missed_r = st.text_area("Why were certain objectives missed? (Bottleneck Analysis)", placeholder="e.g., Environment configuration dependencies taking time...")
            recovery_s = st.text_area("Proactive Contingency Recovery Plan", placeholder="e.g., Shifting 45m deep session to tomorrow morning...")
            
            if st.form_submit_button("Close Daily Ledger"):
                set_night_review(today_str, completed_c, missed_r, recovery_s)
                st.success("Day logged. AI coach is updating scheduling optimization arrays.")
                st.rerun()

st.markdown("---")

# ==========================================
# SMART AI DAILY PLANNER
# ==========================================
st.subheader("🤖 Dynamic AI Daily Scheduler Engine")
if current_log:
    avail_hours = current_log.available_hours
    st.info(f"⚡ **AI Engine Active:** System detected **{avail_hours} hours** of free velocity for today's assignment run.")
    
    schedulable_tasks = [t for t in all_tasks if t.kanban_status in ["Todo", "In Progress"]]
    
    if schedulable_tasks:
        accumulated_time = 0.0
        st.markdown("**Your Custom High-Yield Allocation Schedule for Today:**")
        
        for task in schedulable_tasks:
            if accumulated_time + task.estimated_time <= avail_hours:
                st.checkbox(f"⏱️ **{task.estimated_time}h** — {task.title} `[{task.category}]`", value=False, key=f"sched_{task.id}")
                accumulated_time += task.estimated_time
        
        if accumulated_time == 0.0:
            st.warning("No individual task fits within your available time window. Break down your task estimations!")
    else:
        st.success("No backlog tasks remaining! Add fresh execution triggers below.")
else:
    st.warning("Please submit your Morning Check-in context above to trigger the dynamic optimization scheduler.")

st.markdown("---")

# ==========================================
# RESTRUCTURED VISUAL KANBAN
# ==========================================
st.subheader("📋 Core Execution Matrix (Visual Kanban)")
cols_meta = [
    {"status": "Todo", "icon": "📝"},
    {"status": "In Progress", "icon": "⚡"},
    {"status": "Blocked", "icon": "⚠️"},
    {"status": "Done", "icon": "✅"}
]

kanban_columns = st.columns(4)
for idx, meta in enumerate(cols_meta):
    with kanban_columns[idx]:
        st.markdown(f"#### {meta['icon']} {meta['status']}")
        filtered = [t for t in all_tasks if t.kanban_status == meta['status']]
        
        for t in filtered:
            with st.container(border=True):
                st.markdown(f"**{t.title}**")
                st.caption(f"🏷️ {t.category} | ⏱️ {t.estimated_time}h | ⚠️ {t.priority}")
                if t.due_date:
                    st.caption(f"📅 Due: {t.due_date}")
                
                nav_targets = [m['status'] for m in cols_meta if m['status'] != meta['status']]
                btn_cols = st.columns(len(nav_targets))
                for b_idx, target in enumerate(nav_targets):
                    if btn_cols[b_idx].button(f"➔ {target[:4]}", key=f"nav_{t.id}_{target}"):
                        # If moving to done, record default actual time equal to estimated
                        actual_duration = t.estimated_time if target == "Done" else 0.0
                        update_kanban_status(t.id, target, actual_time=actual_duration)
                        st.rerun()

st.markdown("---")

# ==========================================
# CONFIGURATION INGESTION DESK
# ==========================================
st.subheader("⚙️ Quick Configuration Desk")
col_g, col_t = st.columns(2)

with col_g:
    with st.expander("🎯 Launch Strategic Goal Asset", expanded=False):
        with st.form("goal_form_main", clear_on_submit=True):
            g_title = st.text_input("Strategic Target Objective")
            g_cat = st.selectbox("Strategic Category Focus", ["Research", "PhD", "Scholarship", "Learning", "Health", "Finance", "Personal"])
            g_prio = st.selectbox("Priority Class", ["Critical", "High", "Medium", "Low"])
            g_dead = st.date_input("Target Goal Deadline", value=datetime.date.today() + datetime.timedelta(days=90))
            if st.form_submit_button("Deploy Goal Asset"):
                if g_title:
                    add_goal(g_title, g_cat, g_prio, g_dead)
                    st.success("Goal synchronized with core matrix!")
                    st.rerun()

with col_t:
    with st.expander("🔨 Inject Operational Task Trigger", expanded=False):
        goals_pool = get_all_goals()
        g_map = {g.id: f"[{g.category}] {g.title}" for g in goals_pool}
        
        with st.form("task_form_main", clear_on_submit=True):
            t_title = st.text_input("Task Label/Description")
            t_cat = st.text_input("Functional Area Module Code", placeholder="e.g., Python Engine Run")
            t_prio = st.selectbox("Priority Vector", ["High", "Medium", "Low"])
            t_est = st.number_input("Estimated Duration Weights (Hours)", min_value=0.5, value=1.5, step=0.5)
            t_due = st.date_input("Task Internal Target Date", value=datetime.date.today())
            t_gid = st.selectbox("Map to Goal Dependency", options=[None] + list(g_map.keys()), format_func=lambda x: "Independent Task" if x is None else g_map[x])
            
            if st.form_submit_button("Deploy Task to Kanban"):
                if t_title and t_cat:
                    add_task(t_title, t_cat, t_prio, t_gid, t_est, t_due)
                    st.success("Task triggered and stacked into pipeline matrix!")
                    st.rerun()