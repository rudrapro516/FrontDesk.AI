import streamlit as st

def clean_val(val):
    if val is None:
        return "Not specified"
    v_str = str(val).replace('\xa0', ' ').strip(' ,.\t\n\r')
    if v_str.lower() in ['nan', 'not specified', 'none', '']:
        return "Not specified"
    return v_str

def render_doctor_card(row):
    name = clean_val(row.get("Doctor Name", "Unknown"))
    dept = clean_val(row.get("Department", "Not specified"))
    desig = clean_val(row.get("Designation", "Not specified"))
    hosp = clean_val(row.get("Hospital", "Not specified"))
    unit = clean_val(row.get("Unit", "Not specified"))
    opd = clean_val(row.get("OPD Days", "Not specified"))
    ot = clean_val(row.get("OT Days", "Not specified"))
    timing = clean_val(row.get("OPD Timing", "Not specified"))
    
    # Timing string only if valid
    timing_str = f" <span style='color: #888888; font-size: 0.8rem;'>({timing})</span>" if str(timing) not in ['Not specified', 'nan', ''] else ""
    
    # Clean empty designations
    desig_str = f" | {desig}" if str(desig) and str(desig) not in ['Not specified', 'nan', ''] else ""
    
    # Conditionally render rows
    hosp_html = f'<div class="doc-detail">🏥 <b>Hospital:</b> {hosp}</div>' if str(hosp) not in ['Not specified', 'nan', ''] else ''
    # Custom Time string instead of Unit
    time_str = "Winter 8 AM to 2 PM, Summer 8 AM to 2 PM"
    time_html = f'<div class="doc-detail">⏱️ <b>Time:</b> {time_str}</div>'
    opd_html = f'<div class="doc-detail">📅 <b>OPD Days:</b> {opd}{timing_str}</div>' if str(opd) not in ['Not specified', 'nan', ''] else ''
    ot_html = f'<div class="doc-detail">🔪 <b>OT Days:</b> {ot}</div>' if str(ot) not in ['Not specified', 'nan', ''] else ''
    
    html_content = f"""<div class="doctor-card">
<div class="doc-name">🧑‍⚕️ {name}</div>
<div class="doc-dept">{dept}{desig_str}</div>
{hosp_html}
{time_html}
{opd_html}
{ot_html}
</div>"""
    
    st.markdown(html_content, unsafe_allow_html=True)
