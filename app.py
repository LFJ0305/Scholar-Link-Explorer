import streamlit as st
from services.profile_services import get_or_create_profile


st.set_page_config(
    page_title="Scholar Link Explorer",
    page_icon="🔗",
    layout="centered"
)


st.title("Scholar Link Explorer")
st.write("Paste your profile URL to begin.")


if "current_profile" not in st.session_state:
    st.session_state.current_profile = None


with st.form("profile_url_form"):
    profile_url = st.text_input(
        "Profile URL",
        placeholder="https://profiles.ucl.ac.uk/..."
    )

    submitted = st.form_submit_button("Submit")


if submitted:
    if not profile_url.strip():
        st.error("Please enter a valid profile URL.")
    else:
        with st.spinner("Creating profile page..."):
            try:
                profile = get_or_create_profile(profile_url)
                st.session_state.current_profile = profile
                st.success("Profile created successfully.")
            except Exception as e:
                st.error("Something went wrong while processing this profile.")
                st.exception(e)


if st.session_state.current_profile:
    profile = st.session_state.current_profile
    raw_profile = profile.get("raw_profile", {})

    st.divider()

    st.subheader("Profile Preview")

    st.write("### Name")
    st.write(raw_profile.get("name", ""))

    st.write("### Bio")
    st.write(raw_profile.get("bio", ""))

    st.write("### Fields of Research")
    st.write(raw_profile.get("fields", ""))

    st.write("### Research Interests")
    st.write(raw_profile.get("research_interests", ""))

    st.divider()

    st.caption(f"Profile ID: {profile.get('profile_id')}")
    st.caption(f"Source URL: {profile.get('profile_url')}")