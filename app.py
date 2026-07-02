import streamlit as st
import datetime
from database import (
    init_db, get_all_goals, add_goal, get_all_tasks, add_task, 
    update_kanban_status, get_accountability_log, set_morning_checkin, 
    set_night_review, compile_automated_alerts, get_active_alerts, 
    dismiss_alert_signal, get_all_memory_insights, upsert_ai_memory
)

# Page Setup Layout Configuration
st.set_page_config(page_title="MissionControlAI v5.0", layout="wide", page_icon="🚀")

# 1. RUN ENGINE INITIALIZATION
init_db()
compile_automated_alerts() # Scan database autonomously on startup for overdue limits

today_str = datetime.date.today().strftime("%Y-%m-%d")

# ==========================================
# MODULE 16: TOP-TIER NOTIFICATION SYSTEMS HUB
# ==========================================
active_alerts = get_active_alerts()

if active_alerts:
    st.markdown("### 🔔 System Security Alerts Desk")
    for alert in active_alerts:
        # Style layout contextually by alert gravity
        if alert.alert_type == "Overdue":
            with st.error_wrapper(f"🛑 **{alert.title}** — {alert.message}") if hasattr(st, 'error_wrapper') else st.error(f"🛑 **{alert.title}** — {alert.message}"):
                if st.button("Dismiss Alert Instance", key=f"dism_{alert.id}"):
                    dismiss_alert_signal(alert.id)
                    st.rerun()
        else:
            with st.warning(f"⚠️ **{alert.title}** — {alert.message}"):
                if st.button("Dismiss Alert Instance", key=f"dism_{alert.id}"):
                    dismiss_alert_signal(alert.id)
                    st.rerun()
    st.markdown("---")

# ==========================================
# CORE SCOREBOARD TELEMETRY
# ==========================================
all_tasks = get_all_tasks()
done_tasks = [t for t in all_tasks if t.kanban_status == "Done"]
todo_tasks = [t for t in all_tasks if t.kanban_status == "Todo"]

mission_score = int((len(done_tasks) / len(all_tasks) * 100)) if all_tasks else 100

st.title("🚀 MissionControlAI — Enterprise Execution Suite")
st.caption("AI Chief of Staff Control Grid | Live Pipeline Synchronization")

# Main Metrics Layout Rows
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("🎯 Mission Score Performance", f"{mission_score}%", delta=f"{len(done_tasks)} Objectives Cleared")
m_col2.metric("📋 Pipeline Backlog Weight", f"{len(todo_tasks)} Tasks", "Pending Run")
m_col3.metric("🔥 System Consistency Streak", "14 Days Continuous", "Target: 30")
m_col4.metric("🧠 Cognitive State Tracker", "Adaptive Context Active", "Stable")

st.markdown("---")

# ==========================================
# MODULE 17: SYSTEM AI MEMORY PROFILE DRAWER
# ==========================================
with st.sidebar:
    st.markdown("### 🧠 Autonomous AI Memory Ledger")
    st.caption("Structured habits, past execution tracking bottlenecks, and recurring productivity vectors.")
    
    # Ingestion point for manual long-term cognitive settings
    with st.expander("📝 Inject Custom Habits/Weaknesses Traits", expanded=False):
        with st.form("mem_inject_form", clear_on_submit=True):
            m_type = st.selectbox("Trait Category Matrix", ["Habit", "Weakness", "Strength", "WorkingHour", "LongTerm"])
            m_key = st.text_input("Identity Descriptor Code", placeholder="e.g., HSK4 Consistency Pattern")
            m_val = st.text_area("Insight Behavioral Description", placeholder="e.g., Slacks documentation execution streams during weekend frames...")
            
            if st.form_submit_button("Commit to AI Core Memory"):
                if m_key and m_val:
                    upsert_ai_memory(m_type, m_key, m_val)
                    st.success("Trait successfully stored into systemic profile memory.")
                    st.rerun()
                    
    # Display running structural memory logs
    memories = get_all_memory_insights()
    if not memories:
        st.info("System AI memory cells are currently building context parameters.")
    else:
        for mem in memories:
            with st.container(border=True):
                icon = "🔥" if mem.memory_type == "Strength" else "⚠️" if mem.memory_type == "Weakness" else "⏳"
                st.markdown(f"**{icon} {mem.key_concept}**")
                st.caption(f"`[{mem.memory_type}]` — {mem.insight_value}")

# ==========================================
# STRATEGIC ACCOUNTABILITY SYSTEMS
# ==========================================
st.subheader("🛡️ Strategic Accountability Engine Logs Desk")
acc_col1, acc_col2 = st.columns(2)

current_log = get_accountability_log(today_str)

with acc_col1:
    with st.expander("🌅 Morning Alignment Tracker Ingestion", expanded=not bool(current_log)):
        with st.form("morning_form"):
            sleep_h = st.slider("Sleep Duration Volume Metrics", 4.0, 12.0, 7.0, step=0.5)
            mood_s = st.select_slider("Current Psychological Focus Index", options=[1, 2, 3, 4, 5], value=4)
            energy_s = st.select_slider("Energy Reservoir Vitality Velocity", options=[1, 2, 3, 4, 5], value=4)
            free_h = st.number_input("Available Dynamic Velocity Allocation (Free Hours)", min_value=1.0, max_value=16.0, value=5.0)
            
            if st.form_submit_button("Lock Morning Vector Baseline"):
                set_morning_checkin(today_str, sleep_h, mood_s, energy_s, free_h)
                st.toast("Morning velocity matrix locked into telemetry buffers.")
                st.rerun()

