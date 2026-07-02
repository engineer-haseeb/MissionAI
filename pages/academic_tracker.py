import streamlit as st
from database import get_all_goals, get_all_papers, add_research_paper, get_all_phd_targets, add_phd_target, update_email_studio

st.set_page_config(page_title="Academic Command Studio", layout="wide", page_icon="🎓")

st.title("🎓 Academic Hub: Literature Matrix & Global Outreach Terminal")
st.caption("Cross-link peer-reviewed extractions directly with context-aware cold communication vectors & application funnels.")

tab1, tab2 = st.tabs(["📚 Lit-Review & Gap Mapping (V1)", "📬 USA PhD Tracker & Outreach (V2)"])

# ==========================================
# TAB 1: LIT-REVIEW GAP GENERATOR
# ==========================================
with tab1:
    st.subheader("📝 Scholarly Insights & Open Gaps Matrix")
    
    with st.expander("📥 Log Structural Paper Breakdown", expanded=False):
        goals = get_all_goals()
        g_map = {g.id: f"[{g.category}] {g.title}" for g in goals}
        
        with st.form("paper_ingest_form", clear_on_submit=True):
            p_title = st.text_input("Academic Publication Title")
            col_a, col_y, col_j = st.columns([2, 1, 2])
            with col_a: p_auth = st.text_input("Authors (Primary et al.)")
            with col_y: p_year = st.number_input("Publication Year", min_value=1950, max_value=2030, value=2025)
            with col_j: p_jour = st.text_input("Journal / IEEE / ACM Venue")
            
            p_meth = st.text_area("Core Methodology Deployment (Equations, Bounds, Variables)")
            p_find = st.text_area("Key Empirical Contribution Findings")
            p_gaps = st.text_area("Identified Bottlenecks & Open Research Gaps")
            p_gid = st.selectbox("Link to Mission Goal Focus", options=list(g_map.keys()), format_func=lambda x: g_map[x] if x in g_map else "Independent")
            
            if st.form_submit_button("Commit Analysis Data"):
                if p_title and p_auth:
                    add_research_paper(p_title, p_auth, int(p_year), p_meth, p_find, p_gaps, p_gid, p_jour)
                    st.success("Paper blueprint mapped successfully!")
                    st.rerun()

    papers_list = get_all_papers()
    if not papers_list:
        st.info("No research papers processed into memory files yet.")
    else:
        for paper in papers_list:
            with st.container(border=True):
                st.markdown(f"### 📖 {paper.title} ({paper.year})")
                st.caption(f"👨‍🔬 Authors: {paper.authors} | 🏢 Venue Outpost: {paper.journal if paper.journal else 'N/A'}")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**⚙️ Methodology Scope:**")
                    st.info(paper.core_methodology)
                with c2:
                    st.markdown("**💡 Extraction Insights:**")
                    st.success(paper.key_findings)
                with c3:
                    st.error("**🔍 Validated Gaps Matrix:**")
                    st.warning(paper.limitations_gaps)

