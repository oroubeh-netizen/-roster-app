import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("تم ربط جدول الورديات (PDF) بنجاح وقراءته مباشرة من المستودع.")

# اسم ملف الـ PDF الذي قمت برفعه
pdf_filename = "2027 Scheman Angered.pdf" # أو اسم الملف الكامل لديك

try:
    # محاولة قراءة ملف الـ PDF الموجود في المشروع تلقائياً
    reader = PdfReader(pdf_filename)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() or ""
        
    st.success(f"تم تحميل وقراءة الملف ({pdf_filename}) بنجاح!")
    
    st.subheader("محتوى الجدول المستخرج من الـ PDF:")
    st.text_area("النصوص الموجودة في الملف:", pdf_text, height=350)

except Exception as e:
    st.info("الرجاء التأكد من تطابق اسم ملف الـ PDF تماماً مع الكود، أو يمكنك رفع الملف أدناه:")
    uploaded_file = st.file_uploader("اختر ملف الـ PDF الخاص بالورديات", type=["pdf"])
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
        st.text_area("محتوى الملف المرفوع:", pdf_text, height=300)
