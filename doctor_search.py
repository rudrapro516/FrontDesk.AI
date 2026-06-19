import streamlit as st
from ui import render_doctor_card

def doctor_finder_interface(df):
    st.markdown("### 🔍 Advanced Doctor Finder")
    
    with st.expander("Filter Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name_query = st.text_input("Search by Name")
            dept_filter = st.selectbox("Department", ["All"] + sorted(df['Department'].astype(str).unique().tolist()))
        with col2:
            hosp_filter = st.selectbox("Hospital", ["All"] + sorted(df['Hospital'].astype(str).unique().tolist())) if 'Hospital' in df.columns else "All"
            day_filter = st.selectbox("OPD Day", ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        with col3:
            ot_day_filter = st.selectbox("OT Day", ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            desig_filter = st.selectbox("Designation", ["All"] + sorted(df['Designation'].astype(str).unique().tolist())) if 'Designation' in df.columns else "All"
            unit_filter = st.selectbox("Time", ["All"] + sorted(df['Unit'].astype(str).unique().tolist())) if 'Unit' in df.columns else "All"
            
    # Apply filters
    filtered_df = df.copy()
    if name_query:
        filtered_df = filtered_df[filtered_df['Doctor Name'].astype(str).str.contains(name_query, case=False, na=False)]
    if dept_filter != "All":
        filtered_df = filtered_df[filtered_df['Department'].astype(str) == dept_filter]
    if hosp_filter != "All":
        filtered_df = filtered_df[filtered_df['Hospital'].astype(str) == hosp_filter]
    if day_filter != "All":
        filtered_df = filtered_df[filtered_df['OPD Days'].astype(str).str.contains(day_filter, case=False, na=False)]
    if ot_day_filter != "All":
        filtered_df = filtered_df[filtered_df['OT Days'].astype(str).str.contains(ot_day_filter, case=False, na=False)]
    if desig_filter != "All":
        filtered_df = filtered_df[filtered_df['Designation'].astype(str) == desig_filter]
    if unit_filter != "All":
        filtered_df = filtered_df[filtered_df['Unit'].astype(str) == unit_filter]
        
    st.success(f"Found {len(filtered_df)} doctors matching your criteria.")
    
    # Display cards
    if not filtered_df.empty:
        cols = st.columns(2)
        for idx, row in enumerate(filtered_df.iterrows()):
            with cols[idx % 2]:
                render_doctor_card(row[1])

def department_explorer(df):
    st.markdown("### 🏢 Department Explorer")
    depts = sorted(df['Department'].astype(str).unique().tolist())
    
    # Simple grid of buttons or selectbox
    selected_dept = st.selectbox("Select a Department to Explore", depts)
    
    if selected_dept:
        st.markdown(f"#### Doctors in {selected_dept}")
        dept_df = df[df['Department'].astype(str) == selected_dept]
        
        cols = st.columns(2)
        for idx, row in enumerate(dept_df.iterrows()):
            with cols[idx % 2]:
                render_doctor_card(row[1])

def schedule_explorer(df):
    st.markdown("### 📅 Schedule Explorer")
    
    col1, col2 = st.columns(2)
    with col1:
        schedule_type = st.radio("Schedule Type", ["OPD (Outpatient)", "OT (Operation Theater)"])
    with col2:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        selected_day = st.selectbox("Select Day", days)
    
    if selected_day:
        st.markdown(f"#### {schedule_type} Schedule for {selected_day}")
        
        target_col = 'OPD Days' if 'OPD' in schedule_type else 'OT Days'
        day_df = df[df[target_col].astype(str).str.contains(selected_day, case=False, na=False)]
        
        if day_df.empty:
            st.info(f"No {schedule_type} scheduled for {selected_day}.")
        else:
            cols = st.columns(2)
            for idx, row in enumerate(day_df.iterrows()):
                with cols[idx % 2]:
                    render_doctor_card(row[1])
