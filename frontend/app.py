import streamlit as st
import base64
import requests
import textwrap
import os
import json


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGIN_BACKGROUND = os.path.join(
    BASE_DIR,
    "assets",
    "travel_background.png"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def html(content):
    """
    Removes unnecessary indentation from HTML/CSS.
    """
    return textwrap.dedent(content).strip()


# ============================================================
# LOAD BACKGROUND IMAGE
# ============================================================

def get_image_base64(image_path):

    if not os.path.exists(image_path):
        return ""

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode()


background_base64 = get_image_base64(
    LOGIN_BACKGROUND
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    html(
        f"""
        <style>

        /* =====================================================
           REMOVE DEFAULT STREAMLIT UI
           ===================================================== */

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header {{
            visibility: hidden;
        }}

        [data-testid="stHeader"] {{
            display: none;
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        [data-testid="stDecoration"] {{
            display: none;
        }}


        /* =====================================================
           MAIN PAGE
           ===================================================== */

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.18),
                    rgba(0, 0, 0, 0.30)
                ),
                url("data:image/png;base64,{background_base64}");

            background-size: cover;
            background-position: center top;
            background-attachment: fixed;
        }}


        /* =====================================================
           MAIN CONTAINER
           ===================================================== */

        .block-container {{
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
        }}


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {{
            width: 100%;

            border: none;

            border-radius: 12px;

            background: linear-gradient(
                90deg,
                #12c2e9,
                #0072ff
            );

            color: white;

            font-size: 16px;

            font-weight: 600;

            padding: 0.65rem 1rem;

            transition: all 0.25s ease;
        }}


        .stButton > button:hover {{
            transform: translateY(-2px);

            box-shadow:
                0 8px 20px
                rgba(0, 114, 255, 0.35);
        }}


        /* =====================================================
           FORM SUBMIT BUTTON
           ===================================================== */

        .stFormSubmitButton > button {{
            width: 100%;

            border: none;

            border-radius: 12px;

            background: linear-gradient(
                90deg,
                #12c2e9,
                #0072ff
            );

            color: white;

            font-size: 16px;

            font-weight: 600;

            padding: 0.65rem 1rem;
        }}


        .stFormSubmitButton > button:hover {{
            transform: translateY(-2px);

            box-shadow:
                0 8px 20px
                rgba(0, 114, 255, 0.35);
        }}


        /* =====================================================
           TEXT INPUT
           ===================================================== */

        .stTextInput label {{
            color: white !important;

            font-weight: 600 !important;
        }}


        .stTextInput input {{
            background: rgba(
                255,
                255,
                255,
                0.92
            ) !important;

            border-radius: 10px !important;

            border: none !important;

            color: #111 !important;

            padding: 12px !important;
        }}


        .stTextInput input::placeholder {{
            color: #777 !important;
        }}


        /* =====================================================
           NUMBER INPUT
           ===================================================== */

        .stNumberInput label {{
            color: white !important;

            font-weight: 600 !important;
        }}


        .stNumberInput input {{
            background: rgba(
                255,
                255,
                255,
                0.92
            ) !important;

            color: #111 !important;

            border-radius: 10px !important;

            border: none !important;
        }}


        .stNumberInput button {{
            color: white !important;
        }}


        /* =====================================================
           MULTISELECT
           ===================================================== */

        .stMultiSelect label {{
            color: white !important;

            font-weight: 600 !important;
        }}


        /* =====================================================
           SELECTBOX
           ===================================================== */

        .stSelectbox label {{
            color: white !important;

            font-weight: 600 !important;
        }}


        /* =====================================================
           LOGIN CARD
           ===================================================== */

        .login-card {{
            background: rgba(
                0,
                0,
                0,
                0.60
            );

            backdrop-filter: blur(12px);

            border: 1px solid
                rgba(255, 255, 255, 0.20);

            border-radius: 22px;

            padding: 35px;

            box-shadow:
                0 20px 50px
                rgba(0, 0, 0, 0.40);
        }}


        /* =====================================================
           LOGIN TITLE
           ===================================================== */

        .login-title {{
            color: white;

            font-size: 36px;

            font-weight: 800;

            text-align: center;

            margin-bottom: 5px;
        }}


        .login-subtitle {{
            color: rgba(
                255,
                255,
                255,
                0.75
            );

            font-size: 16px;

            text-align: center;

            margin-bottom: 25px;
        }}


        /* =====================================================
           TRAVEL TAGLINE
           ===================================================== */

        .travel-tagline {{
            color: white;

            font-size: 42px;

            font-weight: 800;

            letter-spacing: 2px;

            text-shadow:
                0 4px 20px
                rgba(0, 0, 0, 0.65);
        }}


        .travel-subtitle {{
            color: rgba(
                255,
                255,
                255,
                0.85
            );

            font-size: 20px;

            margin-top: 10px;

            text-shadow:
                0 2px 10px
                rgba(0, 0, 0, 0.60);
        }}


        /* =====================================================
           DASHBOARD
           ===================================================== */

        .dashboard-title {{
            color: white;

            font-size: 34px;

            font-weight: 800;

            text-shadow:
                0 3px 15px
                rgba(0, 0, 0, 0.60);
        }}


        .dashboard-subtitle {{
            color: rgba(
                255,
                255,
                255,
                0.82
            );

            font-size: 18px;

            margin-top: 5px;
        }}


        /* =====================================================
           FEATURE CARDS
           ===================================================== */

        .feature-card {{
            background: rgba(
                0,
                0,
                0,
                0.48
            );

            backdrop-filter: blur(10px);

            border: 1px solid
                rgba(255, 255, 255, 0.20);

            border-radius: 18px;

            padding: 25px;

            min-height: 170px;

            box-shadow:
                0 15px 30px
                rgba(0, 0, 0, 0.25);
        }}


        .feature-icon {{
            font-size: 38px;
        }}


        .feature-title {{
            color: white;

            font-size: 22px;

            font-weight: 700;

            margin-top: 10px;
        }}


        .feature-description {{
            color: rgba(
                255,
                255,
                255,
                0.72
            );

            font-size: 15px;

            margin-top: 8px;

            line-height: 1.5;
        }}


        /* =====================================================
           SECTION TITLE
           ===================================================== */

        .section-title {{
            color: white;

            font-size: 28px;

            font-weight: 750;

            margin-top: 20px;
        }}


        .section-description {{
            color: rgba(
                255,
                255,
                255,
                0.75
            );

            font-size: 16px;

            margin-bottom: 15px;
        }}


        /* =====================================================
           WEATHER CARD
           ===================================================== */

        .weather-card {{
            background: rgba(
                0,
                0,
                0,
                0.55
            );

            backdrop-filter: blur(10px);

            border: 1px solid
                rgba(255, 255, 255, 0.20);

            border-radius: 18px;

            padding: 25px;

            color: white;
        }}


        /* =====================================================
           TRIP CARD
           ===================================================== */

        .trip-card {{
            background: rgba(
                0,
                0,
                0,
                0.55
            );

            backdrop-filter: blur(10px);

            border: 1px solid
                rgba(255, 255, 255, 0.20);

            border-radius: 18px;

            padding: 22px;

            margin-bottom: 15px;

            color: white;
        }}


        /* =====================================================
           CHAT MESSAGE
           ===================================================== */

        .chat-user {{
            background: rgba(
                0,
                114,
                255,
                0.75
            );

            color: white;

            padding: 12px 16px;

            border-radius: 15px;

            margin: 8px 0;

            margin-left: 20%;
        }}


        .chat-ai {{
            background: rgba(
                0,
                0,
                0,
                0.60
            );

            color: white;

            padding: 12px 16px;

            border-radius: 15px;

            margin: 8px 0;

            margin-right: 20%;
        }}


        /* =====================================================
           FORM
           ===================================================== */

        [data-testid="stForm"] {{
            background: rgba(
                0,
                0,
                0,
                0.35
            );

            border: 1px solid
                rgba(255, 255, 255, 0.15);

            border-radius: 18px;

            padding: 20px;
        }}

        </style>
        """
    )
)


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state["token"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "trip_result" not in st.session_state:
    st.session_state["trip_result"] = None

if "weather_result" not in st.session_state:
    st.session_state["weather_result"] = None

if "show_planner" not in st.session_state:
    st.session_state["show_planner"] = False

if "active_section" not in st.session_state:
    st.session_state["active_section"] = None

if "chat_session_id" not in st.session_state:
    st.session_state["chat_session_id"] = None

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []


# ============================================================
# API URL
# ============================================================

API_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8001"
)


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state["token"]:

    st.html("<br><br><br>")

    left, right = st.columns(
        [1.15, 0.85],
        gap="large"
    )


    # ========================================================
    # LEFT SIDE
    # ========================================================

    with left:

        st.html("<br><br><br>")

        st.html(
            html(
                """
                <div class="travel-tagline">
                    DREAM ✦ PLAN ✦ EXPLORE
                </div>

                <div class="travel-subtitle">
                    Let AI plan your perfect journey 🌍
                </div>
                """
            )
        )


    # ========================================================
    # RIGHT SIDE LOGIN CARD
    # ========================================================

    with right:

        st.html(
            html(
                """
                <div class="login-card">

                    <div class="login-title">
                        🌍 AI Trip Planner
                    </div>

                    <div class="login-subtitle">
                        Your Smart Travel Companion
                    </div>

                </div>
                """
            )
        )


        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )


        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )


        st.html("<br>")


        login_clicked = st.button(
            "🚀 Login"
        )


        if login_clicked:

            if not username or not password:

                st.warning(
                    "Please enter username and password."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/login",

                        json={
                            "username": username,
                            "password": password
                        },

                        timeout=10
                    )


                    if response.status_code == 200:

                        data = response.json()


                        if "access_token" in data:

                            st.session_state["token"] = (
                                data["access_token"]
                            )

                            st.session_state["username"] = (
                                username
                            )

                            st.success(
                                "Login successful! 🎉"
                            )

                            st.rerun()


                        else:

                            st.error(
                                data.get(
                                    "message",
                                    "Invalid username or password."
                                )
                            )


                    else:

                        st.error(
                            "Login failed. "
                            "Please check your credentials."
                        )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to backend. "
                        "Make sure FastAPI is running."
                    )


                except requests.exceptions.Timeout:

                    st.error(
                        "Backend request timed out."
                    )


                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# ============================================================
