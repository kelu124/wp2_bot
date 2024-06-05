import streamlit as st
import OAI
import intern
from io import BytesIO
from tempfile import NamedTemporaryFile
from pymongo import MongoClient
import pandas as pd
import os

st.set_page_config(
    page_title="Cool bot",
    page_icon="🤖",
    layout="wide",
)


h = OAI.Helper("wp2_assistant")

h.GOTOCACHE = st.secrets["CACHE"]
h.DBAdress = st.secrets["DB"]
h.DB = st.secrets["DB"]
h.PWD = st.secrets["PWD"]
h.cluster = MongoClient(h.DBAdress)
h.db = h.cluster["OAI"]
h.collection = h.db["OAI_Collection"]
h.DB = h.collection

if not os.path.exists(h.GOTOCACHE):
    os.makedirs(h.GOTOCACHE)

st.write("# Cool bot")
st.sidebar.write("### Debug space")
st.info("Input below the text to review")
txt = st.text_area(
    "Text to analyze",
    intern.CERNA,
    height=400,
)
Q = {}
if st.button("Process"):
    CERNA_review = {}
    F, A = intern.flavors, list(intern.angles.keys())
    for f in F:
        CERNA_review[f] = {}
        for a in A:
            print(f, a)
            P = intern.createBackground(f, a)
            # st.sidebar.write(h.GOTOCACHE)
            # st.sidebar.write(h.DB)
            assessment = h.ask(
                P, txt, v="gpt-3.5-turbo-16k-0613",
                ow=False, src="none", seed=""
            )
            CERNA_review[f][a] = assessment



    st.write("# Mandatory questions")
    with open("questions.txt", "r") as f:
        t = [x.strip() for x in f.read().split("\n") if len(x.strip())]
    for k in t:

        PROMPT = """# Mission

* You are an international expert in behavioural science and social innovation. You are part of a team of experts working on the assessment and evaluation of social or behavioural innovations, which is detailed below. Your communication style is kind, to-the-point and professional.
* You need to answer this question, in relation to the text in the next section, in up to three short sentences:
  * QQQ
* If the text to review does not have enough information, start your answer with "Insufficient information", and if you can, ask for more details.

# Text to review
"""
        PROMPT = PROMPT.replace("QQQ",k)
        MQ = h.ask(PROMPT,txt,v="gpt-3.5-turbo-16k-0613",ow=False,src="none",seed="")
        st.write("### "+k)
        st.write(MQ)
        Q[k] = MQ
    for k in list(Q.keys()):
       ADDINFO = "\n\n* Question: "+k+"\n\n* Answer: "+Q[k]+"\n\n"

    st.write("# Report generation")
    with open("report.txt", "r") as f:
        t = [x.strip() for x in f.read().split("\n") if len(x.strip())]
    for k in t: 
        PROMPT = """# Mission

* You are an international expert in behavioural science and social innovation. You are part of a team of experts working on the assessment and evaluation of social or behavioural innovations, which is detailed below. Your communication style is kind, to-the-point and professional.
* You are preparing a report that analyses an innovation, and you will cover a specific section of this report.
* For the current section, you need to answer this question, in relation to the text and other information in the next section: 'QQQ'

# Text to review

## Original text

OOO

### Additional information

AAA

"""
        PROMPT = PROMPT.replace("QQQ",k)
        PROMPT = PROMPT.replace("AAA",ADDINFO)
        PROMPT = PROMPT.replace("OOO",txt)
        RS = h.ask(PROMPT,txt,v="gpt-3.5-turbo-16k-0613",ow=False,src="none",seed="")
        Q[k] = RS
        st.write("### "+k)
        st.write(RS)


    st.write("# Overview of the table")
    book = intern.getWorkbook(CERNA_review, txt)
    df = pd.DataFrame(CERNA_review)
    st.table(df)

    with NamedTemporaryFile() as tmp:
        book.save(tmp.name)
        data = BytesIO(tmp.read())

    st.download_button(
        "Retrieve file", data=data, mime="xlsx", file_name="assessment.xlsx"
    )
