import streamlit as st
import requests
import re
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="BEU Result Merger", layout="centered")

# --- CUSTOM CSS (For Blue-Black Theme) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        color: #f8fafc;
    }
    div[data-testid="stText"] { color: #94a3b8; }
    .main-title { color: #38bdf8; text-transform: uppercase; text-align: center; font-weight: 600; font-size: 2.2rem; }
    .sub-title { color: #94a3b8; text-align: center; margin-bottom: 2rem; }
    .footer { text-align: center; margin-top: 3rem; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); color: #94a3b8; font-size: 0.85rem; }
    .linkedin-btn { background: #0077b5; color: white !important; padding: 8px 20px; border-radius: 20px; text-decoration: none; display: inline-block; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- UI INTERFACE ---
st.markdown('<h1 class="main-title">Bihar Engineering University, Patna</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Bulk Result For Any Semester (Merged Edition)</p>', unsafe_allow_html=True)

# Input Box
raw_url = st.text_input("Paste Sample Result URL", placeholder="https://beu-bih.ac.in/result-three?...")
st.caption("Example: https://beu-bih.ac.in/result-three?name=...&regNo=23153125001&...")

col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Registration No", value=23153125001, step=1)
with col2:
    end_reg = st.number_input("End Registration No", value=23153125010, step=1)

if st.button("Generate & Merge Results"):
    if not raw_url:
        st.warning("Please provide a sample URL first.")
    else:
        # यहाँ हम रिजल्ट्स का एक 'HTML Report' बनाएंगे जिसे यूजर PDF की तरह सेव कर सके
        st.info("Generating links... Click below to view and save all as one PDF.")
        
        all_links_html = ""
        for reg in range(int(start_reg), int(end_reg) + 1):
            # URL में regNo को बदलने का लॉजिक
            new_url = re.sub(r"(regNo=)(\d+)", rf"\1{reg}", raw_url)
            all_links_html += f"<div style='background:rgba(255,255,255,0.05); padding:10px; margin:5px; border-radius:8px; border-left:4px solid #38bdf8;'>Reg No: <b>{reg}</b> | <a href='{new_url}' target='_blank' style='color:#38bdf8;'>Open Result</a></div>"
        
        st.markdown(all_links_html, unsafe_allow_html=True)
        st.success("सारे लिंक्स तैयार हैं! एक ही PDF में मर्ज करने के लिए 'Print' (Ctrl+P) दबाएं और 'Save as PDF' चुनें।")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>, 
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering, Batch 2023</b>, 
        from the <b>Mechanical Engineering Department</b>.<br><br>
        This tool is created with the purpose of result prediction for students.<br>
        <a href="https://www.linkedin.com/in/krishna-raj-%F0%9F%87%AE%F0%9F%87%B3-528108310" class="linkedin-btn" target="_blank">Connect with me on LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)
