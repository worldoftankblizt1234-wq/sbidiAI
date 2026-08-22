import streamlit as st
import random
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Shop Mây")
st.title("🎀 Shop Mây - AI tư vấn")

# Vòng quay bên sidebar
with st.sidebar:
    st.header("🎡 Vòng quay may mắn")
    if st.button("Quay ngay!"):
        qua = random.choice(["Giảm 10%", "Giảm 20%", "Freeship", "Tặng sticker", "Chúc may mắn lần sau"])
        st.success(f"Bạn trúng: {qua}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if q := st.chat_input("Hỏi Mây đi..."):
    st.session_state.messages.append({"role": "user", "content": q})
    st.chat_message("user").write(q)
    msgs = [{"role": "system", "content": "Bạn là Mây, nhân viên shop vui vẻ, nói ngắn gọn"}] + st.session_state.messages
    res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=msgs, max_tokens=200)
    reply = res.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
