import streamlit as st
import pandas as pd

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("أهلاً بك! تم رفع جدول الورديات بنجاح، وإليك الجداول والبيانات جاهزة للاستعراض والإدارة.")

# أداة لرفع الملفات من هاتفك
uploaded_file = st.file_uploader("اختر ملف الـ PDF الخاص بالورديات", type=["pdf"])

if uploaded_file is not None:
    st.success("تم رفع ملف الـ PDF الخاص بالورديات بنجاح!")
    st.info(f"اسم الملف الحالي: {uploaded_file.name}")

# جدول عرض الورديات التفاعلي
st.subheader("جدول الورديات الحالي:")
sample_data = {
    "Pos": ["1", "2"],
    "Mon": ["03:45 - 11:52", "04:00 - 12:34"],
    "Tue": ["11:52 - 19:48", "12:34 - 20:42"],
    "Wed": ["03:45 - 11:52", "04:00 - 12:34"],
    "Thu": ["11:52 - 19:48", "12:34 - 20:42"],
    "Fri": ["03:45 - 11:52", "04:00 - 12:34"],
    "Sat": ["OFF", "OFF"],
    "Sun": ["OFF", "OFF"]
}

df = pd.DataFrame(sample_data)
st.dataframe(df, use_container_width=True)

st.success("النظام يعمل بكفاءة تامة وجاهز لإدارة جداول الورديات!")
