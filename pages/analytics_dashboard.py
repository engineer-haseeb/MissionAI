import streamlit as st
import pandas as pd
from database import get_all_tasks, get_all_accountability_logs, get_all_goals

st.set_page_config(page_title="Analytics Center", layout="wide", page_icon="📊")

st.title("📊 Mission Intelligence & Analytics Control Panel")
st.caption("Productivity trends engine parsing sleep metrics, energy ratios, and core milestone task velocities.")

tasks = get_all_tasks()
logs = get_all_accountability_logs()
goals = get_all_goals()

# Convert data sets to Pandas objects for seamless mathematical transformations
df_tasks = pd.DataFrame([t.model_dump() for t in tasks]) if tasks else pd.DataFrame()
df_logs = pd.DataFrame([l.model_dump() for l in logs]) if logs else pd.DataFrame()

# ==========================================
# CRITICAL HIGH-LEVEL KPI METRICS
# ==========================================
c1, c2, c3 = st.columns(3)

if df_tasks.empty:
    c1.metric("Weekly Task Completion Rate", "0%")
    c2.metric("Total Hours Yielded", "0.0 Hrs")
    c3.metric("Goal Saturation Score", "0%")
else:
    done_count = len(df_tasks[df_tasks['kanban_status'] == 'Done'])
    rate = int((done_count / len(df_tasks)) * 100)
    c1.metric("Task Completion Rate", f"{rate}%", f"{done_count} Executed Tasks")
    
    total_hours = df_tasks[df_tasks['kanban_status'] == 'Done']['actual_time'].sum()
    c2.metric("Total Actual Invested Time", f"{total_hours:.1f} Hours", "Yielded")
    
    active_goals = len(goals)
    c3.metric("Strategic Managed Goals", f"{active_goals} Anchors", "Active")

st.markdown("---")

# ==========================================
# PROGRESSIVITY RENDERING MAPS
# ==========================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔥 Execution Volume by Priority Categories")
    if not df_tasks.empty:
        category_counts = df_tasks['category'].value_counts()
        st.bar_chart(category_counts)
    else:
        st.info("Insufficient backlog data arrays to map operational frequencies.")

with col_right:
    st.subheader("📈 Energy-Mood Correlation Logs Timeline")
    if not df_logs.empty:
        # Sort values by sequential timelines
        df_logs = df_logs.sort_values(by="log_date")
        chart_data = df_logs.set_index("log_date")[["morning_mood", "morning_energy", "sleep_hours"]]
        st.line_chart(chart_data)
    else:
        st.info("Submit continuous Morning/Night ledger logs to map correlation patterns.")

st.markdown("---")

# ==========================================
# BOTTLENECK ANALYSIS
# ==========================================
st.subheader("🔍 Friction Analysis Matrix (Missed Targets Analysis)")
if not df_logs.empty:
    missed_logs = df_logs[df_logs['night_missed_reason'].notna() & (df_logs['night_missed_reason'] != "")]
    if missed_logs.empty:
        st.success("Clean execution tracking records! Zero execution blockages noted.")
    else:
        for _, row in missed_logs.iterrows():
            with st.container(border=True):
                st.markdown(f"📅 **Timeline Milestone Date:** `{row['log_date']}`")
                st.markdown(f"💥 **Identified Bottleneck Pattern:** {row['night_missed_reason']}")
                if row['recovery_plan']:
                    st.info(f"🛡️ **Recovery Strategy Injected:** {row['recovery_plan']}")
else:
    st.info("Wipe out historical limits and input night logs to isolate processing bottlenecks.")