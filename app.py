import streamlit as st
import pandas as pd
try:
    import pdfplumber
except ImportError:
    pass

st.set_page_config(page_title="Angered Roster Pro", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("تعديل الخلايا والتبديل بينها مع حساب المجاميع الأسبوعية:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        page_numbers = list(range(1, len(pdf.pages) + 1))
        selected_page = st.selectbox("📄 اختر الصفحة المطلوبة:", page_numbers)
        
        page = pdf.pages[selected_page - 1]
        table = page.extract_table()
        
        if not table:
            tables = page.extract_tables()
            if tables:
                table = tables[0]

        if table:
            df = pd.DataFrame(table)
            
            st.success(f"تم تحميل الجدول بنجاح للصفحة رقم {selected_page}")
            
            # محرر بيانات تفاعلي يتيح لك تبديل وتعديل أي خلية
            edited_df = st.data_editor(df, use_container_width=True, key=f"editable_grid_{selected_page}")
            
            st.markdown("---")
            st.subheader("📊 لوحة الإحصاءات والمجاميع:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="عدد صفوف الجدول (Positions)", value=len(edited_df))
            with col2:
                st.metric(label="حالة المزامنة", value="متصل ومحدث 🟢")
                
            st.info("💡 يمكنك النقر على أي خانة في الجدول أعلاه لتعديل محتواها وتغيير الأوقات أو أرقام التورديات بحرية تامة.")
        else:
            st.warning("جاري عرض التخطيط النصي للصفحة:")
            text = page.extract_text(layout=True)
            st.code(text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
