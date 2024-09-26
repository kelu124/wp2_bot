import streamlit as st
import OAI
import intern
from io import BytesIO
from tempfile import NamedTemporaryFile
from pymongo import MongoClient
import pandas as pd
import os
from fwk_colors import summary, OOI
from openai import OpenAI

st.set_page_config(
    page_title="Evaluation Assistant (EVA - D2.8)",
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
h.CLIENT = OpenAI(api_key=st.secrets["OAI"])

h.NAME = "WP2 Bot"
if not os.path.exists(h.GOTOCACHE):
    os.makedirs(h.GOTOCACHE)

st.write("# Evaluation Assistant (EVA - D2.8)")
HTML = '<img src="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlhoJZrN3D_qPxh-nNb9d9ey1ZSiAls4tGdyX7pOHwivEcckYk" alt="drawing" width="250"/>'
st.sidebar.html(HTML)
# st.sidebar.write("### Dev space")

tab1, tab2, tab3, tab4 = st.tabs(["🗒️ Background", "🔎 Finer questions", "🔬 Analysis", "📑 Review"])

with tab1:
    st.info(
        "Please adapt the text below for an evaluation of the social/behavioral innovation implemented"
    )

    txt = st.text_area(
        "Text to analyze",
        intern.CERNA,
        height=400,
        key = "FirstInput"
    )
    step1 = st.checkbox("I am happy with this text", value=False, key="_step1") 
    if not st.session_state["_step1"]:
        for key in ["_step2","_step3"]:
            st.session_state[key] = False


with tab2:
    if st.session_state["_step1"]:
        Q = {}

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
            PROMPT = PROMPT.replace("QQQ", k)
            MQ = h.ask(PROMPT, txt, v="gpt-4o-mini", ow=False, src="none", seed="")
            st.write("### " + k)

            MQ = st.text_area(k, MQ, height=170, key=k)
            Q[k] = MQ
        for k in list(Q.keys()):
            ADDINFO = "\n\n* Question: " + k + "\n\n* Answer: " + Q[k] + "\n\n"
        step2 = st.checkbox("I am happy with this.", value=False, key="_step2") 
        if not st.session_state["_step2"]:
            for key in ["_step3"]:
                st.session_state[key] = False
    else:
        st.warning("You need to validate the previous step -- look towards the end and tick the 'I'm done' button.")


        
with tab3:
    if st.session_state["_step1"] and st.session_state["_step2"]:

        st.write("# Report generation")
        with open("report.txt", "r") as f:
            t = [x.strip() for x in f.read().split("\n") if len(x.strip())]
        for k in t:
            print(k)
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
            PROMPT = PROMPT.replace("QQQ", k)
            PROMPT = PROMPT.replace("AAA", ADDINFO)
            PROMPT = PROMPT.replace("OOO", txt)
            RS = h.ask(PROMPT, txt, v="gpt-4o-mini", ow=False, src="none", seed="")
            Q[k] = RS
            st.write("#### " + k)
            txt = st.text_area(
                k,
                RS,
                height=600,
                key = k
            )
            #st.write(RS)


        step3 = st.checkbox("I am happy with this text", value=False, key="_step3") 
    else:
        st.warning("You need to validate the previous step -- look towards the end and tick the 'I'm done' button.")

with tab4:
    if st.session_state["_step1"] and st.session_state["_step2"]  and st.session_state["_step3"]:
        st.write("# Overview of the table")

        CERNA_review = {}
        F, A = intern.flavors, list(intern.angles.keys())
        CLARIFS = ""
        for k in list(Q.keys()):
            CLARIFS += "* __Question__: " + k + "\n"
            CLARIFS += "* __Answer__: " + Q[k] + "\n\n"
        for f in F:
            CERNA_review[f] = {}
            for a in A:
                print(f, a)
                P = intern.createBackground(f, a)
                # st.sidebar.write(h.GOTOCACHE)
                # st.sidebar.write(h.DB)
                assessment = h.ask(
                    P,
                    "## Original text:\n\n"
                    + txt
                    + "\n\n## Additional information\n\n"
                    + CLARIFS,
                    v="gpt-4o-mini",
                    ow=False,
                    src="none",
                    seed="",
                )
                CERNA_review[f][a] = assessment

        CERNA_review = intern.augmentReview(CERNA_review)
        book = intern.getWorkbook(CERNA_review, txt, Q)
        df = pd.DataFrame(CERNA_review)



        with NamedTemporaryFile() as tmp:
            book.save(tmp.name)
            data = BytesIO(tmp.read())

        st.download_button(
            "Retrieve file", data=data, mime="xlsx", file_name="assessment.xlsx"
        )


        st.table(df)
    else:
        st.warning("You need to validate the previous step -- look towards the end and tick the 'I'm done' button.")

def clearall():
    for key in st.session_state.keys():
        del st.session_state[key]


if st.sidebar.button("Clear everything"):
    clearall()
    st.session_state["_step1"] = False
    st.rerun()