# DASHBOARD
# ============================================================

else:

    # ========================================================
    # TOP NAVIGATION
    # ========================================================

    st.html(
        html(
            """
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                padding:10px 5px;
            ">

                <div style="
                    color:white;
                    font-size:28px;
                    font-weight:800;
                ">
                    🌍 AI Trip Planner
                </div>

                <div style="
                    color:rgba(255,255,255,0.80);
                    font-size:15px;
                ">
                    Your Smart Travel Companion
                </div>

            </div>
            """
        )
    )


    # ========================================================
    # WELCOME MESSAGE
    # ========================================================

    st.html(
        html(
            f"""
            <div class="dashboard-title">
                Welcome back, {st.session_state["username"]}! 👋
            </div>

            <div class="dashboard-subtitle">
                Where will your next adventure take you? 🌎
            </div>
            """
        )
    )


    st.html("<br>")


    # ========================================================
    # FEATURE CARDS
    # ========================================================

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )


    # ========================================================
    # CHAT CARD
    # ========================================================

    with col1:

        st.html(
            html(
                """
                <div class="feature-card">

                    <div class="feature-icon">
                        💬
                    </div>

                    <div class="feature-title">
                        AI Travel Chat
                    </div>

                    <div class="feature-description">
                        Talk with your intelligent
                        travel assistant and refine
                        your trip using conversation.
                    </div>

                </div>
                """
            )
        )


    # ========================================================
    # MY TRIPS CARD
    # ========================================================

    with col2:

        st.html(
            html(
                """
                <div class="feature-card">

                    <div class="feature-icon">
                        🧳
                    </div>

                    <div class="feature-title">
                        My Trips
                    </div>

                    <div class="feature-description">
                        View your previous adventures
                        and saved AI-generated
                        itineraries.
                    </div>

                </div>
                """
            )
        )


    # ========================================================
    # WEATHER CARD
    # ========================================================

    with col3:

        st.html(
            html(
                """
                <div class="feature-card">

                    <div class="feature-icon">
                        🌤️
                    </div>

                    <div class="feature-title">
                        Live Weather
                    </div>

                    <div class="feature-description">
                        Check current weather
                        information before
                        planning your journey.
                    </div>

                </div>
                """
            )
        )


    st.html("<br>")


    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    action1, action2, action3, action4 = st.columns(4)


    # ========================================================
    # CHAT BUTTON
    # ========================================================

    with action1:

        chat_clicked = st.button(
            "💬 Chat with AI"
        )

        if chat_clicked:

            st.session_state["active_section"] = "chat"

            st.session_state["show_planner"] = False

            st.rerun()


    # ========================================================
    # MY TRIPS BUTTON
    # ========================================================

    with action2:

        trips_clicked = st.button(
            "🧳 My Previous Trips"
        )

        if trips_clicked:

            st.session_state["active_section"] = "trips"

            st.session_state["show_planner"] = False

            st.rerun()


    # ========================================================
    # WEATHER BUTTON
    # ========================================================

    with action3:

        weather_clicked = st.button(
            "🌤️ Live Weather"
        )

        if weather_clicked:

            st.session_state["active_section"] = "weather"

            st.session_state["show_planner"] = False

            st.rerun()


    # ========================================================
    # PLAN TRIP BUTTON
    # ========================================================

    with action4:

        planner_clicked = st.button(
            "✨ Plan New Trip"
        )

        if planner_clicked:

            st.session_state["active_section"] = "planner"

            st.session_state["show_planner"] = True

            st.rerun()


    # ========================================================
    # CLOSE ACTIVE SECTION
    # ========================================================

    if st.session_state["active_section"] is not None:

        st.html("<br>")

        close_clicked = st.button(
            "✕ Close"
        )

        if close_clicked:

            st.session_state["active_section"] = None

            st.session_state["show_planner"] = False

            st.rerun()


    # ========================================================
    # ========================================================
    # CHAT SECTION
    # ========================================================
    # ========================================================

    if st.session_state["active_section"] == "chat":

        st.html(
            html(
                """
                <div class="section-title">
                    💬 AI Travel Chat
                </div>

                <div class="section-description">
                    Talk to your AI travel assistant and refine your journey.
                </div>
                """
            )
        )


        # ----------------------------------------------------
        # START CHAT SESSION
        # ----------------------------------------------------

        if st.session_state["chat_session_id"] is None:

            try:

                response = requests.post(
                    f"{API_URL}/chat/start",

                    headers={
                        "Authorization":
                        f"Bearer {st.session_state['token']}"
                    },

                    timeout=10
                )


                if response.status_code == 200:

                    data = response.json()

                    st.session_state["chat_session_id"] = (
                        data["session_id"]
                    )

                else:

                    st.error(
                        "Unable to start chat session."
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to backend. "
                    "Make sure FastAPI is running."
                )


            except Exception as e:

                st.error(
                    f"Could not start chat: {e}"
                )


        # ----------------------------------------------------
        # DISPLAY PREVIOUS MESSAGES
        # ----------------------------------------------------

        for message in st.session_state["chat_messages"]:

            with st.chat_message(message["role"]):

                st.write(
                    message["content"]
                )


        # ----------------------------------------------------
        # CHAT INPUT
        # ----------------------------------------------------

        user_message = st.chat_input(
            "Ask anything about your trip..."
        )


        if user_message:

            st.session_state["chat_messages"].append(
                {
                    "role": "user",
                    "content": user_message
                }
            )


            with st.chat_message("user"):

                st.write(
                    user_message
                )


            try:

                response = requests.post(
                    f"{API_URL}/chat/message",

                    headers={
                        "Authorization":
                        f"Bearer {st.session_state['token']}"
                    },

                    json={
                        "session_id":
                        st.session_state["chat_session_id"],

                        "message":
                        user_message
                    },

                    timeout=120
                )


                if response.status_code == 200:

                    data = response.json()

                    ai_response = data.get(
                        "response",
                        "Sorry, I could not generate a response."
                    )


                    st.session_state["chat_messages"].append(
                        {
                            "role": "assistant",
                            "content": ai_response
                        }
                    )


                    with st.chat_message("assistant"):

                        st.write(
                            ai_response
                        )


                else:

                    st.error(
                        f"Chat request failed: "
                        f"{response.text}"
                    )


            except requests.exceptions.Timeout:

                st.error(
                    "The AI took too long to respond."
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend."
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


    # ========================================================
    # ========================================================
    # MY TRIPS SECTION
    # ========================================================
    # ========================================================

    if st.session_state["active_section"] == "trips":

        st.html(
            html(
                """
                <div class="section-title">
                    🧳 My Previous Trips
                </div>

                <div class="section-description">
                    View your previous adventures and saved itineraries.
                </div>
                """
            )
        )


        try:

            response = requests.get(
                f"{API_URL}/my-trips",

                headers={
                    "Authorization":
                    f"Bearer {st.session_state['token']}"
                },

                timeout=10
            )


            if response.status_code == 200:

                trips = response.json()


                if not trips:

                    st.info(
                        "You haven't planned any trips yet."
                    )


                else:

                    for trip in trips:

                        # ------------------------------------
                        # TRIP INFORMATION
                        # ------------------------------------

                        st.html(
                            html(
                                f"""
                                <div class="trip-card">

                                    <h2>
                                        🌍
                                        {trip.get(
                                            "destination",
                                            "Unknown"
                                        )}
                                    </h2>

                                    <p>
                                        📅
                                        {trip.get(
                                            "days",
                                            0
                                        )} days
                                    </p>

                                    <p>
                                        💰
                                        Budget:
                                        ₹{trip.get(
                                            "budget",
                                            0
                                        )}
                                    </p>

                                    <p>
                                        ❤️
                                        Interests:
                                        {trip.get(
                                            "interests",
                                            ""
                                        )}
                                    </p>

                                </div>
                                """
                            )
                        )


                        # ------------------------------------
                        # SAVED ITINERARY
                        # ------------------------------------

                        trip_plan_string = trip.get(
                            "trip_plan",
                            ""
                        )


                        if trip_plan_string:

                            try:

                                saved_plan = json.loads(
                                    trip_plan_string
                                )


                                # --------------------------------
                                # SUMMARY
                                # --------------------------------

                                summary = saved_plan.get(
                                    "summary",
                                    ""
                                )


                                if summary:

                                    st.html(
                                        html(
                                            f"""
                                            <div class="trip-card">

                                                <h3>
                                                    🗺️ Trip Summary
                                                </h3>

                                                <p>
                                                    {summary}
                                                </p>

                                            </div>
                                            """
                                        )
                                    )


                                # --------------------------------
                                # DAYS
                                # --------------------------------

                                saved_days = saved_plan.get(
                                    "days",
                                    []
                                )


                                for day in saved_days:

                                    day_number = day.get(
                                        "day",
                                        ""
                                    )


                                    day_title = day.get(
                                        "title",
                                        ""
                                    )


                                    st.html(
                                        html(
                                            f"""
                                            <div class="trip-card">

                                                <h3>
                                                    📅 Day {day_number}
                                                    — {day_title}
                                                </h3>

                                            </div>
                                            """
                                        )
                                    )


                                    # ----------------------------
                                    # ACTIVITIES
                                    # ----------------------------

                                    activities = day.get(
                                        "activities",
                                        []
                                    )


                                    for activity in activities:

                                        time = activity.get(
                                            "time",
                                            ""
                                        )


                                        activity_name = activity.get(
                                            "activity",
                                            ""
                                        )


                                        description = activity.get(
                                            "description",
                                            ""
                                        )


                                        st.html(
                                            html(
                                                f"""
                                                <div style="
                                                    background:
                                                    rgba(0,0,0,0.45);

                                                    padding:15px;

                                                    margin:8px 0;

                                                    border-radius:12px;

                                                    color:white;
                                                ">

                                                    <b>
                                                        🕐 {time}
                                                    </b>

                                                    <br>

                                                    <b>
                                                        {activity_name}
                                                    </b>

                                                    <br>

                                                    <span style="
                                                        color:
                                                        rgba(
                                                            255,
                                                            255,
                                                            255,
                                                            0.75
                                                        );
                                                    ">
                                                        {description}
                                                    </span>

                                                </div>
                                                """
                                            )
                                        )


                            except json.JSONDecodeError:

                                st.warning(
                                    "Saved itinerary could not be displayed."
                                )


            else:

                st.error(
                    "Unable to fetch your trips."
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend. "
                "Make sure the backend is running."
            )


        except requests.exceptions.Timeout:

            st.error(
                "Fetching trips took too long."
            )


        except Exception as e:

            st.error(
                f"Could not fetch your trips: {e}"
            )


        # ========================================================
    # ========================================================
    # LIVE WEATHER SECTION
    # ========================================================
    # ========================================================

    if st.session_state["active_section"] == "weather":

        st.html(
            html(
                """
                <div class="section-title">
                    🌦️ Live Weather
                </div>

                <div class="section-description">
                    Check the current weather information.
                </div>
                """
            )
        )


        # ----------------------------------------------------
        # STATE INPUT
        # ----------------------------------------------------

        destination = st.text_input(
            "Enter state",
            placeholder="Example: Goa, Punjab, Kerala..."
        )


        # ----------------------------------------------------
        # CHECK WEATHER BUTTON
        # ----------------------------------------------------

        check_weather_clicked = st.button(
            "🌤️ Check Weather"
        )


        # ----------------------------------------------------
        # FETCH WEATHER
        # ----------------------------------------------------

        if check_weather_clicked:

            if not destination.strip():

                st.warning(
                    "Please enter a state name."
                )


            else:

                try:

                    response = requests.get(
                        f"{API_URL}/test-weather",

                        params={
                            "destination": destination
                        },

                        timeout=10
                    )


                    # ------------------------------------------------
                    # SUCCESS
                    # ------------------------------------------------

                    if response.status_code == 200:

                        data = response.json()


                        # --------------------------------------------
                        # BACKEND RESPONSE:
                        #
                        # {
                        #     "destination": "goa",
                        #     "weather": {
                        #         "temperature": 28.7,
                        #         "humidity": 75,
                        #         "weather_code": 3,
                        #         "wind_speed": 9.7
                        #     }
                        # }
                        # --------------------------------------------

                        weather = data["weather"]


                        # --------------------------------------------
                        # SAVE WEATHER RESULT
                        # --------------------------------------------

                        st.session_state["weather_result"] = data


                        # --------------------------------------------
                        # DISPLAY WEATHER
                        # --------------------------------------------

                        st.success(
                            f"Current weather for "
                            f"{data['destination'].title()}"
                        )


                        col1, col2, col3, col4 = st.columns(4)


                        # --------------------------------------------
                        # TEMPERATURE
                        # --------------------------------------------

                        with col1:

                            st.metric(
                                "🌡️ Temperature",
                                f"{weather['temperature']} °C"
                            )


                        # --------------------------------------------
                        # HUMIDITY
                        # --------------------------------------------

                        with col2:

                            st.metric(
                                "💧 Humidity",
                                f"{weather['humidity']}%"
                            )


                        # --------------------------------------------
                        # WIND SPEED
                        # --------------------------------------------

                        with col3:

                            st.metric(
                                "💨 Wind Speed",
                                f"{weather['wind_speed']} km/h"
                            )


                        # --------------------------------------------
                        # WEATHER CODE
                        # --------------------------------------------

                        with col4:

                            st.metric(
                                "☁️ Weather Code",
                                weather["weather_code"]
                            )


                        # --------------------------------------------
                        # WEATHER CARD
                        # --------------------------------------------

                        st.html(
                            html(
                                f"""
                                <div class="weather-card">

                                    <h2>
                                        🌍
                                        {data["destination"].title()}
                                    </h2>

                                    <p>
                                        🌡️
                                        Temperature:
                                        <b>
                                            {weather["temperature"]} °C
                                        </b>
                                    </p>

                                    <p>
                                        💧
                                        Humidity:
                                        <b>
                                            {weather["humidity"]}%
                                        </b>
                                    </p>

                                    <p>
                                        💨
                                        Wind Speed:
                                        <b>
                                            {weather["wind_speed"]} km/h
                                        </b>
                                    </p>

                                    <p>
                                        ☁️
                                        Weather Code:
                                        <b>
                                            {weather["weather_code"]}
                                        </b>
                                    </p>

                                </div>
                                """
                            )
                        )


                    # ------------------------------------------------
                    # BACKEND ERROR
                    # ------------------------------------------------

                    else:

                        st.error(
                            f"Unable to fetch weather. "
                            f"Status code: {response.status_code}"
                        )


                        st.write(
                            "Backend response:",
                            response.text
                        )


                # ----------------------------------------------------
                # CONNECTION ERROR
                # ----------------------------------------------------

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI backend. "
                        "Make sure the backend is running."
                    )


                # ----------------------------------------------------
                # TIMEOUT
                # ----------------------------------------------------

                except requests.exceptions.Timeout:

                    st.error(
                        "Weather request took too long."
                    )


                # ----------------------------------------------------
                # OTHER ERROR
                # ----------------------------------------------------

                except Exception as e:

                    st.error(
                        f"Could not fetch weather: {e}"
                    )

    # ========================================================
    # ========================================================
    # PLAN NEW TRIP SECTION
    # ========================================================
    # ========================================================

    if st.session_state["active_section"] == "planner":

        st.html(
            html(
                """
                <div class="section-title">
                    ✨ Plan Your Next Adventure
                </div>

                <div class="section-description">
                    Let our AI create a personalized
                    travel experience for you.
                </div>
                """
            )
        )


        # ====================================================
        # TRIP PLANNER FORM
        # ====================================================

        with st.form("trip_planner_form"):

            # ------------------------------------------------
            # DESTINATION
            # ------------------------------------------------

            destination = st.text_input(
                "📍 Destination",
                placeholder="Example: Kerala"
            )


            # ------------------------------------------------
            # NUMBER OF DAYS
            # ------------------------------------------------

            days = st.number_input(
                "📅 Number of Days",

                min_value=1,

                max_value=30,

                value=3,

                step=1
            )


            # ------------------------------------------------
            # BUDGET
            # ------------------------------------------------

            budget = st.number_input(
                "💰 Budget (₹)",

                min_value=1000,

                max_value=1000000,

                value=10000,

                step=1000
            )


            # ------------------------------------------------
            # INTERESTS
            # ------------------------------------------------

            interests = st.multiselect(
                "❤️ Interests",

                [
                    "Nature",
                    "Adventure",
                    "Beaches",
                    "Food",
                    "Culture",
                    "History",
                    "Shopping",
                    "Relaxation"
                ]
            )


            # ------------------------------------------------
            # GENERATE BUTTON
            # ------------------------------------------------

            generate_clicked = st.form_submit_button(
                "🚀 Generate My Trip"
            )


        # ====================================================
        # GENERATE TRIP
        # ====================================================

        if generate_clicked:

            if not destination:

                st.warning(
                    "Please enter a destination."
                )


            elif not interests:

                st.warning(
                    "Please select at least one interest."
                )


            else:

                try:

                    response = requests.post(
                        f"{API_URL}/plan-trip",

                        headers={
                            "Authorization":
                            f"Bearer {st.session_state['token']}"
                        },

                        json={
                            "destination": destination,

                            "days": int(days),

                            "budget": int(budget),

                            "interests": interests
                        },

                        timeout=120
                    )


                    if response.status_code == 200:

                        result = response.json()


                        st.session_state[
                            "trip_result"
                        ] = result


                        st.success(
                            "🎉 Your AI trip has been created!"
                        )


                    else:

                        st.error(
                            f"Trip planning failed: "
                            f"{response.text}"
                        )


                except requests.exceptions.Timeout:

                    st.error(
                        "Trip planning took too long. "
                        "Please try again."
                    )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI backend."
                    )


                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


        # ====================================================
        # DISPLAY GENERATED TRIP
        # ====================================================

        if st.session_state["trip_result"]:

            result = st.session_state[
                "trip_result"
            ]


            st.html("<br>")


            st.html(
                html(
                    """
                    <div class="section-title">
                        🗺️ Your AI Generated Itinerary
                    </div>
                    """
                )
            )


            trip_plan = result.get(
                "trip_plan"
            )


            if trip_plan:

                destination_result = trip_plan.get(
                    "destination",
                    "Your Trip"
                )


                summary = trip_plan.get(
                    "summary",
                    ""
                )


                # --------------------------------------------
                # SUMMARY
                # --------------------------------------------

                st.html(
                    html(
                        f"""
                        <div class="trip-card">

                            <h2>
                                🌍 {destination_result}
                            </h2>

                            <p>
                                {summary}
                            </p>

                        </div>
                        """
                    )
                )


                # --------------------------------------------
                # DAYS
                # --------------------------------------------

                days_data = trip_plan.get(
                    "days",
                    []
                )


                for day in days_data:

                    day_number = day.get(
                        "day",
                        ""
                    )


                    day_title = day.get(
                        "title",
                        ""
                    )


                    st.html(
                        html(
                            f"""
                            <div class="trip-card">

                                <h3>
                                    📅 Day {day_number}
                                    — {day_title}
                                </h3>

                            </div>
                            """
                        )
                    )


                    # ----------------------------------------
                    # ACTIVITIES
                    # ----------------------------------------

                    activities = day.get(
                        "activities",
                        []
                    )


                    for activity in activities:

                        time = activity.get(
                            "time",
                            ""
                        )


                        activity_name = activity.get(
                            "activity",
                            ""
                        )


                        description = activity.get(
                            "description",
                            ""
                        )


                        st.html(
                            html(
                                f"""
                                <div style="
                                    background:
                                    rgba(0,0,0,0.45);

                                    padding:15px;

                                    margin:8px 0;

                                    border-radius:12px;

                                    color:white;
                                ">

                                    <b>
                                        🕐 {time}
                                    </b>

                                    <br>

                                    <b>
                                        {activity_name}
                                    </b>

                                    <br>

                                    <span style="
                                        color:
                                        rgba(
                                            255,
                                            255,
                                            255,
                                            0.75
                                        );
                                    ">
                                        {description}
                                    </span>

                                </div>
                                """
                            )
                        )


    # ========================================================
    # ========================================================
    # LOGOUT
    # ========================================================
    # ========================================================

    st.html("<br><br>")


    logout_clicked = st.button(
        "🚪 Logout"
    )


    if logout_clicked:

        st.session_state["token"] = None

        st.session_state["username"] = None

        st.session_state["trip_result"] = None

        st.session_state["weather_result"] = None

        st.session_state["show_planner"] = False

        st.session_state["active_section"] = None

        st.session_state["chat_session_id"] = None

        st.session_state["chat_messages"] = []

        st.rerun()