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
import hashlib
import json

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
#st.sidebar.html(HTML)

st.sidebar.image("images/bot.png")

# st.sidebar.write("### Dev space")

tab1, tab2, tab3, tab4 = st.tabs(
    ["🗒️ Step1: Background", "🔎 Step2: Follow-up questions", "🔬 Step 3: Analysis", "📑 Step 4: Review"]
)

with tab1:
    st.info(
        """The text below should describe the
purpose, the input, the target group and the expected outcome of the social or behavioural
innovation you are evaluating. Please read the text and adapt. When you are done, tick “I
am happy with it” and continue to the follow-up questions in the next section by navigating
the menu in the top row"""
    )

    if not "FirstInput" in st.session_state.keys():
        MQ = intern.CERNA
    else:
        MQ = st.session_state["FirstInput"]

    FirstInput = st.text_area(
        "Text to analyze", intern.CERNA,
        height=400, key="FirstInput"
    )
    step1 = st.checkbox("I am happy with this text", value=False, key="_step1")
    if not st.session_state["_step1"]:
        for key in ["_step2", "_step3"]:
            st.session_state[key] = False


with tab2:
    if st.session_state["_step1"]:

        if not "STEP1MD5" in st.session_state.keys():
            st.session_state["STEP1MD5"] = hashlib.md5(
                FirstInput.encode("utf-8")
            ).hexdigest()
            st.rerun()
        elif (
            hashlib.md5(FirstInput.encode("utf-8")).hexdigest()
            != st.session_state["STEP1MD5"]
        ):
            st.session_state["STEP1MD5"] = hashlib.md5(
                FirstInput.encode("utf-8")
            ).hexdigest()
            st.rerun()
        Q = {}

        st.write("# Follow-up questions")
        st.info("""In this step, we will make sure that all aspects of the evaluation of the innovation are 
covered. You will be asked 15 questions, and the answers are pre-filled. It is your job to read 
the answers and adapt the text so that it corresponds to the execution of the innovation 
activity. When you are done, please tick “I am happy with this” and continue to Step 3”."""
        )
        with open("questions.txt", "r") as f:
            t = [x.strip() for x in f.read().split("\n") if len(x.strip())]
        print("## Tab2")
        for k in t:

            PROMPT = """# Mission

    * You are an international expert in behavioural science and social innovation. You are part of a team of experts working on the assessment and evaluation of social or behavioural innovations, which is detailed below. Your communication style is kind, to-the-point and professional.
    * You need to answer this question, in relation to the text in the next section, in up to three short sentences:
    * QQQ
    * If the text to review does not have enough information, start your answer with "Insufficient information", and if you can, ask for more details.

    # Text to review
    """
            PROMPT = PROMPT.replace("QQQ", k)

            st.write("### " + k)

            if not k in st.session_state.keys():
                MQ = h.ask(
                    PROMPT,
                    st.session_state["FirstInput"],
                    v="gpt-4o-mini",
                    ow=False,
                    src="none",
                    seed="",
                )

            else:
                MQ = st.session_state[k]
            if  "expected impact" in k:
                MQ = st.text_area(label ="""If you expect no impact on this dimension, please just write “No impact expected”""" , value = MQ, height=170, key=k)
            elif "time horizon" in k:
                MQ = st.text_area(label = "Please describe the expected short-term, mid-term and long-term impact (if any)", value = MQ, height=170, key=k)
            else:
                MQ = st.text_area(label = k, value = MQ, height=170, key=k)

            Q[k] = MQ

        for k in list(Q.keys()):
            ADDINFO = (
                "\n\n* Question: " + k + "\n\n* Answer: " + st.session_state[k] + "\n\n"
            )
        st.session_state["ADDINFO"] = ADDINFO
        step2 = st.checkbox("I am happy with this.", value=False, key="_step2")
        if not st.session_state["_step2"]:
            for key in ["_step3"]:
                st.session_state[key] = False
    else:
        st.warning(
            "You need to validate the previous step -- look towards the end, and tick the 'I'm done' button."
        )


