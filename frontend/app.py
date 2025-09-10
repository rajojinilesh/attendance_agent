import streamlit as st
import requests

st.title("📍 GPS Attendance Agent")

# --- Inject JavaScript to capture GPS ---
get_location = """
<script>
navigator.geolocation.getCurrentPosition(
    (pos) => {
        const coords = pos.coords.latitude + "," + pos.coords.longitude;
        window.parent.postMessage({coords: coords}, "*");
    },
    (err) => {
        window.parent.postMessage({coords: "error"}, "*");
    }
);
</script>
"""
st.components.v1.html(get_location, height=0)

# --- Placeholder for coordinates ---
coords = st.session_state.get("coords", None)

# --- Show waiting text ---
st.write("Waiting for location...")

# Dummy listener placeholder (not fully functional, but keeps your structure)
def js_listener():
    st.session_state.coords = st.experimental_get_query_params().get("coords", [None])[0]

# --- Student input ---
student = st.text_input("Enter your name:")

# --- Single button with unique key ---
if st.button("Mark Attendance", key="mark_attendance"):
    if coords and coords != "error":
        try:
            lat, lon = map(float, coords.split(","))
            response = requests.post(
                "http://127.0.0.1:8000/mark_attendance/",
                json={"student": student, "latitude": lat, "longitude": lon},
            )
            st.write(response.json())
        except Exception as e:
            st.error(f"Failed to submit attendance: {e}")
    else:
        st.warning("Location not available. Please allow GPS access.")
