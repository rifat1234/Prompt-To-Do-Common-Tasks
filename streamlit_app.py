import streamlit as st
import openai



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

        if submitted:
            response = get_completion("who is the best footballer?")
            print(response)


openai.api_key = st.secrets['OPENAI_API_KEY']
client = openai.OpenAI()
create_ui()
print("running")
#response = get_completion("who is the best footballer?")
#print(response)
