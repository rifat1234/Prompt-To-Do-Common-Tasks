import streamlit as st

def create_ui():
    with st.form("my_form"):
        task1 = 'Summarise'
        task2 = 'Proofread'
        option = st.selectbox(
            'Choose your preferred Task',
            (task1, task2))
        txt = st.text_area(f'Write your text', height=500,
                           value="", max_chars=10000)
        # Every form must have a submit button.
        submitted = st.form_submit_button('Submit')


create_ui()