with acc_col2:
    with st.expander("🌃 Night Execution Ledger Closures", expanded=False):
        with st.form("night_form"):
            completed_c = st.number_input("Verified Cleared Pipeline Checkboxes", min_value=0, step=1)
            missed_r = st.text_area("Encountered Friction / Bottleneck Analysis Log Entries", placeholder="Detail why certain goals shifted off-track...")
            recovery_s = st.text_area("Proactive Contingency Recovery Injections", placeholder="Detail exactly how schedule gaps will be reclaimed...")
            
            if st.form_submit_button("Close Daily Operational Cycle"):
                set_night_review(today_str, completed_c, missed_r, recovery_s)
                st.toast("Ledger closed. Autonomic profiling script parsed successfully.")
                st.rerun()

st.markdown("---")

# ==========================================
# SMART AI DAILY PLANNER
# ==========================================
st.subheader("🤖 Dynamic AI Daily Scheduler Engine")
if current_log:
    avail_hours = current_log.available_hours
    st.info(f"⚡ **AI Engine Status Running:** System registered **{avail_hours} working hours** for today's automated pipeline sequence.")
    
    # ADAPTIVE COGNITIVE SCHEDULING WITH MEMORY OVERLAY
    st.markdown("##### 🧠 Context-Aware Memory Guidelines Override:")
    bottleneck_mem = [m for m in memories if m.key_concept == "Recent Core Bottleneck Analysis"]
    if bottleneck_mem:
        st.warning(f"👉 **AI Agent Warning:** {bottleneck_mem[0].insight_value} — Adjust task focus parameters safely to override historical lag blocks!")
    else:
        st.success("👉 **AI Agent Strategy Guidance:** Clean historical velocity loops detected. Drive high-yield critical weights first.")
        
    schedulable_tasks = [t for t in all_tasks if t.kanban_status in ["Todo", "In Progress"]]
    
    if schedulable_tasks:
        accumulated_time = 0.0
        st.markdown("**Your Smart High-Yield Allocation Matrix for Today:**")
        
        for task in schedulable_tasks:
            if accumulated_time + task.estimated_time <= avail_hours:
                st.checkbox(f"⏱️ **{task.estimated_time} Hours** — {task.title} `[{task.category}]`", value=False, key=f"sched_{task.id}")
                accumulated_time += task.estimated_time
        
        if accumulated_time == 0.0:
            st.warning("No individual standalone backlog item fits inside your current free time metrics profile layout.")
    else:
        st.success("Execution queue completely cleared! Inject new task triggers to allocate resources.")
else:
    st.warning("Please submit your Morning Check-in alignment tracking values to spin up the smart dynamic layout scheduler.")

st.markdown("---")

# ==========================================
# INTERACTIVE VISUAL KANBAN MATRIX
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
                st.caption(f"🏷️ {t.category} | ⏱️ {t.estimated_time}h | Priority: **{t.priority}**")
                if t.due_date:
                    st.caption(f"📅 Limit: {t.due_date}")
                
                # Dynamic shifting mechanisms
                nav_targets = [m['status'] for m in cols_meta if m['status'] != meta['status']]
                btn_cols = st.columns(len(nav_targets))
                for b_idx, target in enumerate(nav_targets):
                    if btn_cols[b_idx].button(f"➔ {target[:4]}", key=f"nav_{t.id}_{target}"):
                        actual_dur = t.estimated_time if target == "Done" else 0.0
                        update_kanban_status(t.id, target, actual_time=actual_dur)
                        st.rerun()

st.markdown("---")

# ==========================================
# CORE INGESTION DESK UNITS
# ==========================================
st.subheader("⚙️ Quick Configuration Desk")
col_g, col_t = st.columns(2)

with col_g:
    with st.expander("🎯 Launch Strategic Goal Asset Framework", expanded=False):
        with st.form("goal_form_main", clear_on_submit=True):
            g_title = st.text_input("Strategic Target Objective")
            g_cat = st.selectbox("Strategic Category Focus", ["Research", "PhD", "Scholarship", "Learning", "Health", "Finance", "Personal"])
            g_prio = st.selectbox("Priority Class Weights Scale", ["Critical", "High", "Medium", "Low"])
            g_dead = st.date_input("Target Goal Absolute Deadline Line", value=datetime.date.today() + datetime.timedelta(days=90))
            if st.form_submit_button("Deploy Strategic Goal Asset"):
                if g_title:
                    add_goal(g_title, g_cat, g_prio, g_dead)
                    st.success("Strategic asset successfully tracked into framework registers!")
                    st.rerun()

with col_t:
    with st.expander("🔨 Inject Operational Task Trigger Parameter", expanded=False):
        goals_pool = get_all_goals()
        g_map = {g.id: f"[{g.category}] {g.title}" for g in goals_pool}
        
        with st.form("task_form_main", clear_on_submit=True):
            t_title = st.text_input("Task Label Blueprint")
            t_cat = st.text_input("Functional Area Module Code Tag", placeholder="e.g., Python Architecture Code Run")
            t_prio = st.selectbox("Priority Execution Vector", ["High", "Medium", "Low"])
            t_est = st.number_input("Estimated Duration Resources Weight (Hours)", min_value=0.5, value=1.5, step=0.5)
            t_due = st.date_input("Task Internal Target Deadline Date", value=datetime.date.today())
            t_gid = st.selectbox("Map to Goal Structural Dependency", options=[None] + list(g_map.keys()), format_func=lambda x: "Independent Execution Unit" if x is None else g_map[x])
            
            if st.form_submit_button("Deploy Operational Task to Kanban Matrix"):
                if t_title and t_cat:
                    add_task(t_title, t_cat, t_prio, t_gid, t_est, t_due)
                    st.success("Operational execution parameter routed into active system lists!")
                    st.rerun()