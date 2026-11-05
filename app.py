import streamlit as st
import pandas as pd
import pdfplumber

st.set_page_config(page_title="نظام إدارة الورديات - Angered", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("قم بررفع ملف الـ PDF الخاص بالجدول لعرضه واستخراج بيانات الورديات أوتوماتيكياً.")

‎# أداة لرفع ملف الـ PDF من هاتفك
uploaded_file = st.file_uploader("اختر ملف الـ PDF الخاص بالورديات", type=["pdf"])

if uploaded_file is not None:
    st.success("تم رفع الملف بنجاح! جاري قراءة البيانات...")
    
‎    # قراءة النصوص والجدول من ملف الـ PDF
    with pdfplumber.open(uploaded_file) as pdf:
        extracted_text = ""
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""
            
    st.subheader("محتوى الملف المستخرج:")
    st.text_area("النصوص الموجودة في الـ PDF:", extracted_text, height=200)
    
‎    # محاولة استخراج الجداول إن وجدت
    with pdfplumber.open(uploaded_file) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                st.write(f"تم العثور على جدول في الصفحة {i+1}:")
                for table in tables:
                    df_pdf = pd.DataFrame(table)
                    st.dataframe(df_pdf, use_container_width=True)
else:
    st.info("الرجاء رفع ملف PDF للبدء.")
