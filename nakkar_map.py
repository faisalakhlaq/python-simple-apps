import folium
import pandas


data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


def marker_colour(elevation):
    e = float(elevation)
    if e < 1000:
        return "blue"
    elif 1000 <= e < 2000:
        return "green"
    elif 2000 >= e < 3000:
        return "orange"
    else:
        return "red"

map = folium.Map(location=[38.58, -99.09], zoom_start=2)
# Nakkar_map below
# map = folium.Map(location=[33.724674, 73.693096], zoom_start=10)
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    colour = marker_colour(el)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=5, color=colour,
                                     popup=folium.Popup(str(el), parse_html=True),
                                     fill_color=colour, fill=True, fill_opacity=1))
# for lt, ln, el in zip(lat, lon, elev):
#     fg.add_child(folium.CircleMarker(location=[lt, ln], radius=500, fill=True,
#                                popup=folium.Popup(str(el), parse_html=True),
#                                icon=folium.Icon(color=marker_colour(el))))
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor':'green'
                            if x['properties']['POP2005'] < 10000000
                                                      else 'orange' if 10000000 <= x['properties']['POP2005']  < 20000000
                                                      else 'red'}))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())

map.save("Nakkar_Map.html")
