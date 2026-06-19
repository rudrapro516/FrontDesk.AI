import streamlit as st
import plotly.express as px
from datetime import datetime

def dashboard_interface(df):
    st.markdown("### 📊 Hospital Analytics Dashboard")
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>Total Doctors</div><div class='metric-value'>{len(df)}</div></div>", unsafe_allow_html=True)
    with c2:
        dept_count = df['Department'].nunique() if 'Department' in df.columns else 0
        st.markdown(f"<div class='metric-box'><div class='metric-label'>Departments</div><div class='metric-value'>{dept_count}</div></div>", unsafe_allow_html=True)
    with c3:
        hosp_count = df['Hospital'].nunique() if 'Hospital' in df.columns else 0
        st.markdown(f"<div class='metric-box'><div class='metric-label'>Hospitals</div><div class='metric-value'>{hosp_count}</div></div>", unsafe_allow_html=True)
    with c4:
        today = datetime.now().strftime("%A")
        today_opd = df[df['OPD Days'].astype(str).str.contains(today, case=False, na=False)] if 'OPD Days' in df.columns else df.iloc[0:0]
        st.markdown(f"<div class='metric-box'><div class='metric-label'>OPD Today ({today[:3]})</div><div class='metric-value'>{len(today_opd)}</div></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Plotly dark mode configuration
    chart_template = "plotly_dark"
    color_seq = ['#888888', '#666666', '#555555', '#444444', '#333333']
    
    col1, col2 = st.columns(2)
    with col1:
        # Dept chart
        if 'Department' in df.columns:
            dept_counts = df['Department'].value_counts().reset_index()
            dept_counts.columns = ['Department', 'Count']
            fig = px.bar(dept_counts.head(10), x='Department', y='Count', title="Top 10 Departments by Doctor Count", color_discrete_sequence=['#555555'], template=chart_template)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Hospital chart
        if 'Hospital' in df.columns:
            hosp_counts = df['Hospital'].value_counts().reset_index()
            hosp_counts.columns = ['Hospital', 'Count']
            fig = px.pie(hosp_counts, names='Hospital', values='Count', title="Doctors by Hospital", color_discrete_sequence=color_seq, template=chart_template)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
    col3, col4 = st.columns(2)
    with col3:
        if 'Designation' in df.columns:
            desig_counts = df['Designation'].value_counts().reset_index()
            desig_counts.columns = ['Designation', 'Count']
            fig = px.bar(desig_counts.head(10), x='Count', y='Designation', orientation='h', title="Designation Distribution", color_discrete_sequence=['#666666'], template=chart_template)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
    with col4:
        if 'Unit' in df.columns:
            unit_counts = df['Unit'].astype(str).value_counts().reset_index()
            unit_counts.columns = ['Unit', 'Count']
            fig = px.pie(unit_counts.head(10), names='Unit', values='Count', hole=0.4, title="Unit Distribution", color_discrete_sequence=color_seq, template=chart_template)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
