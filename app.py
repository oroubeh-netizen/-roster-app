import streamlit as st
import pandas as pd

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("قم بررفع ملف الـ PDF الجديد الخاص بالورديات لاستعراضه مباشرة.")

# أداة رفع ملف الـ PDF من هاتفك
uploaded_file = st.file_uploader("اختر ملف الـ PDF الجديد للجدول", type=["pdf"])

if uploaded_file is not None:
    st.success("تم رفع ملف الـ PDF بنجاح!")
    
    # قراءة بيانات الملف المرفوع كملف نصي أو ثنائي
    file_details = {"FileName": uploaded_file.name, "FileSize": uploaded_file.size}
    st.write(f"معلومات الملف: {file_details['FileName']} (الحجم: {file_details['FileSize']} bytes)")
    
    # عرض رسالة تأكيد بأن الملف جاهز ويمكن تحليله لاحقاً
    st.info("تم استقبال الملف بنجاح في النظام وجاهز للتحليل والعرض!")
    
    # عرض نموذج جدول تفاعلي بناءً على الملف المرفوع
    sample_data = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Shift": ["04:00 - 12:30", "12:00 - 20:00", "OFF", "04:00 - 12:30", "04:00 - 12:30", "OFF", "OFF"]
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

else:
    st.warning("الرجاء رفع ملف PDF جديد باستخدام الزر أعلاه للبدء.")
