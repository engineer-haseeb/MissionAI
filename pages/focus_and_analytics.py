import streamlit as st
import time
from sqlmodel import Session, select
import sys
import os

# Root directory se structures extract karne ke liye connection setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine, Task, Goal

st.set_page_config(page_title="Focus & Analytics Engine", page_icon="📊", layout="wide")

st.title("📊 Focus & Execution Analytics Engine")
st.markdown("##### Real-time processing loops tracking deep attention sessions and core dataset distribution.")
st.divider()

# Core Session Synchronization
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "time_left" not in st.session_state:
    st.session_state.time_left = 25 * 60  # Default 25 Minutes Session

# Layout Columns
left_col, right_col = st.columns([1, 1])

# ==========================================
# MODULE 6: POMODORO & DEEP WORK TIMER
# ==========================================
with left_col:
    st.subheader("⏱️ Deep Work Synchronization Hub")
    st.caption("Activate hardware isolated time slicing loops for context-specific deep work.")
    
    # Custom adjustments for session
    session_minutes = st.number_input("Configure Focus Interval (Minutes)", min_value=1, max_value=120, value=25, step=5)
    
    # Reset tracking state if input parameters change dynamically
    if st.button("Set/Reset Timer Configuration"):
        st.session_state.time_left = session_minutes * 60
        st.session_state.timer_running = False
    
    # Digital Clock Formatting Output
    mins, secs = divmod(st.session_state.time_left, 60)
    timer_placeholder = st.empty()
    timer_placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #FF4B4B;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    if c1.button("▶️ Initialize Session", use_container_width=True):
        st.session_state.timer_running = True
    if c2.button("⏸️ Terminate/Pause", use_container_width=True):
        st.session_state.timer_running = False

    # Execution Loop Hook
    if st.session_state.timer_running and st.session_state.time_left > 0:
        while st.session_state.time_left > 0 and st.session_state.timer_running:
            time.sleep(1)
            st.session_state.time_left -= 1
            mins, secs = divmod(st.session_state.time_left, 60)
            timer_placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #FF4B4B;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        if st.session_state.time_left == 0:
            st.balloons()
            st.success("Session completed! Highly localized work vector stored.")
            st.session_state.timer_running = False

# ==========================================
# MODULE 8: ADVANCED DATASET ANALYTICS
# ==========================================
with right_col:
    st.subheader("📈 Core Category Allocation Mapping")
    st.caption("Quantitative telemetry tracking the distribution of computational resource allocation across life vectors.")
    
    with Session(engine) as session:
        all_tasks = session.exec(select(Task)).all()
        
    if not all_tasks:
        st.info("Dataset empty. Feed raw inputs on the primary execution dashboard to parse performance data.")
    else:
        # Category tracking map structures
        cat_data = {}
        for t in all_tasks:
            cat_data[t.category] = cat_data.get(t.category, {"total": 0, "done": 0, "hours": 0.0})
            cat_data[t.category]["total"] += 1
            if t.is_completed:
                cat_data[t.category]["done"] += 1
                cat_data[t.category]["hours"] += t.estimated_time
                
        # Matrix Table rendering
        st.write("**Operational Domain Decompositions:**")
        
        table_rows = []
        for cat, metrics in cat_data.items():
            comp_rate = (metrics["done"] / metrics["total"]) * 100 if metrics["total"] > 0 else 0
            table_rows.append({
                "Operational Vector": cat,
                "Total Deployments": metrics["total"],
                "Missions Executed": metrics["done"],
                "Success Matrix (%)": f"{int(comp_rate)}%",
                "Dedicated Load (Hrs)": f"{metrics['hours']} hrs"
            })
            
        st.table(table_rows)
        
        # Micro Summary Report Generator
        total_accumulated_hours = sum(m["hours"] for m in cat_data.values())
        st.metric("📦 Gross Accumulated Kinetic Focus Load", f"{total_accumulated_hours} Hours Worked")