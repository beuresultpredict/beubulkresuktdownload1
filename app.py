import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import io

# Page Config (वही लुक रखने के लिए)
st.set_page_config(page_title="BEU Merged Result", page_icon="🎓")

# Custom CSS for Blue-Black Theme
st.markdown("""
    <style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { background-color: #38bdf8; color: #020617; border-radius: 10px; font-weight: bold; width: 100%; }
    .stInput>div>div>input { background-color: #0f172a; color: white; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Bihar Engineering University, Patna")
st.subheader("Bulk Result Merger (Single PDF)")

# Inputs
raw_url = st.text_input("Paste Sample Result URL", placeholder="https://beu-bih.ac.in/result-three?...")
col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Reg No", value=23153125001, step=1)
with col2:
    end_reg = st.number_input("End Reg No", value=23153125010, step=1)

if st.button("Generate & Merge All Results"):
    if not raw_url:
        st.error("Please enter a URL first!")
    else:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        progress_bar = st.progress(0)
        total = int(end_reg) - int(start_reg) + 1
        
        found_any = False
        
        for idx, reg in enumerate(range(int(start_reg), int(end_reg) + 1)):
            target_url = raw_url.replace("regNo=" + str(start_reg), "regNo=" + str(reg)) # Simple replace logic
            
            try:
                res = requests.get(target_url, timeout=10)
                if res.status_code == 200:
                    # PDF में नया पेज जोड़ना
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, txt=f"Result for Registration No: {reg}", ln=True, align='C')
                    pdf.ln(10)
                    pdf.set_font("Arial", size=10)
                    
                    # बेसिक डेटा निकलना (Scraping)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    text_content = soup.get_text()
                    # PDF में साफ़ सुथरा टेक्स्ट डालना
                    pdf.multi_cell(0, 5, txt=text_content[:2000]) # पहले 2000 अक्षर (पूरी मार्कशीट के लिए)
                    found_any = True
            except:
                st.warning(f"Could not fetch data for {reg}")
            
            progress_bar.progress((idx + 1) / total)

        if found_any:
            # PDF को मेमोरी में सेव करना
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.success("✅ All results merged successfully!")
            st.download_button(
                label="📥 Download Merged PDF File",
                data=pdf_output,
                file_name="Merged_Results.pdf",
                mime="application/pdf"
            )
        else:
            st.error("No results found to merge.")

# Your Footer
st.markdown("---")
st.write(f"""
    This Bulk Result Downloader is designed and developed by **Krishna Raj**, 
    a student of **Rashtrakavi Ramdhari Singh Dinkar College of Engineering, Batch 2023**, 
    from the **Mechanical Engineering Department**.
    [Connect on LinkedIn](https://www.linkedin.com/in/krishna-raj-🇮🇳-528108310)
""")
