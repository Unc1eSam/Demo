import folium
from folium.plugins import MousePosition
from folium.plugins import TagFilterButton
from folium.plugins import MeasureControl
import json
from folium.features import DivIcon
import branca
import csv

m = folium.Map(location=[45.035252, 38.974123], zoom_start=15,min_zoom=15)

ratings = set()

big_data = []
cols = ['name','rating','price','price_per_square_meter','infrastructure','count_infs','type_of_building','quadrature','tag','floor']

with open('correct_data1.json', encoding='cp1251') as f:
    data = json.load(f)
    for i in range(len(data['organic'])):
        tmp = []
        try:
            point = [data['organic'][i]['latitude'], data['organic'][i]['longitude']]
            name = data['organic'][i]['title']
            rating = data['organic'][i]['rating']
            ratings.add(str(rating))
            img = data['organic'][i]['image_url']
            price = data['organic'][i]['price']
            infrastructure = data['organic'][i]['infrastructure']
            count_infs = data['organic'][i]['count_infs']
            type_of_bilding = data['organic'][i]['types_building']
            quadrature = data['organic'][i]['quadrature']
            tag = data['organic'][i]['category'][0]['title']
            price_m = price/quadrature
            floor = data['organic'][i]['floor']
        except:
            print(i)
        iframe =f'<h3>{name}</h3><img src="{img}"><h5>Рейтинг:{rating}</h5><p><h5>Квадратура:{quadrature} м2</h5></p><p><h5>Тип деятелньости:{tag}</p></h5><p><h5>Цена:{price} рублей в месяц</h5></p><p><h5>Тип здания:{type_of_bilding}</h5></p><p><h5>Рядом со зданием:{",".join(str(x) for x in infrastructure)}</h5></p>'
        nframe = branca.element.IFrame(html=iframe, width=500, height=300)
        poup = folium.Popup(nframe, max_width=500)
        folium.Marker(point, popup=poup,
                      tooltip=f'{name}',tags=[str(rating)], icon=DivIcon(icon_size=(60,36),icon_anchor=(0,0),html=f"""<div style="font-size: 16pt; color: white"><g><svg><rect width="80" height="30" fill="blue" opacity=".9" rx="15"/><text x="10" y="20" font-family="Verdana" font-size="16" fill="white">{int(price/1000)}т.р</text></g></svg></div>""")).add_to(m)


formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(m)

TagFilterButton(sorted(list(ratings))).add_to(m)
m.add_child(MeasureControl())

m.save('map.html')



