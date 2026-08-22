import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import random, torch

st.set_page_config(page_title="Shop Mây")
st.title("🎀 Shop Mây")

@st.cache_resource
def load_bot():
    name = "HuggingFaceTB/SmolLM2-135M-Instruct"
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype="auto")
    return tok, model

tok, model = load_bot()

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

    # Prompt chuẩn để nó không trả lời toán
    messages = [
        {"role": "system", "content": "Bạn là Mây, nhân viên shop quần áo vui vẻ. Chỉ trả lời về shop, không làm toán."},
        {"role": "user", "content": q}
    ]
    inputs = tok.apply_chat_template(messages, return_tensors="pt")
    out = model.generate(inputs, max_new_tokens=100, temperature=0.7, do_sample=True)
    reply = tok.decode(out[0][inputs.shape[1]:], skip_special_tokens=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
