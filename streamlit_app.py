import streamlit as st
import openai
from redlines import Redlines
import pyperclip


def setup_openai():
    openai.api_key = st.secrets['OPENAI_API_KEY']
    client = openai.OpenAI()
    return client


def get_completion(prompt, model="gpt-3.5-turbo-0613"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


@st.experimental_fragment
def add_copy(text):
    copy_button = st.button("Copy to clipboard")
    if copy_button:
        pyperclip.copy(text)
        st.toast("Copied to clipboard")


def create_ui():
    task_summarise = 'Summarise'
    task_proofread = 'Proofread'
    option = st.selectbox(
        'Choose Task',
        (task_proofread, task_summarise))
    txt = st.text_area(f'Write your text', height=200,
                       value="", max_chars=10000)

    if option == task_summarise:
        word_limit = st.number_input("Summarise word limit (GPT is not always accurate)", value=60, min_value=5,
                                     max_value=600)

    submitted = st.button('Submit')

    if submitted:
        if len(txt.strip()) == 0:
            st.warning('Input needs to have at least one character.')
            return

        if option == task_proofread:
            if len(txt.strip()) == 0:
                st.warning('Please input something to proofread and correct')
                return

            prompt = f"proofread and correct this text: ```{txt}```"
            response = get_completion(prompt)
            st.text_area('Corrected Version', height=200, value=response, disabled=True)
            add_copy(response)

            with st.expander("See the corrections"):
                diff = Redlines(txt, response)
                st.markdown(diff.output_markdown, unsafe_allow_html=True)

        if option == task_summarise:
            prompt = f"Summarise the text inside delimited by triple backticks within {word_limit} words: '''{txt}''' "
            response = get_completion(prompt)
            word_count = len(response.split())
            st.text_area(f'Summary (word count: {word_count})', height=200, value=response, disabled=True)
            add_copy(response)


client = setup_openai()
create_ui()
