import streamlit as st

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="FrontDesk.AI - Dr SN Medical College & Hospital", page_icon="🏥", layout="wide")

from data_loader import load_data
import time
from chatbot import chat_interface
from doctor_search import doctor_finder_interface, department_explorer, schedule_explorer
from dashboard import dashboard_interface

def main():
    # Load CSS
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not load styles.css: {e}")
        
    # Load Data
    df = load_data()
    
    if df.empty:
        st.warning("Please ensure the dataset file is present at 'c:\\Users\\ASUS\\Desktop\\challenges\\code\\HOSPITAL DATA - Copy.xlsx'.")
        return

    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 0;">🏥 FrontDesk.AI</h1>
                <p style="color: #888888; font-size: 0.9rem; margin-top: 0;">Dr SN Medical College & Hospital</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        selection = st.radio("Navigation Menu", [
            "💬 Chat Assistant", 
            "🔍 Doctor Finder", 
            "🏢 Department Explorer",
            "📅 Schedules",
            "📊 Analytics Dashboard"
        ])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.success("Chat history cleared!")
            time.sleep(0.5)
            st.rerun()

    # Route based on selection
    if selection == "💬 Chat Assistant":
        chat_interface(df)
    elif selection == "🔍 Doctor Finder":
        doctor_finder_interface(df)
    elif selection == "🏢 Department Explorer":
        department_explorer(df)
    elif selection == "📅 Schedules":
        schedule_explorer(df)
    elif selection == "📊 Analytics Dashboard":
        dashboard_interface(df)

if __name__ == "__main__":
    main()
