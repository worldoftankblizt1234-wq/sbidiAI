import streamlit as st
from transformers import pipeline
import random

st.set_page_config(page_title="Shop Mây")
st.title("🎀 Shop Mây")

@st.cache_resource
def load_bot():
    # con này chuyên tiếng Việt, nhẹ
    return pipeline("text-generation", model="bmd1905/vietnamese-gpt2", device_map="cpu")

bot = load_bot()

with st.sidebar:
    st.header("🎡 Vòng quay")
    if st.button("Quay ngay!"):
        st.success(random.choice(["Giảm 10%", "Freeship", "Tặng sticker", "Giảm 20%"]))

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if q := st.chat_input("Hỏi gì đi..."):
    st.session_state.messages.append({"role": "user", "content": q})
    st.chat_message("user").write(q)

    prompt = f"Khách: {q}\nMây shop trả lời:"
    result = bot(prompt, max_new_tokens=60, do_sample=True, temperature=0.7, repetition_penalty=1.2)
    reply = result[0]['generated_text'].replace(prompt, "").strip()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
