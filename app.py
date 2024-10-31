import streamlit as st
import time

from swarm import Swarm
from agent_pool import agent_gillie

client = Swarm()

st.set_page_config(page_title="Talk to Gillie", page_icon="avatar/gil_logo.png")
st.title("🎓 Talk to Gillie 🚜")

gillie_avatar = "avatar/gillie_female_realistic.png"
user_avatar = "avatar/user.png"


def response_generator(gen_response):
    for word in gen_response.split():
        yield word + " "
        time.sleep(0.10)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi 👋 my name is Gillie and I am your personal research assistant 👓 for finding relevant scientific knowledge. How are you today?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message(msg["role"], avatar=gillie_avatar).write(msg["content"])
    elif msg["role"] == "user":
        st.chat_message(msg["role"], avatar=user_avatar).write(msg["content"])

if prompt := st.chat_input(placeholder="Reply to Gillie"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=user_avatar).write(prompt)

    messages = st.session_state.messages

    with st.spinner(text="Let me think about that..."):
        response = client.run(agent=agent_gillie, messages=messages)
    
    agent_response = response.messages[-1]["content"]

    with st.chat_message("assistant", avatar=gillie_avatar):
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        st.write_stream(response_generator(agent_response))
