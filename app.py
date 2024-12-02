import base64
import json
import os
from datetime import datetime

import pytz
import streamlit as st
from streamlit_javascript import st_javascript
from user_agents import parse

# Constants
GRID_COLUMNS = 5
TOTAL_DAYS = 25
OUTPUT_IMAGES_DIR = "images/output_images"  # Directory containing individual images

# Get the current day of December
polish_timezone = pytz.timezone("Europe/Warsaw")
current_date = datetime.now(polish_timezone)
CURRENT_DAY = current_date.day if current_date.month == 12 else 0


def load_calendar_data(json_file):
    with open(json_file, "r") as file:
        return json.load(file)


def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")
        return None


def render_button(day):
    image_path = os.path.join(OUTPUT_IMAGES_DIR, f"{day}.jpg")
    base64_image = get_base64_image(image_path)

    # Determine if the button should be clickable
    clickable = day <= CURRENT_DAY

    # Generate the button HTML
    button_html = f"""
    <div style="position: relative; width: 120px; height: 120px; margin: 5px;">
        <button style="
            position: absolute;
            width: 100%;
            height: 100%;
            border: none;
            background: url('data:image/jpeg;base64,{base64_image}') no-repeat center center;
            background-size: cover;
            color: white;
            font-size: 20px;
            font-weight: bold;
            cursor: {'pointer' if clickable else 'not-allowed'};
            pointer-events: {'auto' if clickable else 'none'};
            border-radius: 5px;
        "></button>
    </div>
    """

    # Display the button
    st.markdown(button_html, unsafe_allow_html=True)

    # Streamlit interaction handled via native buttons
    if clickable and st.button(f"Prezent #{day}", key=f"day_{day}", use_container_width=True):
        st.session_state["selected_day"] = day
        render_popup(day)


def application():
    st.title("Kalendarz adwentowy dla Dorotki")
    st.write("Wesołych świąt pięknisiu!")
    for row in range((TOTAL_DAYS - 1) // GRID_COLUMNS + 1):
        cols = st.columns(GRID_COLUMNS)
        for col_idx in range(GRID_COLUMNS):
            day = row * GRID_COLUMNS + col_idx + 1
            if day <= TOTAL_DAYS:
                with cols[col_idx]:
                    render_button(day)


@st.dialog("Prezent")
def render_popup(day):
    calendar_data = load_calendar_data("calendar_data.json")
    if "selected_day" in st.session_state and st.session_state["selected_day"] is not None:
        day = st.session_state["selected_day"]
        day_data = calendar_data.get(str(day), {})

        # Display the popup in a separate section
        st.write(day_data.get("christmas_saying", "Buzi buzi!"))
        if "image_url" in day_data:
            st.image(day_data["image_url"])
        if "youtube_url" in day_data:
            st.video(day_data["youtube_url"])


def authenticate():
    # Check if the authentication status is stored in the session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # Display the password input
        password = st.text_input("Hasło", type="password")

        if password == st.secrets["password"]:
            st.session_state["authenticated"] = True
            st.rerun()  # Rerun the app to update the UI and hide the password input
        elif password:
            st.error("Błędne hasło!")
            st.stop()  # Stop further execution if authentication fails
    else:
        # Proceed to the main app if authenticated
        application()


def check_if_mobile():
    # Check if the app is being accessed from a mobile device
    ua_string = st_javascript("""window.navigator.userAgent;""")
    user_agent = parse(ua_string)
    return user_agent.is_mobile


if __name__ == "__main__":
    if check_if_mobile():
        st.error("Ta aplikacja nie jest obsługiwana na urządzeniach mobilnych. Uruchom ją na komputerze.")
        st.stop()
    else:
        authenticate()
