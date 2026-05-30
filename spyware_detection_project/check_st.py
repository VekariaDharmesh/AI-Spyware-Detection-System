
import streamlit as st
try:
    print(f"Streamlit version: {st.__version__}")
    if hasattr(st, 'fragment'):
        print("st.fragment is available")
    else:
        print("st.fragment is NOT available")
except Exception as e:
    print(f"Error: {e}")
