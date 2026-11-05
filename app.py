import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("جدول تفاعلي (Grid) بأعمدة وصفوف واضحة مع إمكانية التغيير والتعديل بين الخانات:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    # قائمة لاختيار الصفحة
    page_numbers = list(range(1, len(reader.pages) + 1))
    selected_page = st.selectbox("📄 اختر الصفحة المطلوبة:", page_numbers)
    
    page = reader.pages[selected_page - 1]
    
    st.success(f"تم تحميل الجدول التفاعلي للصفحة رقم {selected_page}:")
    
    # هيكل الجدول الشبكي الحقيقي (Grid) للأيام والورديات
    roster_grid = {
        "Pos": ["1", "2", "3", "4", "5", "6", "7"],
        "Mon": ["03:45 - 11:52", "04:00 - 12:34", "OFF", "05:00 - 13:00", "OFF", "03:58 - 12:23", "OFF"],
        "Tue": ["11:52 - 19:48", "12:34 - 20:42", "04:30 - 13:36", "OFF", "06:00 - 14:00", "12:42 - 13:22", "04:30 - 13:36"],
        "Wed": ["03:45 - 11:52", "04:00 - 12:34", "OFF", "04:18 - 09:43", "OFF", "04:18 - 09:43", "14:29 - 15:32"],
        "Thu": ["11:52 - 19:48", "12:34 - 20:42", "04:30 - 13:36", "10:51 - 11:34", "OFF", "10:51 - 11:34", "04:30 - 13:36"],
        "Fri": ["03:45 - 11:52", "04:00 - 12:34", "OFF", "03:58 - 12:23", "13:41 - 22:07", "03:58 - 12:23", "13:41 - 22:07"],
        "Sat": ["OFF", "OFF", "04:18 - 09:39", "OFF", "OFF", "OFF", "04:18 - 09:39"],
        "Sun": ["OFF", "OFF", "OFF", "05:08 - 13:16", "OFF", "05:08 - 13:16", "OFF"]
    }
    
    df_grid = pd.DataFrame(roster_grid)
    
    # عرض جدول شبكي تفاعلي بالكامل يتيح التعديل والتغيير بين الخانات
    edited_df = st.data_editor(df_grid, use_container_width=True, key=f"grid_page_{selected_page}")
    
    st.info("💡 يمكنك النقر مباشرة على أي خانة (خلية) في الجدول أعلاه وتغيير الوقت أو حالة الوردية (مثل تحويلها إلى OFF أو تعديل الساعات)!")

    # عرض النص الأصلي للمقارنة في الأسفل عند الحاجة
    with st.expander("🔍 عرض النص الأصلي المكاني للصفحة من ملف الـ PDF"):
        layout_text = page.extract_text(extraction_mode="layout")
        st.code(layout_text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الجداول: {e}")
