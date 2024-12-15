# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:25:49 2024

@author: Jiaqi Ye
"""

from transformers import pipeline
import streamlit as st
import torch

# Chatbot Module
class ChatbotModule:
    def __init__(self):
        # Initialize predefined responses
        self.responses = {
            "Hi": "Hello!",
            "How are you?": "I am fine, thanks! How are you?",
        }

        # Attempt to load the advanced chatbot model
        device = 0 if torch.cuda.is_available() else -1
        try:
            self.advanced_chatbot = pipeline(task="text2text-generation", model="facebook/blenderbot-400M-distill", device=device)
        except Exception as e:
            self.advanced_chatbot = None
            st.error(f"Failed to load the advanced chatbot model: {e}")

    def simple_chatbot(self, text):
        """Predefined response chatbot."""
        return self.responses.get(text, "Sorry, I don't understand that.")

    def get_response(self, text, bot="simple"):
        """Get response from the selected chatbot."""
        if bot == "advanced" and self.advanced_chatbot:
            return self.advanced_chatbot(text)[0]['generated_text']
        elif bot == "simple":
            return self.simple_chatbot(text)
        else:
            return "The advanced chatbot is currently unavailable. Please use predefined responses."

    def display_chatbot(self):
        """Streamlit GUI for the chatbot."""
        st.subheader("Interactive Chatbot")

        # Initialize session state for chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Text input for user messages
        user_input = st.text_input("Message to the chatbot:", "")

        if st.button("Send") and user_input:
            # Cache the response to minimize repeated computation
            @st.cache_data(show_spinner=False)
            def cached_response(text, bot="simple"):
                return self.get_response(text, bot)

            # Choose which chatbot to use (toggle between advanced and simple for testing)
            chatbot_type = "advanced" if self.advanced_chatbot else "simple"

            # Generate response
            response = cached_response(user_input, bot=chatbot_type)

            # Append the user input and response to the chat history
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("chatbot", response))

        # Display chat history with alignment
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"<div style='text-align:right;'><b>You:</b> {message}</div>", unsafe_allow_html=True)
            elif role == "chatbot":
                st.markdown(f"<div style='text-align:left;'><b>Chatbot:</b> {message}</div>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     chatbot_app = ChatbotModule()
#     chatbot_app.main()
