import streamlit as st
import requests
import streamlit.components.v1 as components

st.title("📍 GPS Attendance Agent")

# --- Placeholder for coordinates ---
if "coords" not in st.session_state:
    st.session_state.coords = None

# --- Inject JavaScript to capture GPS ---
get_location = """
<script>
function sendCoords() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const coords = pos.coords.latitude + "," + pos.coords.longitude;
            const queryString = "?coords=" + coords;
            window.location.href = window.location.pathname + queryString;
        },
        (err) => {
            const queryString = "?coords=error";
            window.location.href = window.location.pathname + queryString;
        }
    );
}
sendCoords();
</script>
"""
components.html(get_location, height=0)

# --- Retrieve coordinates from query params ---
coords = st.experimental_get_query_params().get("coords", [None])[0]
if coords and coords != "error":
    st.session_state.coords = coords

# --- Show coordinates or waiting text ---
if st.session_state.coords:
    st.success(f"Location detected: {st.session_state.coords}")
else:
    st.warning("Waiting for location... Please allow GPS access.")

# --- Student input ---
student = st.text_input("Enter your name:")

# --- Mark Attendance ---
if st.button("Mark Attendance", key="mark_attendance"):
    if st.session_state.coords and st.session_state.coords != "error":
        try:
            lat, lon = map(float, st.session_state.coords.split(","))
            response = requests.post(
                "http://127.0.0.1:8000/mark_attendance/",
                json={"student": student, "latitude": lat, "longitude": lon},
            )
            st.write(response.json())
        except Exception as e:
            st.error(f"Failed to submit attendance: {e}")
    else:
        st.warning("Location not available. Please allow GPS access.")
