import streamlit as st
import time

# Streamed response generator
def response_generator(prompt):
    if prompt == "done":
        all_order = ""
        for item in st.session_state.order_list:
            all_order += str(item) + ", "
        response = "Thank you! You ordered:"+ all_order[:-2] + ". Please wait a minute."
    else:
        # Check if the order exists in drink list
        if prompt in drink_list:
            response = "You ordered " + prompt + "."
            st.session_state.order_list.append(prompt)
        else:
            response = "We do not have " + prompt

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Sample :blue[App]")

# drink list
drink_list = ["Coke", "Orange Juice", "Oolong Tea", "Coffee", "Beer", "Sake"]

# Initialize order list
if "order_list" not in st.session_state:
    st.session_state.order_list = []

# Initialize chat history
all_menu = ""
for item in drink_list:
    all_menu += "- " + str(item) + "\n"
initial_message = f"Hi! What would you like to order? Our menu: \n{all_menu}\nType 'done' to complete your order."
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": initial_message}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your reply!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
