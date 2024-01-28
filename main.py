# xnwKsTNEIU9ACggnpZQpyXzh2ZcCIS2k
# yOU3QMP9oKmbKdQlXMWG4ad0pFXlvqLn
# B80Dd87eFGyrS2IuCpyB81Fnx6I9DLLD
# T6rgXJAV7mNZBbdxGAcdZQCGWe3tyTXg

from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import Graph, LinePlot
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDBottomAppBar
import configparser
from api_requests.locations import location_suggestions
from api_requests import forecasts
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.core.window import Window
from kivy.lang import Builder
from main_kv import KV
from kivy.uix.scrollview import ScrollView
from api_requests.imgs import icon_mapping
phone_width = 700
phone_height = 1000

Window.size = (phone_width, phone_height)

config = configparser.ConfigParser()
config.read("config.ini")

background_src = None


class CurrentWeatherWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        current_conditions = forecasts.current_weather(config)
        self.ids.location_label.text = config.get('main_config', 'location_name')

        global background_src

        app = MDApp.get_running_app()

        if not current_conditions['IsDayTime']:
            background_src = 'src/background_night.png'
            app.theme_cls.theme_style = "Dark"
        elif current_conditions['WeatherIcon'] in [6, 7, 8, 11, 12, 13, 14, 15, 16,
                                                   17, 18, 19, 20, 22, 23, 24, 25, 26, 29, 32]:
            background_src = 'src/background_rainy.png'
            app.theme_cls.theme_style = "Dark"
        else:
            background_src = 'src/background_sunny.png'
            MDApp.get_running_app().theme_cls.theme_style = "Light"

        self.ids.weather_icon.icon = icon_mapping[current_conditions['WeatherIcon']]
        self.ids.temperature.text = current_conditions['Temperature'] + '°C'
        self.ids.weather_text.text = current_conditions['WeatherText']
        self.ids.realfeel_temperature.text = current_conditions['RealFeelTemperature'] + '°C'
        self.ids.wind.text = current_conditions['Wind'][0] + ', ' + current_conditions['Wind'][1]
        self.ids.humidity.text = current_conditions['RelativeHumidity'] + '%'
        self.ids.pressure.text = current_conditions['Pressure'] + ' мм'


class Days5ForecastsWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refresh_5days_forecast()

    def refresh_5days_forecast(self):
        self.data = []
        self.data = forecasts.day5_forecast(config)
        columns = [
            ('', dp(22)),
            ('', dp(10)),
            ('', dp(38)),
            ('Мин °C', dp(15)),
            ('Макс °C', dp(15)),
            ('Вероятность осадков', dp(21))
        ]
        rows = self.data
        self.add_widget(MDDataTable(
            column_data=columns,
            row_data=rows,
            use_pagination=True,
            background_color_cell=(1, 1, 1, 0.2),
            background_color=(1, 1, 1, 0.2),
            background_color_header=(1, 1, 1, 0.2)
        ))



class Hours12ForecastsWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refresh_12hour_forecast()

    def refresh_12hour_forecast(self):
        icons_layout = GridLayout(cols=12, size_hint=(1, 0.1))
        icons = ['weather-sunny']
        icons = icons * 12
        for icon in icons:
            icon_widget = OneLineIconListItem()
            icon_widget.add_widget(IconLeftWidget(icon=icon))
            icons_layout.add_widget(icon_widget)

        graph_layout = BoxLayout(size_hint=(1, 0.9))
        data_x = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        data_y = [12, 12, 13, 14, 15, 16, 13, 12, 12, 11, 10, 10, 8]

        graph = Graph(x_ticks_major=1, x_ticks_minor=2,
                      y_ticks_major=1,
                      xmin=min(data_x), xmax=max(data_x),
                      ymin=min(data_y) - 3, ymax=max(data_y) + 3,
                      background_color=(1, 1, 1, 1),
                      y_grid=True, x_grid=True,
                      tick_color=(0, 0, 0, 0.2)
                      )

        plot = LinePlot(color=[0, 0, 0, 0.7], line_width=2)
        plot.points = (tuple(zip(data_x, data_y)))
        graph.add_plot(plot)
        graph_layout.add_widget(graph)
        self.add_widget(graph_layout)


        self.add_widget(icons_layout)

class ForecastSeparator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ForecastContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(CurrentWeatherWidget())
        self.add_widget(ForecastSeparator())
        self.add_widget(Days5ForecastsWidget())
        self.add_widget(ForecastSeparator())
        self.add_widget(Hours12ForecastsWidget())


class BottomBar(MDBottomAppBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class LocationSelectorItem(MDFlatButton):
    def __init__(self, loc_name, **kwargs):
        super().__init__(**kwargs)
        self.width = dp(20)

        self.layout = BoxLayout()
        self.layout.add_widget(MDLabel(
                        text=loc_name,
                        pos_hint={"center_x": 0.5, "center_y": 0.1},
                        font_style="H2"))
        self.layout.width = self.width
        self.add_widget(self.layout)


class LocationSelector(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LeftSettings(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AppScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background = AsyncImage(allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        self.container = ScrollView(do_scroll_y=True,
                                    do_scroll_x=False,
                                    size_hint=(1, None),
                                    size=(Window.width, Window.height))
        self.container.add_widget(ForecastContainer(size_hint_y=None, height=self.container.height))

        global background_src
        self.background.source = background_src

        self.add_widget(self.container)
        self.add_widget(BottomBar())


class WeatherApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def open_location_selector(self):
        self.root.ids.location_selector.set_state("open")

    def update_location_suggestions(self):
        loc_name = self.root.ids.search_field.text
        location_key_dict = location_suggestions(loc_name, config)

        def add_location(loc_name):
            location_element = {
                "viewclass": "CustomOneLineIconListItem",
                "icon": 'map-marker',
                "text": loc_name,
                "on_press": lambda x=loc_name: refresh_forecasts_on_selected_loc(loc_name)
            }
            if not any(item["text"] == loc_name for item in self.root.ids.saved_locations.data):
                self.root.ids.saved_locations.data.append(location_element)
            refresh_forecasts_on_selected_loc(loc_name)
            self.root.ids.location_selector.set_state("close")

        def refresh_forecasts_on_selected_loc(loc_name):
            config.set('main_config', 'location_key', str(location_key_dict[loc_name]))
            config.set('main_config', 'location_name', loc_name)
            with open('config.ini', 'w') as config_file:
                config.write(config_file)

            config.read_file(open('config.ini'))

            self.root.ids.main_screen.container.clear_widgets()
            self.root.ids.main_screen.container.add_widget(
                ForecastContainer(size_hint_y=None,
                                  height=self.root.ids.main_screen.container.height)
            )
            global background_src
            self.root.ids.main_screen.background.source = background_src
            self.root.ids.search_field.text = ''

        def add_icon_item(loc_name):
            self.root.ids.suggestions.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": 'map-marker',
                    "text": loc_name,
                    "on_press": lambda x=loc_name: add_location(x)
                }
            )

        self.root.ids.suggestions.data = []
        if loc_name:
            for name in location_key_dict.keys():
                add_icon_item(name)


LabelBase.register(name='MyFont', fn_regular='src/ubuntu-medium.ttf')


WeatherApp().run()
