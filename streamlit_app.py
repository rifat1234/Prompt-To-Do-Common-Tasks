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



def create_ui():
    task_summarise = 'Summarise'
    task_proofread = 'Proofread'
    option = st.selectbox(
        'Choose your preferred Task',
        (task_summarise, task_proofread))
    txt = st.text_area(f'Write your text', height=200,
                       value="", max_chars=10000)

    if option == task_summarise:
        word_limit = st.number_input("Summarise word limit", value=30, min_value=10, max_value=300)




    submitted = st.button('Submit')

    if submitted:
        if len(txt.strip()) == 0:
            st.warning('Input needs to have at least one character.')
            return

        if option == task_proofread:
            if len(txt.strip()) == 0:
                st.warning('Please input something to proofread and correct')
                return

            # text1 = 'I like icecream'
            # text2 = 'I liked icecream'
            # diff = Redlines(text1, text2)
            # st.markdown(diff.output_markdown, unsafe_allow_html=True)

            prompt = f"proofread and correct this text: ```{txt}```"
            response = get_completion(prompt)
            diff = Redlines(txt, response)
            st.markdown(diff.output_markdown, unsafe_allow_html=True)
            if st.button("Copy to clipboard"):
                pyperclip.copy(response)
                st.success("Copied to clipboard")
        # prompt = f"Summarise the text inside "
        # print(prompt)
        # response = get_completion("who is the best footballer?")
        # print(response)


client = setup_openai()
create_ui()

