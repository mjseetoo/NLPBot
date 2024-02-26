import os
import streamlit as st


wait = 0



st.subheader("Enter Your Credentials")
api_key = st.text_input("Enter API Key:")
project_id = st.text_input("Enter Project ID:")


def get_credentials():
    return {
        "url" : "https://us-south.ml.cloud.ibm.com",
        "apikey" : api_key
    }

model_id = "meta-llama/llama-2-70b-chat"

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 100,
    "stop_sequences": ["\n\n"],
    "repetition_penalty": 1
}

space_id = os.getenv("SPACE_ID")

from ibm_watson_machine_learning.foundation_models import Model

def make_model(model_id, parameters, project_id, space_id):
    model = Model(
        model_id = model_id,
        params = parameters,
        credentials = get_credentials(),
        project_id = project_id,
        space_id = space_id
        )

    return model


prompt_input = """You are an NLP Chat bot questions about an NLP course given the syllabus below. If the syllabus does
     not explicitly have an answer, if you don't have the answer, say 'I don't know, you might want to ask 
     the instructor'.

    Syllabus: 
    ###

    Natural Language Processing (NLP) is the engineering art and science of how to teach computers to understand
    human language. NLP is a type of artificial intelligence technology, and it’s now ubiquitous – NLP lets us talk to
    our phones, use the web to answer questions, map out discussions in books and social media, and even translate
    between human languages. Since language is rich, ambiguous, and very difficult for computers to understand,
    these systems can sometimes seem like magic – but these are engineering problems we can tackle with data, math,
    and insights from linguistics.
    1
    1.1 Course Objective
    This course will introduce NLP methods and applications including probabilistic language models, machine trans-
    lation, and parsing algorithms for syntax and the deeper meaning of text. During the course, students will (1)
    learn and derive mathematical models and algorithms for NLP; (2) become familiar with key facts about human
    language that motivate them, and help practitioners know what problems are possible to solve; and (3) complete
    a series of hands-on projects to implement, experiment with, and improve NLP models, gaining practical skills for
    natural language systems engineering.
    By the end of the semester students will:
    • Acquire the fundamental linguistic concepts that are relevant to language technology.
    • Analyze and understand state-of-the-art algorithms and statistical techniques for reasoning about linguistic
    data.
    • Implement state-of-the-art algorithms and statistical techniques for reasoning about linguistic data.
    • Adapt and apply state-of-the-art language technology to new problems and settings.
    • Read and understand current research on natural language processing.
    • Exercise public speaking skills by discussing various course topics with classmates, asking and answering
    questions, and doing group presentations.
    By the end of this course students should be able to transfer the knowledge gained, and apply it outside of the
    context of the course to:
    • Identify, formulate, analyze, and solve complex computing or engineering problems by applying principles of
    computing, engineering, science, and mathematics.
    • Design, implement, and evaluate a computing or engineering solution to meet a given set of requirements,
    with consideration of public health, safety, and welfare, as well as global, cultural, social, environmental, and
    economic factors.
    • Communicate effectively in a variety of professional contexts, with a range of audiences.
    • Function effectively as a member or leader of a team engaged in activities appropriate to the program’s
    discipline, creating a collaborative and inclusive environment, establishing goals, planning tasks, and meeting
    objectives.
    1.2 Prerequisites
    • For CSCI 4140: CSCI 2540 Data Abstraction and Object-Oriented Data Structures, MATH 2228 Elementary
    Statistical Methods I, or MATH 2283 Statistics for Business.
    • For CSCI/DASC 6040: enrolled in the master of science in computer science, data science, or software
    engineering programs or consent of instructor.
    1.3 Course materials
    • Optional: Speech and Language Processing (SLP) – an introduction to natural language processing, compu-
    tational linguistics, and speech recognition.
    • Optional: Dive into Deep Learning (D2L) – interactive deep learning book with code, math, and discussions.
    Tue 01/09 Introduction
    Thu 01/11 N-gram LMs
    - Homework 1 on N-gram LMs released (due Sun 1/21)
    - Optional: Introduction to Python (videos)
    Tue 01/16 Vector embeddings
    - Homework 2 on Exploring Word Vectors released (due Sun 2/04)
    - Homework 3 on word2vec released (due Sun 2/18)
    Thu 01/18 Steamship LMMs
    - Homework 4 on LMM applications released (due Sat 3/02)
    Tue 01/23 Artificial neural networks
    Thu 01/25 Final project details (video; no class)
    Tue 01/30 Recurrent neural networks
    Thu 02/01 PyTorch tutorial
    Tue 02/06 Fancy RNNs (videos; no class)
    - Homework 5 on Neural Machine Translation with RNNs and Analyzing NMT Systems
    released (due Sun 3/17)
    Thu 02/08 Self-attention and transformers (videos; no class)
    Tue 02/13 Hugging face tutorial
    Thu 02/15 Nano GPT
    - Homework 6 on Nano GPT released (due on Sun 3/31)
    Tue 02/20 Pretraining
    - Homework 7 on Self-Attention, Transformers, and Pretraining released (due on Sun 4/14)
    Thu 02/22 Guest lecture on public speaking
    Tue 02/27 Neural language generation
    Thu 02/29 Prompting, instruction fine-tuning, and RLHF
    Sun 03/03 Spring break
    Sun 03/10 Spring break
    Tue 03/12 Qestion answering
    Thu 03/14 CNN, TreeRNN
    Tue 03/19 Code generation
    Thu 03/21 Multimodal deep learning
    Tue 03/26 Model analysis and explenation
    Thu 03/28 Model interpretability and editing
    Tue 04/02 Ethical issues related to NLP
    Thu 04/04 Course wrap-up
    Tue 04/09 Final project presentations
    Thu 04/11 Final project presentations
    Tue 04/16 Final project presentations
    Thu 04/18 Final project presentations
    ###

    Question: When does this class end?
    Answer: The course ends on 3:30 on Tuesdays and Thursdays, however it will fully conclude on May 6th.

    Question: What is NLP
    Answer: The syllabus gives the description for NLP: Natural Language Processing (NLP) is the engineering art and science of how to teach computers to understand human language.

    Question: """

try:
    model = make_model(model_id, parameters, project_id, space_id)

except Exception as e:
    st.text("Waiting for keys")

try:
    st.title('Ask the NLP Bot')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.text_input('Ask your question here')

    if prompt:
        st.chat_message('user').markdown(prompt)

        st.session_state.messages.append({'role': 'user', 'content': prompt})

        LLM_Response = model.generate_text(prompt=prompt_input + prompt + "Answer: ")

        st.chat_message('assistant').markdown(LLM_Response)

        st.session_state.messages.append({
            'role': 'assistant', 'content': LLM_Response
        })
except Exception as e:
    st.text("Correct keys have not been entered yet")
