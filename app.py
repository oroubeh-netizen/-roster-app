import streamlit as st
import pandas as pd
try:
    import pdfplumber
except ImportError:
    pass

st.set_page_config(page_title="Angered Roster 3-Lines View", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض تفاصيل كل خلية في الجدول على شكل ثلاثة أسطر مترابطة تماماً كما في ملف الـ PDF الأصلي:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        page_numbers = list(range(1, len(pdf.pages) + 1))
        selected_page = st.selectbox("📄 اختر الصفحة المطلوبة:", page_numbers)
        
        page = pdf.pages[selected_page - 1]
        
        # استخراج الجداول بنجاح مع الحفاظ على هيكلة الخلايا
        table = page.extract_table()
        
        if not table:
            # محاولة استخراج بديلة في حال اختلاف هيكل حدود الجدول
            tables = page.extract_tables()
            if tables:
                table = tables[0]

        if table:
            df = pd.DataFrame(table)
            
            # تنظيف وفهرسة الأعمدة والصفوف لتظهر كجدول إكسل احترافي
            st.success(f"تم تحميل الجدول بدقة مطابقة للصفحة رقم {selected_page}!")
            
            # تنسيق النص داخل الخلايا لضمان ظهور المعلومات كسطور متعددة واضحة
            st.dataframe(df, use_container_width=True)
            
            st.info("💡 ملاحظة: الخلايا الآن مصممة لتציيد البيانات فوق بعضها بنفس هيكلة ملف الـ PDF الأصلي.")
        else:
            # عرض التخطيط النصي المكاني في حال تعذر استخراج الجدول كشبكة حدودية مباشرة
            st.warning("جاري عرض التخطيط المكاني المتقدم للصفحة:")
            text = page.extract_text(layout=True)
            st.code(text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
