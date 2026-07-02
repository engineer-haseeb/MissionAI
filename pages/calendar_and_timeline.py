import streamlit as st
import datetime
from database import get_all_goals, get_all_tasks

st.set_page_config(page_title="Calendar & Timelines", layout="wide", page_icon="📅")

st.title("📅 Central Calendar & Mission Timelines Matrix")
st.caption("Synchronized view tracking long-term strategic milestones alongside immediate engineering task deadlines.")

goals = get_all_goals()
tasks = get_all_tasks()

t1, t2 = st.tabs(["🗓️ Milestone & Goal Deadline Matrix", "📋 Immediate Tasks Queue Calendar"])

with t1:
    st.subheader("🎯 Macro Milestones & Deadlines")
    active_deadlines = [g for g in goals if g.deadline]
    
    if not active_deadlines:
        st.info("No active goal target timelines declared yet.")
    else:
        # Sort based on closest deadline
        active_deadlines.sort(key=lambda x: x.deadline)
        
        for idx, g in enumerate(active_deadlines):
            days_left = (g.deadline - datetime.date.today()).days
            
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"#### 🏆 `{g.category}` — {g.title}")
                c2.markdown(f"📅 Target: **{g.deadline}**")
                
                if days_left < 0:
                    c3.error(f"⚠️ Overdue by {abs(days_left)} days")
                elif days_left <= 7:
                    c3.warning(f"🚨 Critical: {days_left} Days Left")
                else:
                    c3.success(f"🔋 Safe: {days_left} Days Remaining")

with t2:
    st.subheader("📋 Task Deadline Ledger & Weekly View")
    
    day_filter = st.radio("Calendar Proximity Filter", ["All Pending Tasks", "Due Today / Overdue Tasks"], horizontal=True)
    
    pending_tasks = [t for t in tasks if t.kanban_status != "Done" and t.due_date]
    pending_tasks.sort(key=lambda x: x.due_date)
    
    if not pending_tasks:
        st.success("No task deadlines logged in the backlog queue dashboard!")
    else:
        for t in pending_tasks:
            is_today = t.due_date == datetime.date.today()
            is_overdue = t.due_date < datetime.date.today()
            
            if day_filter == "Due Today / Overdue Tasks" and not (is_today or is_overdue):
                continue
                
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                col1.markdown(f"**{t.title}** `[{t.category}]`")
                col2.caption(f"⏱️ Est: {t.estimated_time}h | Priority: {t.priority}")
                
                if is_overdue:
                    col3.markdown(f"🔴 **Overdue ({t.due_date})**")
                elif is_today:
                    col3.markdown(f"🟡 **DUE TODAY**")
                else:
                    col3.markdown(f"🟢 Due: {t.due_date}")