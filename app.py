from services.profile_service import get_or_create_profile
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

from scraper import scrape_profile

if submitted:
    if profile_url.strip():
        st.success("Processing profile...")

        data = get_or_create_profile(profile_url)

        st.subheader("Extracted Data")

        st.write("**Name:**", data["name"])
        st.write("**Bio:**", data["bio"])
        st.write("**Fields:**", data["fields"])
        st.write("**Research Interests:**", data["research_interests"])
    else:
        st.error("Please enter a valid profile URL.")