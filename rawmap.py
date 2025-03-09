from polyline import decode
import folium
import requests
def actualizar(refresh_token :str):
    try:
        # Actualizo el token
        response = requests.post(f"https://www.strava.com/oauth/token?client_id=143763&client_secret=9ddc6c13807019d306436f8f13972b2936a26e47&refresh_token={refresh_token}&grant_type=refresh_token")
        refresh= response.json()
        token=refresh["access_token"]
        print(token)
                        # Check if the request was successful
        response.raise_for_status()  # Raises an error for 4xx/5xx HTTP status codes
    except requests.exceptions.RequestException as e:
                print(f"Error: {e}")  # Print the error if there is an issue with the request 
    # Try making the GET request
    # The URL for the Strava API request
    url = f"https://www.strava.com/api/v3/athlete/activities?access_token={token}&per_page=200&page=1"
    try:
        # Send the request with the authorization header
        stats = requests.get(url).json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")  # Print the error if there is an issue with the request

    l= folium.Map(location=[42.794776, -1.659370], zoom_start=5)
    for i in range(len(stats)):
        poly = stats[i]["map"]["summary_polyline"]
        deporte=stats[i]["sport_type"]
        distancia= round(stats[i]["distance"]/1000,2)
        nombre=stats[i]["name"]
        if deporte == "Walk":
            gradiente= 255-int(distancia*255/40)
            colores= f"rgb({gradiente}, 0, 0)"
        elif deporte== "Run":
            gradiente=255 - int(distancia*255/20)

            colores= f"rgb(0, {gradiente}, 0)"
        else:
            gradiente= 255-int(distancia*255/150)
            colores= f"rgb(0, 0, {gradiente})"
        try:
            vel=round(60/(stats[i]["average_speed"]*3.6),2)
        except ZeroDivisionError:
            vel="-"
        if poly != "":
            decoded_coordinates = decode(poly)
            listica= [list(coord) for coord in decoded_coordinates]
            folium.PolyLine(
            listica,
            color=colores,
            tooltip=f"Nombre: {nombre} \n , Distancia: {distancia} km \n , Velocidad = {vel} min/km"
            ).add_to(l)
    
    
    map_title = "Las rutas"
    title_html = f'<h1 style="position:absolute;z-index:100000;left:40vw" >{map_title}</h1>'
    l.get_root().html.add_child(folium.Element(title_html))
    #l.save("./templates/stravastreamlit.html")
    temp_path = f"/tmp/stravastreamlit.html"
    l.save(temp_path)







#actualizar("0c4943d0df64282d2eee68a5966e5f7fdf1e67d5")
