import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض وتنسيق بيانات جدول الورديات المستخرج من ملف الـ PDF:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    # استخراج النصوص وتقسيمها لتسهيل العرض
    all_rows = []
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                all_rows.append({"الصفحة": index + 1, "محتوى السطر": line})

    # تحويل البيانات إلى جدول منظم باستخدام Pandas
    df_pdf = pd.DataFrame(all_rows)
    
    st.success("تم قراءة وترتيب محتوى الملف بنجاح!")
    
    # عرض البيانات في جدول تفاعلي منظم
    st.subheader("📊 جدول بيانات الورديات المنظم:")
    st.dataframe(df_pdf, use_container_width=True)

except Exception as e:
    st.warning("الرجاء التأكد من رفع ملف الـ PDF بالشكل الصحيح في المستودع.")
    uploaded_file = st.file_uploader("اختر ملف الـ PDF", type=["pdf"])
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        all_rows = []
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    all_rows.append({"الصفحة": index + 1, "محتوى السطر": line})
        st.dataframe(pd.DataFrame(all_rows), use_container_width=True)
