import streamlit as st
from .incidents import CATEGORIES, URGENCIES, list_incidents, list_audit, review_incident

def render():
    records = list_incidents()
    a, b, c = st.columns(3)
    a.metric('Reports', len(records))
    b.metric('Pending review', sum(r['status'] == 'Pending review' for r in records))
    c.metric('Reviewed', sum(r['status'] == 'Reviewed' for r in records))
    if not records:
        st.info('Submit a synthetic report from the Citizen report page first.')
        return
    st.dataframe([{k: r[k] for k in ('id','location','category','urgency','status','created')} for r in records], hide_index=True)
    by_id = {r['id']: r for r in records}
    selected = st.selectbox('Select incident', list(by_id), format_func=lambda i: f"ASH-{i:04d} · {by_id[i]['location']}")
    chosen = by_id[selected]
    st.write('Original report:', chosen['report'])
    st.caption('Manual classification only — AI extraction is not integrated.')
    with st.form(f'review_{selected}'):
        cat = st.selectbox('Category', CATEGORIES, index=CATEGORIES.index(chosen['category']) if chosen['category'] in CATEGORIES else 0)
        urg = st.selectbox('Suggested urgency (manual simulation)', URGENCIES, index=URGENCIES.index(chosen['urgency']) if chosen['urgency'] in URGENCIES else 0)
        if st.form_submit_button('Save review'):
            try:
                review_incident(selected, cat, urg)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.rerun()
    st.subheader('Audit log')
    st.dataframe(list_audit(), hide_index=True)
