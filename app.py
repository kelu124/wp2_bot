import streamlit as st
import OAI
import intern
from io import BytesIO
from tempfile import NamedTemporaryFile

st.set_page_config(
    page_title="Cool bot",
    page_icon="🤖",
    layout="wide",
)


h = OAI.Helper("wp2_assistant")
h.GOTOCACHE = "./"

st.write("# Cool bot")
st.sidebar.write("### Debug space")
st.info("Input below the text to review")
txt = st.text_area(
    "Text to analyze",
    intern.CERNA,
    height = 400,
    )

if st.button("Process"):
    CERNA_review = {}
    F, A = intern.flavors, list(intern.angles.keys())
    for f in F:
        CERNA_review[f] = {}
        for a in A:
            print(f,a)
            P = intern.createBackground(f, a)
            assessment = h.ask(P,txt,v="gpt-3.5-turbo-16k-0613",ow=False,src="none",seed="")
            CERNA_review[f][a] = assessment

    book = intern.getWorkbook(CERNA_review,txt)

    with NamedTemporaryFile() as tmp:
        book.save(tmp.name)
        data = BytesIO(tmp.read())

    st.download_button("Retrieve file",
        data=data,
        mime='xlsx',
        file_name="assessment.xlsx")