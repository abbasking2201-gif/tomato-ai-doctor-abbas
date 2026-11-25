
import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

st.set_page_config(
    page_title="Tomato AI Doctor",
    page_icon="🍅",
    layout="centered"
)

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("tomato_disease_model.keras")

@st.cache_data
def load_classes():
    with open("class_names.json", "r") as f:
        return json.load(f)

model = load_model()
class_names = load_classes()

st.title("🍅 Tomato AI Doctor")
st.subheader("نظام ذكي لتشخيص أمراض أوراق الطماطة")
st.caption("Developed by Abbas Fadhil")

st.write("ارفع صورة ورقة الطماطة حتى يقوم الذكاء الاصطناعي بتحليلها.")

uploaded_file = st.file_uploader(
    "اختر صورة ورقة الطماطة",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة المرفوعة", use_container_width=True)

    if st.button("🔍 تشخيص المرض", type="primary"):
        with st.spinner("جاري تحليل الصورة..."):
            resized = image.resize((224, 224))
            img_array = np.array(resized, dtype=np.float32)
            img_array = preprocess_input(img_array)
            img_array = np.expand_dims(img_array, axis=0)

            predictions = model.predict(img_array, verbose=0)[0]
            top_indices = np.argsort(predictions)[::-1][:3]

        st.success("اكتمل التشخيص!")

        for i, index in enumerate(top_indices):
            name = class_names[index].replace("_", " ").replace("  ", " ")
            confidence = float(predictions[index]) * 100

            if i == 0:
                st.subheader("النتيجة الرئيسية")
                st.write(f"الحالة: {name}")
                st.metric("نسبة ثقة النموذج", f"{confidence:.2f}%")

            st.write(f"{i+1}. {name}")
            st.progress(confidence / 100)

        st.info("النتيجة تقدير آلي من النموذج وليست بديلاً عن الفحص الزراعي المتخصص.")