# ==========================================
# TAB 2: USA PHD TRACKER & OUTREACH
# ==========================================
with tab2:
    st.subheader("📬 USA University Match Radar & AI Communication Studio")
    
    with st.expander("🚀 Ingest Target University & Professor Profile", expanded=False):
        with st.form("prof_ingest_form", clear_on_submit=True):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                prof_n = st.text_input("Professor Full Name")
                prof_e = st.text_input("Official Email Axis")
                univ_n = st.text_input("Target USA/Global University")
            with c_p2:
                status_e = st.selectbox("Email Timeline State", ["Not Sent", "Sent", "Follow-up", "Replied", "Interview"])
                match_s = st.slider("Research Match Alignment Score (%)", 10, 100, 85)
                prof_abs = st.text_area("Professor's Abstract or Core Lab Themes")
                
            if st.form_submit_button("Lock Profile into Application Funnel"):
                if prof_n and prof_e and univ_n:
                    add_phd_target(univ_n, prof_n, prof_e, status_e, match_s, prof_abs)
                    st.success(f"Locked target asset: {prof_n} at {univ_n}")
                    st.rerun()

    targets_list = get_all_phd_targets()
    if not targets_list:
        st.info("No active USA PhD application paths running inside the tracking module.")
    else:
        for target in targets_list:
            with st.container(border=True):
                th_col, ts_col = st.columns([3, 1])
                with th_col:
                    st.markdown(f"#### 🏛️ {target.professor_name} | {target.university}")
                    st.caption(f"📧 Contact: `{target.professor_email}` | 🎯 Research Match Score: `{target.research_match_score}%`")
                with ts_col:
                    p_states = ["Not Sent", "Sent", "Follow-up", "Replied", "Interview"]
                    p_idx = p_states.index(target.email_status) if target.email_status in p_states else 0
                    nxt_status = st.selectbox("Email Vector State", p_states, index=p_idx, key=f"t_stat_{target.id}")
                    
                    acc_states = ["Pending", "Accepted", "Rejected"]
                    acc_idx = acc_states.index(target.acceptance_status) if target.acceptance_status in acc_states else 0
                    nxt_acc = st.selectbox("Acceptance Status", acc_states, index=acc_idx, key=f"t_acc_{target.id}")
                    
                    if nxt_status != target.email_status or nxt_acc != target.acceptance_status:
                        update_email_studio(target.id, nxt_status, acceptance=nxt_acc)
                        st.rerun()

                with st.expander("📝 Application Progress & Interview Notes Logs", expanded=False):
                    with st.form(f"notes_form_{target.id}"):
                        current_notes = st.text_area("Live Interview / Progress Log Context", value=target.interview_notes if target.interview_notes else "")
                        if st.form_submit_button("Save Pipeline Notes"):
                            update_email_studio(target.id, target.email_status, draft=target.generated_draft, acceptance=target.acceptance_status, notes=current_notes)
                            st.toast("Application progress ledger secured!")
                            st.rerun()

                ec1, ec2 = st.columns([2, 3])
                with ec1:
                    st.markdown("**Lab Anchor Research Focus:**")
                    st.info(target.professor_research if target.professor_research else "Empty abstract parameters.")
                    
                    if st.button("✨ Compile Contextual Proposal Draft", key=f"c_draft_{target.id}"):
                        compiled_email = (
                            f"Subject: Inquiry Regarding PhD Opportunities and Research Alignment - {target.professor_name}\n\n"
                            f"Dear Professor {target.professor_name},\n\n"
                            f"My name is Abdul Haseeb, and I am currently completing my Master's degree in Computer Science at Southwest University of Science and Technology (SWUST) in Mianyang, China. My background includes high-level software stack tracking, implementing clear Object-Oriented Programming (OOP) paradigms in Python, and conducting modular data flow logic tests.\n\n"
                            f"I have closely been tracking your research laboratory's advancements concerning: '{target.professor_research[:140]}...'. Your methodology maps closely with my core analytical skillset and my primary target goal to pursue rigorous, research-driven doctoral tasks under your supervision.\n\n"
                            f"I have attached my comprehensive academic CV for your review. Would you be available for a brief meeting to discuss prospective vacancies within your group?\n\n"
                            f"Thank you for your time and professional courtesy.\n\n"
                            f"Best regards,\n"
                            f"Abdul Haseeb\n"
                            f"SWUST, Mianyang, China"
                        )
                        update_email_studio(target.id, target.email_status, draft=compiled_email, acceptance=target.acceptance_status)
                        st.rerun()
                        
                with ec2:
                    st.markdown("**Active Proposal Template Output:**")
                    if target.generated_draft:
                        st.text_area("Copy Clip Buffer", target.generated_draft, height=200, key=f"buf_{target.id}")
                    else:
                        st.warning("Trigger compilation sequence via left dashboard command array.")