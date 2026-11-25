import streamlit as st
from ashray import database, citizen, dashboard

st.set_page_config(page_title='AASHRAY', page_icon='🛡️', layout='wide')
database.initialize()
st.title('AASHRAY · ଆଶ୍ରୟ')
st.warning('Educational simulation only. Do not submit real emergencies or personal information. No dispatch or live hazard monitoring.')
page = st.sidebar.radio('Workspace', ['Citizen report', 'Officer dashboard'])
if page == 'Citizen report':
    citizen.render()
else:
    dashboard.render()
