import streamlit as st
from rawmap import actualizar
import requests
import matplotlib.pyplot as plt
st.title("Mapitas")
st.subheader("Powered by :orange[Strava]")
url = "https://www.strava.com/oauth/authorize?client_id=143763&redirect_uri=https://mapitas.streamlit.app&response_type=code&scope=activity:read_all"
#st.write("Consigue los datos aqui: [link](%s)" % url)

    # Step 3: Retrieve the authorization code from the redirected URL
query_params = st.query_params  # Capture URL parameters
st.session_state["auth_code"] = query_params.get("code")

if "code" in query_params and st.session_state["auth_code"] is None:
        st.rerun()  # Force a rerun to capture query parameters

if "code" in query_params and st.session_state["auth_code"]:
        st.session_state["authenticated"] = True  # Mark user as authenticated
        st.write("✅ Ya estás registrado, ahora puedes ver tu mapa!")

else:
        st.write("🔗 Consigue los datos aqui: [link](%s)" % url)

if "code" in query_params and st.session_state["auth_code"]:
        st.session_state["authenticated"] = True  # Mark user as authenticated
        st.session_state["button"]=st.button("Pulsa para la magia")
        if st.session_state["button"]:  
                url_refresh=f"https://www.strava.com/oauth/token?client_id=143763&client_secret=9ddc6c13807019d306436f8f13972b2936a26e47&code={st.session_state["auth_code"]}&grant_type=authorization_code"
                try:     # Sending POST request with data as JSON
                        response = requests.post(url_refresh)
                        # Check if the request was successful
                        #response.raise_for_status()  # Raises an error for 4xx/5xx HTTP status codes
                        response=response.json()
                        nombre_atleta=response["athlete"]["firstname"]
                        id_atleta= response["athlete"]["id"]
                        refresh_token=response["refresh_token"]
                        fig=actualizar(refresh_token)
                        
                except Exception as e:
                        #st.error(f"An error occurred: {e}")
                        None
        st.session_state["graf"] = st.radio(" ",['Mapa', 'kms Acumulados']) 
        if st.session_state["graf"]=="Mapa" and st.session_state["button"]:            
                try:
                        path_to_html = "./templates/stravastreamlit.html"

                        # Read file and keep in variable
                        temp_path = f"/tmp/stravastreamlit.html"
                        with open(temp_path,'r') as f: 
                                html_data = f.read()

                        ## Show in webpage
                        st.components.v1.html(html_data,height=500)
                except Exception:
                        None
        if st.session_state["graf"]=="kms Acumulados" and st.session_state["button"]: 
                if fig:
                        st.pyplot(fig)  # Use st.plotly_chart(fig) if it's Plotly
                else:
                        st.warning("No figure available to display.")
