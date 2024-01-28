KV = '''
Screen:
    MDNavigationLayout:
        ScreenManager:
            AppScreen:
                id: main_screen

                
        MDNavigationDrawer:
            id: location_selector
            anchor: "right"
            GridLayout:
                rows: 3
                size_hint_y: 1
                MDTextField:
                    id: search_field
                    hint_text: 'Search location'
                    on_text: app.update_location_suggestions()
        
                RecycleView:
                    id: suggestions
                    key_viewclass: 'viewclass'
                    key_size: 'height'
                    size_hint_y: 1 if search_field.text else 0
                    RecycleBoxLayout:
                        padding: dp(10)
                        default_size_hint: 1, None
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: 'vertical'
        
                RecycleView:
                    id: saved_locations
                    key_viewclass: 'viewclass'
                    key_size: 'height'
                    size_hint_y: 0 if search_field.text else 1
                    RecycleBoxLayout:
                        padding: dp(10)
                        default_size: None, dp(48)
                        default_size_hint: 1, None
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: 'vertical'     
                                
        LeftSettings:
            id: settings
            anchor: "left"

<LocationSelectorItem>:
    size_hint_y: None
    width: dp(20)

<NewLocation>:
    size_hint_y: None
    width: dp(20)    

<BottomBar>:
    MDTopAppBar:
        md_bg_bottom_color: 0, 0, 0, 0
        icon_color: 0, 0, 0, 1
        elevation: 0
        type: "bottom"
        mode: "end"
        icon: "map"
        on_action_button: app.open_location_selector()
        left_action_items: [["menu", lambda x: app.root.ids.settings.set_state("open")]]
        

<ForecastContainer>:
    orientation: 'vertical'
    height: self.minimum_height
    padding: dp(20), dp(10), dp(20), dp(100)

<ForecastSeparator>:
    size_hint_y: None
    height: self.minimum_height
    orientation: 'vertical'
    Widget:
        size_hint_y: None
        height: dp(20)
    MDSeparator:
    Widget:
        size_hint_y: None
        height: dp(20)

<Days5ForecastsWidget>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)
    size_hint_y: None
    height: dp(500)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.5
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20, 20, 20, 20]
    MDLabel:
        size_hint_y: 0.1
        text: 'Прогноз на 5 дней'
        font_name: 'MyFont'
        font_size: "20sp"
        

<Hours12ForecastsWidget>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)
    size_hint_y: None
    height: dp(500)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.5
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20, 20, 20, 20]
    MDLabel:
        size_hint_y: 0.1
        text: 'Прогноз на 12 часов'
        font_name: 'MyFont'
        font_size: "20sp"
        
    
    

<CurrentWeatherWidget>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(300)
    height: self.minimum_height
    spacing: dp(20)
    MDLabel:
        id: location_label
        padding: dp(20)
        
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_style: "H1"
        font_name: 'MyFont'
        font_size: '80sp'
        bold: True
        halign: "left"
        size_hint_y: None
        height: dp(100)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(100)
        spacing: "8dp"
        IconLeftWidget:
            icon_size: '100sp'
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1 
            allow_stretch: True
            keep_ratio: True
            id: weather_icon
        MDLabel:
            id: temperature
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            size_hint_y: None
            font_style: 'H3'
            font_size: '100sp'
    Widget:
        size_hint_y: None
        height: dp(10)
    MDLabel:
        id: weather_text
        padding: dp(20)
        font_name: 'MyFont'
        font_size: "30sp"
        halign: "left"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
    Widget:
        size_hint_y: None
        height: dp(10)
    GridLayout:
        padding: dp(20)
        spacing: dp(20)
        cols: 2
        rows: 2
        canvas.before:
            Color:
                rgba: 1, 1, 1, 0.4
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20, 20, 20, 20]
        size_hint: 1, None,
        height: self.minimum_height
        CurrentWeatherBottomElement:
            IconLeftWidget:
                icon_size: '70sp'
                allow_stretch: True
                keep_ratio: True
                icon: 'thermometer'
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                MDLabel:
                    text: 'Ощущается как:'
                    font_name: 'MyFont'
                    font_size: '20sp'
                MDLabel:
                    id: realfeel_temperature
                    font_name: 'MyFont'
                    font_size: '30sp'
        CurrentWeatherBottomElement:
            IconLeftWidget:
                icon_size: '70sp'
                allow_stretch: True
                keep_ratio: True
                icon: 'weather-windy'
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                MDLabel:
                    text: 'Ветер:'
                    font_name: 'MyFont'
                    font_size: '20sp'
                MDLabel:
                    id: wind
                    font_name: 'MyFont'
                    font_size: '30sp'
        CurrentWeatherBottomElement:
            IconLeftWidget:
                icon_size: '70sp'
                allow_stretch: True
                keep_ratio: True
                icon: 'water'
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                MDLabel:
                    text: 'Влажность:'
                    font_name: 'MyFont'
                    font_size: '20sp'
                MDLabel:
                    id: humidity
                    font_name: 'MyFont'
                    font_size: '30sp'
        CurrentWeatherBottomElement:
            IconLeftWidget:
                icon_size: '70sp'
                allow_stretch: True
                keep_ratio: True
                icon: 'balloon'
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                MDLabel:
                    text: 'Давление:'
                    font_name: 'MyFont'
                    font_size: '20sp'
                MDLabel:
                    id: pressure
                    font_name: 'MyFont'
                    font_size: '30sp'
                

<CurrentWeatherBottomElement@BoxLayout>:
    padding: dp(10)
    size_hint_y: None
    size_hint_x: 0.5
    height: dp(100)
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.4
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20, 20, 20, 20]
            
<CustomOneLineIconListItem>:
    IconLeftWidget:
        icon: root.icon
'''