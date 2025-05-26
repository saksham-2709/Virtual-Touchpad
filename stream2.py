import streamlit as st
import subprocess

st.markdown(
    """
    <style>
        /* Overall Page Styling */
        body {
            background: black;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        
        /* Logo Styling */
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Title Styling */
        .title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
        }
        
        /* Button Styling */
        .stButton > button {
            background: white;
            color: black;
            padding: 12px 30px;
            border-radius: 20px;
            border: 2px solid white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }

        .stButton > button:hover {
            background: gray;
            color: white;
            transform: scale(1.05);
        }

        /* Output Box Styling */
        .output-box {
            background: #1e1e1e;
            color: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid white;
            font-family: monospace;
            margin-top: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Space for Logo
st.markdown('<div class="logo-container">[Your Logo Here]</div>', unsafe_allow_html=True)

st.markdown('<h1 class="title">Execute Scripts</h1>', unsafe_allow_html=True)

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        return result.stdout, result.stderr
    except FileNotFoundError:
        return None, f"Script '{script_name}' not found."
    except Exception as e:
        return None, str(e)

if st.button('Use Virtual Keyboard'):
    stdout, stderr = run_script('main_keyboard.py')
    if stdout:
        st.markdown(f'<div class="output-box">{stdout}</div>', unsafe_allow_html=True)

if st.button('Use Virtual Touchpad'):
    stdout, stderr = run_script('main_touchpad.py')
    if stdout:
        st.markdown(f'<div class="output-box">{stdout}</div>', unsafe_allow_html=True)
