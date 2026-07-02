import streamlit as st
from sqlmodel import Session, select
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine, add_scholarship, get_all_scholarships, add_phd_target, get_all_phd_targets, update_email_status

st.set_page_config(page_title="Academic Execution Radar", page_icon="🎓", layout="wide")

st.title("🎓 Academic Execution Radar")
st.markdown("##### Central pipeline for Funding Scholarships, Professor Communication, and Ph.D. Applications Profiles.")
st.divider()

# Multi-Tabs interface for modular clean look
tab1, tab2 = st.tabs(["🏅 Scholarship Funding Pipeline", "🔍 Ph.D. Professor Cold-Email Radar"])

# ==========================================
# TAB 1: SCHOLARSHIP TRACKER
# ==========================================
with tab1:
    st.subheader("Funding & Scholarship Pipelines")
    
    with st.expander("➕ Track New Scholarship Scheme", expanded=False):
        with st.form("sch_form", clear_on_submit=True):
            s_name = st.text_input("Scholarship Name", placeholder="e.g., ANSO Fellowship, CSC Scholarship Type A")
            s_country = st.text_input("Host Country/Region", value="China")
            s_deadline = st.text_input("Application Deadline Date", value="2027-03-01")
            s_status = st.selectbox("Current Tracking Pipeline Status", ["Drafting", "Applied", "Shortlisted", "Accepted", "Rejected"])
            s_notes = st.text_area("Critical Entry Requirements / Notes")
            
            if st.form_submit_button("Log Scholarship Matrix") and s_name:
                add_scholarship(s_name, s_country, s_deadline, s_status, s_notes)
                st.toast("Scholarship tracker configuration serialized!", icon="🏅")
                st.rerun()

    # Render Scholarships
    s_list = get_all_scholarships()
    if not s_list:
        st.info("No scholarship metrics loaded yet.")
    else:
        for sch in s_list:
            with st.container():
                c1, c2, c3 = st.columns([2, 2, 1])
                c1.markdown(f"#### **{sch.name}** ({sch.country})")
                c2.markdown(f"⏳ **Deadline:** `{sch.deadline}` | Status: `{sch.status}`")
                if sch.notes:
                    st.caption(f"📝 *Requirements Notes:* {sch.notes}")
                st.divider()

# ==========================================
# TAB 2: PHD PROFESSOR COLD-EMAIL RADAR
# ==========================================
with tab2:
    st.subheader("Ph.D. Academic Radar & Communication Logs")
    
    with st.expander("➕ Log Professor / University Profile Target", expanded=False):
        with st.form("phd_form", clear_on_submit=True):
            p_univ = st.text_input("Target University Name", placeholder="e.g., Tsinghua University, National University of Singapore")
            p_name = st.text_input("Professor Name")
            p_email = st.text_input("Professor Email Coordinates")
            p_status = st.selectbox("Cold-Email Handshake Status", ["Not Sent", "Cold Email Sent", "Replied (Positive)", "Replied (Negative)", "Interview Scheduled"])
            p_notes = st.text_area("Research Alignment Notes (e.g., Working on Federated Learning / Latency)")
            
            if st.form_submit_button("Inject Radar Target") and p_univ:
                add_phd_target(p_univ, p_name, p_email, p_status, p_notes)
                st.toast("Academic radar coordinates synchronized!", icon="🔍")
                st.rerun()

    # Render PhD Targets
    p_list = get_all_phd_targets()
    if not p_list:
        st.info("Academic pipeline scanning complete. No professor targets logged yet.")
    else:
        # Mini analytics row for cold emails
        total_emails = len(p_list)
        replies = sum(1 for p in p_list if "Replied" in p.email_status or p.email_status == "Interview Scheduled")
        
        st.markdown(f"`Total Target Stack: {total_emails}` | `Response Volume: {replies}`")
        st.write("")
        
        for tgt in p_list:
            with st.container():
                col_info, col_status = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"#### Prof. {tgt.professor_name} — **{tgt.university}**")
                    st.markdown(f"📧 `{tgt.professor_email}`")
                    if tgt.notes:
                        st.caption(f"🧬 *Research Alignment Context:* {tgt.notes}")
                
                with col_status:
                    # Dynamic state status inline update dropdown
                    current_idx = ["Not Sent", "Cold Email Sent", "Replied (Positive)", "Replied (Negative)", "Interview Scheduled"].index(tgt.email_status)
                    new_st = st.selectbox("Update Status", ["Not Sent", "Cold Email Sent", "Replied (Positive)", "Replied (Negative)", "Interview Scheduled"], index=current_idx, key=f"prof_status_{tgt.id}")
                    if new_st != tgt.email_status:
                        update_email_status(tgt.id, new_st)
                        st.rerun()
            st.divider()