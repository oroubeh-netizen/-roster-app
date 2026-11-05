import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("قم برفع ملف الـ PDF الخاص بالجدول لعرضه واستعراضه مباشرة من هاتفك.")

# أداة لرفع ملف الـ PDF
uploaded_file = st.file_uploader("اختر ملف الـ PDF الخاص بالورديات", type=["pdf"])

if uploaded_file is not None:
    st.success("تم رفع ملف الـ PDF بنجاح!")
    
    # قراءة محتوى الـ PDF
    reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() or ""
        
    st.subheader("محتوى الجدول المستخرج من الـ PDF:")
    st.text_area("النصوص الموجودة في الملف:", pdf_text, height=300)
else:
    st.info("لم يتم رفع ملف PDF بعد. يمكنك اختيار الجدول الافتراضي أدناه:")
    
    # الجدول الافتراضي
    roster_option = st.selectbox(
        "Select Roster / اختر الجدول:",
        ["Roster 700 (Produktionssupport)", "Roster 701 (Var tredje helg)"]
    )

    if "700" in roster_option:
        data = {
            "Pos": ["1", "2"],
            "Mon": ["03:45 - 11:52", "04:00 - 12:34"],
            "Tue": ["11:52 - 19:48", "12:34 - 20:42"],
            "Wed": ["03:45 - 11:52", "04:00 - 12:34"],
            "Thu": ["11:52 - 19:48", "12:34 - 20:42"],
            "Fri": ["03:45 - 11:52", "04:00 - 12:34"],
            "Sat": ["OFF", "OFF"],
            "Sun": ["OFF", "OFF"]
        }
    else:
        data = {
            "Pos": ["1", "2"],
            "Mon": ["03:58 - 12:23", "OFF"],
            "Tue": ["12:42 - 13:22", "04:30 - 13:36"],
            "Wed": ["04:18 - 09:43", "14:29 - 15:32"],
            "Thu": ["10:51 - 11:34", "04:30 - 13:36"],
            "Fri": ["03:58 - 12:23", "13:41 - 22:07"],
            "Sat": ["OFF", "04:18 - 09:39"],
            "Sun": ["05:08 - 13:16", "OFF"]
        }

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

st.success("النظام يعمل بكفاءة وجاهز لاستقبال ملفاتك!")