with tab3:
    if st.session_state["_step1"] and st.session_state["_step2"]:
        if not "STEP2MD5" in st.session_state.keys():
            st.session_state["STEP2MD5"] = hashlib.md5(
                st.session_state["ADDINFO"].encode("utf-8")
            ).hexdigest()
            st.rerun()
        elif (
            hashlib.md5(st.session_state["ADDINFO"].encode("utf-8")).hexdigest()
            != st.session_state["STEP2MD5"]
        ):
            st.session_state["STEP2MD5"] = hashlib.md5(
                st.session_state["ADDINFO"].encode("utf-8")
            ).hexdigest()
            st.rerun()
        st.info("""You will now be presented 
with the evaluation of the innovation activity. Please go through this and correct the text if 
needed. When you are done, tick “I am happy with this” and continue to download the report 
in Step 4: Review”."""
        )
        st.write("# Report generation")
        with open("report.txt", "r") as f:
            t = [x.strip() for x in f.read().split("\n") if len(x.strip())]
        print("## Tab3")
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
            PROMPT = PROMPT.replace("QQQ", k)
            PROMPT = PROMPT.replace("AAA", st.session_state["ADDINFO"])
            PROMPT = PROMPT.replace("OOO", st.session_state["FirstInput"])

            st.write("#### " + k)

            if not k in st.session_state.keys():
                RS = h.ask(
                    PROMPT,
                    st.session_state["FirstInput"],
                    v="gpt-4o-mini",
                    ow=False,
                    src="none",
                    seed="",
                )

            else:
                RS = st.session_state[k]
            Q[k] = RS

            st.text_area(k, RS, height=600, key=k)
            # st.write(RS)

        step3 = st.checkbox("I am happy with this text", value=False, key="_step3")
    else:
        st.warning(
            "You need to validate the previous step -- look towards the end and tick the 'I'm done' button."
        )


with tab4:
    if (
        st.session_state["_step1"]
        and st.session_state["_step2"]
        and st.session_state["_step3"]
    ):
        st.write("# Final report")
        st.info("""

“We have now prepared the final evaluation report for you. The report 
consists of a summary of 3 key _outputs, outcomes_, and expected _impact_ of the social or 
behavioural innovation. It also includes a summary of the _lessons learned_ during the 
implementation of the social or behavioural innovation. and _3 recommendations for future 
implementation_ as well as an _evaluation_ and a _colour-coded overview_. Please retrieve the 
file and make sure to send it to your Work Package leader.”

        """)
        CERNA_review = {}
        F, A = intern.flavors, list(intern.angles.keys())
        CLARIFS = ""
        for k in list(Q.keys()):
            CLARIFS += "* __Question__: " + k + "\n"
            CLARIFS += "* __Answer__: " + st.session_state[k] + "\n\n"
        for f in F:
            CERNA_review[f] = {}
            for a in A:
                # print(f, a)
                P = intern.createBackground(f, a)
                # st.sidebar.write(h.GOTOCACHE)
                # st.sidebar.write(h.DB)
                assessment = h.ask(
                    P,
                    "## Original text:\n\n"
                    + st.session_state["FirstInput"]
                    + "\n\n## Additional information\n\n"
                    + CLARIFS,
                    v="gpt-4o-mini",
                    ow=False,
                    src="none",
                    seed="",
                )
                CERNA_review[f][a] = assessment

        CERNA_review = intern.augmentReview(CERNA_review)
        st.session_state["CERNA_review"] = CERNA_review
        # Creates excel file
        book = intern.getWorkbook(CERNA_review, st.session_state["FirstInput"], Q)
        df = pd.DataFrame(CERNA_review)

        with NamedTemporaryFile() as tmp:
            book.save(tmp.name)
            data = BytesIO(tmp.read())

        st.download_button(
            "Retrieve file", data=data, mime="xlsx", file_name="assessment.xlsx"
        )

        #st.table(df)
    else:
        st.warning(
            "You need to validate the previous step -- look towards the end and tick the 'I'm done' button."
        )


def clearall():
    for key in st.session_state.keys():
        del st.session_state[key]


if st.sidebar.button("Clear everything"):
    clearall()
    st.session_state["_step1"] = False
    st.rerun()


SESSION = {}
for k in st.session_state.keys():
    SESSION[k] = st.session_state[k]

if False:
    st.sidebar.download_button(
        label="Debug log",
        file_name="data.json",
        mime="application/json",
        data=json.dumps(SESSION),
    )
