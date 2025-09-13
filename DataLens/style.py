# style.py
import streamlit as st

def show_header():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
            background-size: 400% 400%;
            animation: gradient 3s ease infinite;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        ">
            🚀 DataLens Pro
        </h1>
        <h3 style="
            color: #2C3E50;
            font-weight: 300;
            margin-top: 10px;
            font-size: 1.2rem;
            letter-spacing: 2px;
        ">
            ✨ INTELLIGENT DATA EXPLORATION & VISUALIZATION SUITE ✨
        </h3>
        <p style="
            color: #7F8C8D;
            font-style: italic;
            margin-top: 5px;
            font-size: 0.9rem;
        ">
            Unleash the power of automated exploratory data analysis
        </p>
    </div>

    <style>
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
    """, unsafe_allow_html=True)
