import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster System", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("النسخة المتكاملة لاستعراض وإدارة الجداول تماماً كما هي في ملف الـ PDF الأصلي:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    # واجهة تبويبات لاختيار طريقة العرض المثالية
    tab1, tab2 = st.tabs(["📄 التنسيق والمظهر الأصلي للـ PDF", "📊 جدول البيانات والبحث السريع"])
    
    with tab1:
        st.subheader("عرض الصفحة بتخطيطها المكاني الأصلي")
        page_numbers = list(range(1, len(reader.pages) + 1))
        selected_page = st.selectbox("اختر الصفحة المطلوبة:", page_numbers, key="p_layout")
        
        page = reader.pages[selected_page - 1]
        # استخدام نمط الحفاظ على التخطيط المكاني الأصلي للأعمدة والأيام
        layout_text = page.extract_text(extraction_mode="layout")
        
        st.success(f"تم تحميل الصفحة رقم {selected_page} بتنسيقها الأصلي بنجاح:")
        st.code(layout_text, language="text")
        
    with tab2:
        st.subheader("البحث والتحكم في البيانات المستخرجة")
        all_rows = []
        for page_idx, p in enumerate(reader.pages):
            txt = p.extract_text()
            if txt:
                for line in txt.split('\n'):
                    l_str = line.strip()
                    parts = l_str.split()
                    if parts and parts[0].isdigit():
                        all_rows.append({
                            "الصفحة": page_idx + 1,
                            "Pos (الموقف)": parts[0],
                            "تفاصيل الأيام والورديات": "   |   ".join(parts[1:])
                        })
                        
        if all_rows:
            df_all = pd.DataFrame(all_rows)
            search = st.text_input("🔍 ابحث برقم الموقف (Pos) أو الوقت (مثال: 1, 2, 700):")
            if search:
                df_all = df_all[df_all['Pos (الموقف)'].str.contains(search) | df_all['تفاصيل الأيام والورديات'].str.contains(search, case=False)]
            
            edited_table = st.data_editor(df_all, use_container_width=True, key="master_grid")
            st.info("💡 يمكنك استعراض كافة السطور والبحث السريع والتعديل المباشر من خلال هذا الجدول.")
        else:
            st.warning("جاري قراءة محتوى الملف...")

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الملف: {e}")
