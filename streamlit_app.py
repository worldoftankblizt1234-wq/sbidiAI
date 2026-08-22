import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, random

st.set_page_config(page_title="Shop Mây")
st.title("🎀 Shop Mây - Không cần API")

@st.cache_resource
def load_bot():
    name = "Qwen/Qwen2.5-0.5B-Instruct"
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(
        name,
        device_map="cpu",
        load_in_4bit=True, # nén xuống 400MB cho vừa 1GB
        low_cpu_mem_usage=True
    )
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

    messages = [
        {"role": "system", "content": "Bạn là Mây, nhân viên shop quần áo, nói tiếng Việt ngắn gọn, vui vẻ."},
        {"role": "user", "content": q}
    ]
    input_ids = tok.apply_chat_template(messages, return_tensors="pt")

    out = model.generate(input_ids, max_new_tokens=120, temperature=0.7, do_sample=True)
    reply = tok.decode(out[0][input_ids.shape[1]:], skip_special_tokens=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
