import folium
import pandas

df = pandas.read_csv("Volcanoes.txt")
longitude = list(df["LON"])
latitude = list(df["LAT"])
elevation = list(df["ELEV"])
world_map = folium.Map(location=[35.20, -30.41], zoom_start=2.5, tiles="Stamen Terrain",
                       width='100%', height='85%')
feature_group_vol = folium.FeatureGroup(name="Volcanos")


def color_producer(el_):
    if el_ < 1000:
        return "green"
    elif 1000 <= el_ <= 3000:
        return "orange"
    else:
        return "red"


for lt, lo, el in zip(latitude, longitude, elevation):
    feature_group_vol.add_child(folium.CircleMarker(location=[lt, lo], radius=6,
                                                    popup=str(el)+"m",
                                                    # popup=folium.Popup(str(el)+"m", parse_html=True),
                                                    fill_color=color_producer(el), color='grey',
                                                    fill_opacity=0.7))

feature_group_boundary = folium.FeatureGroup(name="Country Boundaries")
feature_group_boundary.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
                                                style_function=lambda x: {'fillColor':'green'
                                                if x['properties']['POP2005'] < 10000000 else 'orange'
                                                if 10000000 < x['properties']['POP2005'] < 20000000 else
                                                'red'},
                                                tooltip=folium.features.GeoJsonTooltip(
                                                    fields=['NAME', 'POP2005'],
                                                    aliases=['Country: ','Population: '],),))

world_map.add_child(feature_group_boundary)
world_map.add_child(feature_group_vol)
world_map.add_child(folium.LayerControl())
world_map.save("world_map.html")
