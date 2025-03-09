import streamlit as st
from rawmap import actualizar
import requests
url = "https://www.strava.com/oauth/authorize?client_id=143763&redirect_uri=https://mapitas.streamlit.app&response_type=code&scope=activity:read_all"
st.write("check out this [link](%s)" % url)

    # Step 3: Retrieve the authorization code from the redirected URL
query_params = st.query_params  # Capture URL parameters
auth_code = query_params.get("code")

if "code" in query_params and auth_code is None:
        st.rerun()  # Force a rerun to capture query parameters

if auth_code:
        #st.success(f"Authorization Code: {auth_code}")
        codigo=1
else:
        st.warning("No authorization code found. Please authorize the app.")


button=st.button("Pulsa para la magia")
if button:
    url_refresh=f"https://www.strava.com/oauth/token?client_id=143763&client_secret=9ddc6c13807019d306436f8f13972b2936a26e47&code={auth_code}&grant_type=authorization_code"
    try:     # Sending POST request with data as JSON
            response = requests.post(url_refresh)
            # Check if the request was successful
            #response.raise_for_status()  # Raises an error for 4xx/5xx HTTP status codes
            response=response.json()
            nombre_atleta=response["athlete"]["firstname"]
            id_atleta= response["athlete"]["id"]
            refresh_token=response["refresh_token"]
            actualizar(refresh_token)
    except Exception as e:
            st.error(f"An error occurred: {e}")
try:
        path_to_html = "./templates/stravastreamlit.html"

        # Read file and keep in variable
        temp_path = "/tmp/stravastreamlit.html"
        with open(temp_path,'r') as f: 
                html_data = f.read()

        ## Show in webpage
        st.components.v1.html(html_data,height=500)
except Exception:
       None
