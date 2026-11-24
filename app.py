import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st

DB = Path(__file__).with_name('incidents.db')
st.set_page_config(page_title='AASHRAY', page_icon='🛡️', layout='wide')

def query(sql, params=()):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]

query('CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY, report TEXT NOT NULL, location TEXT NOT NULL, created TEXT NOT NULL, category TEXT DEFAULT "Unclassified", urgency TEXT DEFAULT "Not assessed", status TEXT DEFAULT "Pending review")')
query('CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, incident_id INTEGER, created TEXT, action TEXT)')
st.title('AASHRAY · ଆଶ୍ରୟ')
st.warning('Educational simulation only. Do not submit real emergencies or personal information. No dispatch or live hazard monitoring.')
page = st.sidebar.radio('Workspace', ['Citizen report', 'Officer dashboard'])
now = lambda: datetime.now(timezone.utc).isoformat(timespec='seconds')
if page == 'Citizen report':
    st.subheader('Submit a simulated distress report')
    with st.form('report'):
        location = st.text_input('Reported location / ସ୍ଥାନ', 'Gopalpur')
        report = st.text_area('Describe the incident / ଘଟଣା ବର୍ଣ୍ଣନା', max_chars=3000)
        if st.form_submit_button('Submit report'):
            if location.strip() and report.strip():
                query('INSERT INTO incidents (report, location, created) VALUES (?, ?, ?)', (report.strip(), location.strip(), now()))
                st.success('Simulated report saved for officer review.')
            else:
                st.error('Please enter both location and report.')
else:
    records = query('SELECT * FROM incidents ORDER BY id DESC')
    a,b,c = st.columns(3)
    a.metric('Reports',len(records)); b.metric('Pending review',sum(r['status']=='Pending review' for r in records)); c.metric('Reviewed',sum(r['status']=='Reviewed' for r in records))
    if not records:
        st.info('Submit a synthetic report from the Citizen report page first.')
    else:
        st.dataframe([{k:r[k] for k in ('id','location','category','urgency','status','created')} for r in records], hide_index=True)
        chosen = st.selectbox('Select incident', records, format_func=lambda r:f"ASH-{r['id']:04d} · {r['location']}")
        st.write('Original report:', chosen['report'])
        st.caption('Manual classification only — AI extraction is not integrated.')
        categories=['Unclassified','Flooding','Medical assistance','Relief supplies','Other']
        levels=['Not assessed','High','Medium','Low']
        with st.form('review'):
            cat=st.selectbox('Category',categories,index=categories.index(chosen['category']))
            urg=st.selectbox('Suggested urgency (manual simulation)',levels,index=levels.index(chosen['urgency']))
            if st.form_submit_button('Save review'):
                with sqlite3.connect(DB) as conn:
                    conn.execute('UPDATE incidents SET category=?, urgency=?, status=? WHERE id=?',(cat,urg,'Reviewed',chosen['id']))
                    conn.execute('INSERT INTO audit (incident_id,created,action) VALUES (?,?,?)',(chosen['id'],now(),f'Manual review: {cat}; {urg}'))
                st.rerun()
        st.subheader('Audit log')
        st.dataframe(query('SELECT * FROM audit ORDER BY id DESC'),hide_index=True)
