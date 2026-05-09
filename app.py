import streamlit as st

st.set_page_config(
    page_title="Scholar Link Explorer",
    page_icon="🔗",
    layout="centered"
)

if "submitted_url" not in st.session_state:
    st.session_state.submitted_url = ""

st.title("Scholar Link Explorer")
st.caption("Enter your public profile URL to start.")

with st.container(border=True):
    with st.form("profile_form"):
        profile_url = st.text_input(
            "Profile URL",
            placeholder="https://www.example.com/profile"
        )
        submitted = st.form_submit_button("Submit")

if submitted:
    cleaned_url = profile_url.strip()

    if cleaned_url:
        st.session_state.submitted_url = cleaned_url
        st.success("Profile URL received.")
    else:
        st.error("Please paste a profile URL before submitting.")

if st.session_state.submitted_url:
    st.subheader("Current input")
    st.code(st.session_state.submitted_url, language=None)