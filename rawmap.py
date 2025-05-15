from polyline import decode
import folium
import requests
from folium.plugins import Fullscreen
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
inicio=[]
final=[]
distancias= defaultdict(list)
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
        fecha=stats[i]["start_date_local"]
        duracion=stats[i]["elapsed_time"]
        fechain=datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%SZ")
        dia=fecha[8:10]+fecha[4:8]+fecha[0:4]   
        #horain= datetime.strptime(fechain, "%H:%M:%S")
    # Add 30 seconds
        horafin = fechain + timedelta(seconds=duracion)
        
        # Format back to a string
        horafin = [horafin.strftime("%w"),horafin.strftime("%H:%M:%S")]
        horain=[fechain.strftime("%w"),fechain.strftime("%H:%M:%S")]

        inicio.append(horain)
        final.append(horafin)
        dia=datetime.strftime(fechain, "%j")  
        year=int(str(fechain)[0:4])
        distancias[str(year)].append([int(dia),distancia])
        if deporte in ["Walk","Hike"]:
            gradiente= 255-int(distancia*255/60)
            colores= f"rgb({gradiente}, 0, 0)"
        elif deporte== "Run":
            gradiente=255 - int(distancia*255/40)

            colores= f"rgb(0, {gradiente}, 0)"
        else:
            gradiente= 255-int(distancia*255/150)
            colores= f"rgb(0, 0, {gradiente})"
        try:
            vel=round(60/(stats[i]["average_speed"]*3.6),2)
            velm=int(vel)
            vels=int((vel-velm)*60)
        except ZeroDivisionError:
            vel="-"
        if poly != "":
            decoded_coordinates = decode(poly)
            listica= [list(coord) for coord in decoded_coordinates]
            folium.PolyLine(
            listica,
            color=colores,
            tooltip=f"Nombre: {nombre} \n , Distancia: {distancia} km \n , Velocidad = {velm}:{vels} min/km"
            ).add_to(l)
    
    Fullscreen(position="topright").add_to(l)
    map_title = "Tus rutas"
    title_html = f'<h1 style="position:absolute;z-index:100000;left:40vw" >{map_title}</h1>'
    l.get_root().html.add_child(folium.Element(title_html))
    legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 80px; 
     border: 0.0000001px solid grey; z-index: 9999; font-size: 14px;
     background-color: rgba(255, 255, 255, 0.05); padding: 10px;">
     &nbsp; Ciclismo &nbsp; <i class="fa fa-minus" style="color:blue"></i><br>
     &nbsp; Carrera &nbsp; <i class="fa fa-minus" style="color:green"></i><br>
     &nbsp; Otros &nbsp; <i class="fa fa-minus" style="color:red"></i><br>
</div>
'''
    l.get_root().html.add_child(folium.Element(legend_html))
    #l.save("./templates/stravastreamlit.html")
    temp_path = f"/tmp/stravastreamlit.html"
    l.save(temp_path)
    # def kmsacumulados(distancias):
    #     plt.style.use('seaborn')  # Better default style
    #     fig, ax = plt.subplots(figsize=(12, 4), dpi=120)  # Wider aspect ratio
   
    #     ax.set_xlim(0, 365)
    #     ax.set_xticks(np.arange(0, 366, 50))
    #     ax.xaxis.set_minor_locator(plt.MultipleLocator(25))
    #     plt.xticks(rotation=30, ha='right', fontsize=9)
    #     # Loop through each year in the dictionary
    #     for year, data in distancias.items():
    #         data = np.array(data)  # Convert to NumPy array
    #         days = np.flip(data[:, 0]) # Extract day numbers
    #         distances = np.flip(data[:, 1])  # Extract distances
    #         cumulative_km = np.cumsum(distances)  # Compute cumulative sum

    #         ax.plot(days, cumulative_km, 
    #             marker="o", 
    #             markersize=4,
    #             linewidth=1.5, 
    #             label=f"{year}")

    #     plt.subplots_adjust(bottom=0.15, left=0.08, right=0.95)
    
    #     # Improve labels and legend
    #     ax.set_xlabel("Día del año", fontsize=10, labelpad=8)
    #     ax.set_ylabel("Kms Acumulados", fontsize=10, labelpad=8)
    #     ax.set_title("Evolución de Kilometraje", fontsize=12, pad=15)
        
    #     # Configure grid and ticks
    #     ax.yaxis.set_major_locator(plt.MaxNLocator(8))
    #     ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)
        
    #     # Position legend outside
    #     ax.legend(fontsize=9, loc='upper left', bbox_to_anchor=(1, 1))
        
    #     plt.tight_layout()
    #     return fig
    # fig=kmsacumulados(distancias)

    #return fig






#actualizar("0c4943d0df64282d2eee68a5966e5f7fdf1e67d5")
