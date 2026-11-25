import streamlit as st
from .incidents import submit_report

def render():
    st.subheader('Submit a simulated distress report')
    with st.form('report'):
        location = st.text_input('Reported location / ସ୍ଥାନ', 'Gopalpur', max_chars=200)
        report = st.text_area('Describe the incident / ଘଟଣା ବର୍ଣ୍ଣନା', max_chars=3000)
        if st.form_submit_button('Submit report'):
            try:
                incident_id = submit_report(location, report)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success(f'Simulated report ASH-{incident_id:04d} saved for officer review.')
