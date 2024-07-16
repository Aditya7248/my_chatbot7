import streamlit as st  # type: ignore
import json
import random
from fuzzywuzzy import process  # type: ignore

# Load intents file
def load_intents():
    with open('mydetails.json') as file:
        data = json.load(file)
    return data

# Function to get a random response based on user input
def get_response(user_input, intents):
    all_patterns = []
    intent_map = {}
    
    # Build a list of all patterns and a mapping to their intents
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            all_patterns.append(pattern)
            intent_map[pattern] = intent

    # Find the best match for the user input
    best_match = process.extractOne(user_input, all_patterns, scorer=process.fuzz.partial_ratio)
    
    # Check if the match is good enough (threshold can be adjusted)
    if best_match[1] >= 70:
        matched_pattern = best_match[0]
        matched_intent = intent_map[matched_pattern]
        
        # Format the response for certain intents to be bullet-pointed
        if matched_intent['tag'] in ['education', 'work_experience', 'skills', 'projects', 'achievements', 'interests']:
            response = "<ul>"
            for item in matched_intent['responses']:
                response += f"<li>{item}</li>"
            response += "</ul>"
            return response
        else:
            return random.choice(matched_intent['responses'])
    
    return "I'm sorry, I don't understand. Could you please rephrase?"

# Streamlit app
def main():
    st.set_page_config(page_title="Aditya's AI Assistant", page_icon=":robot_face:", layout="centered")

    # Custom CSS for styling
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="header">
            <img src="https://cdn-icons-png.flaticon.com/512/10817/10817417.png" alt="robot" class="avatar">
            <h2>Aditya's AI Assistant</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("Hello! I'm here to assist you. Ask me anything about Aditya.")

    intents = load_intents()

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    def handle_user_input():
        user_input = st.session_state.input
        st.session_state.conversation.append(("user", user_input))
        response = get_response(user_input, intents)
        st.session_state.conversation.append(("bot", response))
        st.session_state.input = ""  # Clear the input after sending

    # Display conversation
    for entity, message in st.session_state.conversation:
        if entity == "user":
            st.markdown(f'<div class="chat-bubble user">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble bot">{message}</div>', unsafe_allow_html=True)

    # Message input section at the bottom
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    st.text_input("Enter your message:", key="input", on_change=handle_user_input)
    if st.button("Send"):
        handle_user_input()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
