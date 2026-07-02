import streamlit as st
import datetime
from database import get_all_scholarships, add_scholarship, update_scholarship_status

st.set_page_config(page_title="Scholarship Pipeline", layout="wide", page_icon="🎖️")

st.title("🎖️ High-Yield Fellowship & Scholarship Tracker Desk")
st.caption("Central management station orchestrating application checklists and milestone countdowns for ANSO, CSC, and global pathways.")

# ==========================================
# NEW FELLOWSHIP INGESTION
# ==========================================
with st.expander("🚀 Anchor New Fellowship Target Pipeline", expanded=False):
    with st.form("sch_form", clear_on_submit=True):
        s_name = st.text_input("Scholarship Fellowship Name", placeholder="e.g., ANSO Fellowship 2027")
        s_status = st.selectbox("Pipeline Application Position", ["Drafting", "Submitted", "Shortlisted", "Awarded", "Rejected"])
        s_dead = st.date_input("Official Submission Deadline Close", value=datetime.date.today() + datetime.timedelta(days=60))
        
        st.markdown("**Required Core Documentation Assembly (Checklist Targets):**")
        c_cv = st.checkbox("Comprehensive Academic CV", value=True)
        c_prop = st.checkbox("Detailed Research Proposal Plan", value=True)
        c_recom = st.checkbox("Two Academic Letters of Recommendation", value=True)
        c_degree = st.checkbox("Attested Degrees & Transcripts Stack", value=True)
        c_hsk = st.checkbox("Language Proficiency Certifications (HSK / IELTS)", value=False)
        
        if st.form_submit_button("Lock Fellowship Track"):
            if s_name:
                # Compile strings array list tokens split items
                tokens = []
                if c_cv: tokens.append("CV")
                if c_prop: tokens.append("Research Proposal")
                if c_recom: tokens.append("Recommendation Letters")
                if c_degree: tokens.append("Transcripts Stack")
                if c_hsk: tokens.append("Language Proficiency")
                
                add_scholarship(s_name, s_status, s_dead, ",".join(tokens))
                st.success(f"Fellowship channel activated for: {s_name}!")
                st.rerun()

st.markdown("---")

# ==========================================
# DISPLAY SYSTEM LIVE FUNNEL FLOW
# ==========================================
active_sch = get_all_scholarships()

if not active_sch:
    st.info("No fellowship networks monitored inside processing memory arrays yet.")
else:
    for sch in active_sch:
        days_countdown = (sch.deadline - datetime.date.today()).days
        
        with st.container(border=True):
            col_head, col_count = st.columns([3, 1])
            with col_head:
                st.markdown(f"### 🏅 {sch.name}")
                st.caption(f"📅 Deadline Anchor: **{sch.deadline}**")
            with col_count:
                if days_countdown < 0:
                    st.error(f"⚠️ Submissions Closed")
                else:
                    st.metric("Timeline Countdown", f"{days_countdown} Days Left")
            
            # Interactive Configuration Status Modifiers
            st.markdown("---")
            cx1, cx2 = st.columns(2)
            
            with cx1:
                states_pool = ["Drafting", "Submitted", "Shortlisted", "Awarded", "Rejected"]
                st_idx = states_pool.index(sch.status) if sch.status in states_pool else 0
                new_state = st.selectbox("Application State Matrix Pointer", states_pool, index=st_idx, key=f"sch_st_{sch.id}")
                
                history_text = st.text_area("Submission Manifest Records / Application Portal Link", value=sch.submission_history if sch.submission_history else "", key=f"sch_hist_{sch.id}")
                
                if st.button("Commit Status Adjustments", key=f"sch_save_btn_{sch.id}"):
                    update_scholarship_status(sch.id, new_state, history=history_text)
                    st.toast("Fellowship progress state verified and synchronized!")
                    st.rerun()

            with cx2:
                st.markdown("**📑 Mandatory Document Verification Checks:**")
                current_docs = sch.doc_checklist.split(",") if sch.doc_checklist else []
                
                st.info("⚙️ Currently Logged Target Requirements: " + (", ".join(current_docs) if current_docs else "None"))
                st.caption("Cross-verify portal requirements continuously to avoid evaluation setup drops.")