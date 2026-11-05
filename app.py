import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("تم رفع ملف الـ PDF الخاص بالجدول بنجاح، وجاري استخراج البيانات:")

# أداة رفع الملف
uploaded_file = st.file_uploader("اختر أو استبدل ملف الـ PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("تم استقبال الملف وقراءته بنجاح!")
    
    # قراءة محتوى الـ PDF صفحة بصفحة
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            extracted_text += f"\n--- صفحة {i+1} ---\n" + text
            
    st.subheader("محتوى الجدول المستخرج من ملفك:")
    st.text_area("النصوص المستخرجة:", extracted_text, height=350)
    
    # جدول تفاعلي لتنظيم الإدارة
    st.subheader("إدارة الورديات والأيام:")
    sample_data = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Shift": ["03:45 - 11:52", "11:52 - 19:48", "OFF", "03:45 - 11:52", "11:52 - 19:48", "OFF", "OFF"]
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

else:
    st.info("الرجاء رفع ملف الـ PDF للبدء في استعراض البيانات.")
