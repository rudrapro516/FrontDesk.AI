import streamlit as st
import pandas as pd
from utils import identify_department, extract_day
from ui import render_doctor_card
import time

def process_query(query, df):
    query_lower = query.lower()
    
    # 1. Symptom checker
    dept = identify_department(query)
    if dept and "department" not in query_lower and "doctor" not in query_lower:
        matched_doctors = df[df['Department'].str.contains(dept, case=False, na=False)]
        response = f"Based on your symptoms, I recommend visiting the **{dept}** Department.\n\n"
        if not matched_doctors.empty:
            response += f"Here are some available doctors:\n"
            for _, doc in matched_doctors.head(3).iterrows():
                hosp = doc.get('Hospital', 'Unknown')
                hosp_text = f" ({hosp})" if str(hosp) not in ["Not specified", "nan", "", "Unknown"] else ""
                response += f"- **{doc.get('Doctor Name', 'Unknown')}**{hosp_text}\n"
        return response, matched_doctors

    # 2. Query matching logic
    # Find by Name (Dr. X or Doctor X)
    if "dr." in query_lower or "doctor" in query_lower or "dr " in query_lower:
        words = query_lower.replace("find", "").replace("show", "").replace("who is", "").replace("search", "").split()
        search_terms = [w for w in words if w not in ["dr.", "doctor", "dr", "the", "a", "an", "is"]]
        if search_terms:
            for term in search_terms:
                if len(term) > 2: # avoid matching very short words
                    matched = df[df['Doctor Name'].str.contains(term, case=False, na=False)]
                    if not matched.empty:
                        return f"Here are the doctors matching '{term}':", matched

    # Find by Department
    depts = df['Department'].dropna().unique()
    stop_words = {"find", "show", "who", "search", "doctor", "doctors", "department", "available", "today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "opd", "ot", "in", "the", "a", "an"}
    query_words = [w for w in query_lower.split() if w not in stop_words and len(w) > 2]
    
    matched_depts = set()
    
    # 1. Exact match
    for d in depts:
        if str(d).lower() in query_lower:
            matched_depts.add(d)
            
    # 2. Partial match (e.g. "surgery" matches "General Surgery", "Pediatric Surgery")
    if not matched_depts:
        for d in depts:
            d_lower = str(d).lower()
            for w in query_words:
                if w in d_lower:
                    matched_depts.add(d)
                    break
                    
    if matched_depts:
        matched = df[df['Department'].isin(list(matched_depts))]
        day = extract_day(query)
        dept_names = ", ".join(list(matched_depts))
        if day:
            matched_day = matched[matched['OPD Days'].astype(str).str.contains(day, case=False, na=False)]
            if not matched_day.empty:
                return f"Doctors in {dept_names} available on {day}:", matched_day
            return f"I couldn't find any doctors in {dept_names} available on {day}. Here are all doctors:", matched
        return f"Here are the doctors in {dept_names}:", matched
            
    # Find by Day
    day = extract_day(query)
    if day:
        matched = df[df['OPD Days'].astype(str).str.contains(day, case=False, na=False)]
        if "ot" in query_lower or "operation" in query_lower:
            matched = df[df['OT Days'].astype(str).str.contains(day, case=False, na=False)]
            return f"Here are doctors who have OT on {day}:", matched
        return f"Here are doctors who have OPD on {day}:", matched
        
    # Find by Designation
    if "senior" in query_lower or "professor" in query_lower:
        matched = df[df['Designation'].astype(str).str.contains("Professor", case=False, na=False)]
        return "Here are the Professors/Senior doctors:", matched
        
    # Find by Hospital
    if 'Hospital' in df.columns:
        hospitals = df['Hospital'].dropna().unique()
        for h in hospitals:
            if str(h).lower() in query_lower:
                matched = df[df['Hospital'].astype(str).str.contains(str(h), case=False, na=False, regex=False)]
                return f"Here are doctors working at {h}:", matched
            
    return "I couldn't specifically find what you're looking for. Try asking 'Find ENT doctors', 'Which doctors are available today?', or describe your symptoms.", pd.DataFrame()

def chat_interface(df):
    st.markdown("### 💬 AI Chat Assistant")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    # Render history
    for msg in st.session_state.chat_history:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
                    
    prompt = st.chat_input("Ask about doctors, departments, or describe your symptoms...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.rerun()
        
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        prompt = st.session_state.chat_history[-1]["content"]
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Searching records..."):
                time.sleep(0.6)
                text_response, df_response = process_query(prompt, df)
                
            st.markdown(text_response)
            
            if not df_response.empty:
                # Append names as a markdown list instead of cards
                names_md = ""
                for _, row in df_response.iterrows():
                    dept = row.get('Department', 'Unknown')
                    names_md += f"- **{row['Doctor Name']}**  |  _{dept}_\n"
                st.markdown(names_md)
                text_response += "\n\n" + names_md
                    
            st.session_state.chat_history.append({"role": "assistant", "content": text_response})
