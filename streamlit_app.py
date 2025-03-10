import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from llamaapi import LlamaAPI  # Hypothetical LLaMA API library

st.set_page_config(page_title="LlamaChat - An LLM-powered Streamlit app")

# Initialize LLaMA API (you'll need to replace with your actual API key)
llama = LlamaAPI("your_api_key_here")

with st.sidebar:
    st.title('🦙💬 LlamaChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [LLaMA API](<https://example.com/llama-api>)  # Replace with actual LLaMA API link
    - LLaMA 70B Instruct model
    
    💡 Note: API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](<https://youtube.com/dataprofessor>)')

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm LlamaChat, How may I help you?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

with input_container:
    user_input = get_text()

# Response output
def generate_response(prompt):
    # Configure the API request for LLaMA 70B Instruct
    api_request = {
        'model': 'llama-70b-instruct',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful AI assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 500,
        'temperature': 0.7
    }
    
    try:
        response = llama.generate(api_request)
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))
