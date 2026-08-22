import streamlit as st
from transformers import pipeline
import random

st.set_page_config(page_title="Shop Mây")
st.title("🎀 Shop Mây")

@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="HuggingFaceTB/SmolLM2-135M-Instruct")

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
    reply = bot(f"User: {q}\nAssistant:", max_new_tokens=100)[0]['generated_text'].split("Assistant:")[-1]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
