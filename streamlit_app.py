import streamlit as st
from transformers import pipeline
import random

st.set_page_config(page_title="Shop Mây")
st.title("🎀 Shop Mây")

@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="HuggingFaceTB/SmolLM2-135M-Instruct", device_map="cpu")

bot = load_bot()

with st.sidebar:
    st.header("🎡 Vòng quay")
    if st.button("Quay ngay!"):
        st.success(random.choice(["Giảm 10%", "Freeship", "Tặng sticker"]))

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if q := st.chat_input("Hỏi gì đi..."):
    st.session_state.messages.append({"role": "user", "content": q})
    st.chat_message("user").write(q)

    # Prompt fix để nó không trả lời toán khi chào hi
    prompt = f"<|im_start|>system\nBạn là Mây, nhân viên shop quần áo, chỉ tư vấn shop, không làm toán.<|im_end|>\n<|im_start|>user\n{q}<|im_end|>\n<|im_start|>assistant\n"

    result = bot(prompt, max_new_tokens=100, do_sample=True, temperature=0.7, truncation=True)
    reply = result[0]['generated_text'].replace(prompt, "").strip()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
