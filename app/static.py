import os

from settings import IMG_PATH

styles = {
    1 : {"background": "#DEDFEF", "text": "#5A6984"},
    2 : {"background": "#D6E1EF", "text": "#296DFF"},
    3 : {"background": "#D6D8F3", "text": "#1804CE"},
    4 : {"background": "#D8CCED", "text": "#562AA1"},
    5 : {"background": "#EFDFE7", "text": "#885163"},
    6 : {"background": "#F3D7D6", "text": "#CE0214"},
    7 : {"background": "#5A6784", "text": "#CED3E7"},
    8 : {"background": "#2D67F3", "text": "#C6DBFF"},
    9 : {"background": "#1800CA", "text": "#C6C3F7"},
    10: {"background": "#5626A1", "text": "#E7D7F7"},
    11: {"background": "#845163", "text": "#E7D3DE"},
    12: {"background": "#C60008", "text": "#F7C3C6"},
    13: {"background": "#F3E3D6", "text": "#EB7521"},
    14: {"background": "#EFD3AD", "text": "#AD6D10"},
    15: {"background": "#EFE3B5", "text": "#A58A10"},
    16: {"background": "#F7F3CE", "text": "#636131"},
    17: {"background": "#EDF3E3", "text": "#639A31"},
    18: {"background": "#E7EBE7", "text": "#006531"},
    19: {"background": "#EB6F14", "text": "#FFEFDE"},
    20: {"background": "#B56D10", "text": "#F7DBB5"},
    21: {"background": "#AB8C10", "text": "#EFE7B5"},
    22: {"background": "#616331", "text": "#FFFFD6"},
    23: {"background": "#639A31", "text": "#F7FFEF"},
    24: {"background": "#006531", "text": "#EFF3EF"},
}

def get_style(id):
    style = "* { background-color: %s; color: %s }" 
    return style % (styles[id]['background'], styles[id]['text'])

contexticons = {
    "accessories_calculator"   : os.path.join(IMG_PATH, "context/accessories_calculator.png"),
    "accessories_text_editor"  : os.path.join(IMG_PATH, "context/accessories_text_editor.png"),
    "applications_accessories" : os.path.join(IMG_PATH, "context/applications_accessories.png"),
    "applications_development" : os.path.join(IMG_PATH, "context/applications_development.png"),
    "applications_games"       : os.path.join(IMG_PATH, "context/applications_games.png"),
    "applications_graphics"    : os.path.join(IMG_PATH, "context/applications_graphics.png"),
    "applications_internet"    : os.path.join(IMG_PATH, "context/applications_internet.png"),
    "applications_office"      : os.path.join(IMG_PATH, "context/applications_office.png"),
    "applications_system"      : os.path.join(IMG_PATH, "context/applications_system.png"),
    "audio_x_generic"          : os.path.join(IMG_PATH, "context/audio_x_generic.png"),
    "camera_photo"             : os.path.join(IMG_PATH, "context/camera_photo.png"),
    "computer"                 : os.path.join(IMG_PATH, "context/computer.png"),
    "emblem_favorite"          : os.path.join(IMG_PATH, "context/emblem_favorite.png"),
    "emblem_important"         : os.path.join(IMG_PATH, "context/emblem_important.png"),
    "format_justify_fill"      : os.path.join(IMG_PATH, "context/format_justify_fill.png"),
    "go_home"                  : os.path.join(IMG_PATH, "context/go_home.png"),
    "network_wireless"         : os.path.join(IMG_PATH, "context/network_wireless.png"),
    "start_here"               : os.path.join(IMG_PATH, "context/start_here.png"),
    "system_file_manager"      : os.path.join(IMG_PATH, "context/system_file_manager.png"),
    "system_search"            : os.path.join(IMG_PATH, "context/system_search.png"),
    "system_users"             : os.path.join(IMG_PATH, "context/system_users.png"),
    "utilities_terminal"       : os.path.join(IMG_PATH, "context/utilities_terminal.png"),
    "video_x_generic"          : os.path.join(IMG_PATH, "context/video_x_generic.png"),
    "weather_showers_scattered": os.path.join(IMG_PATH, "context/weather_showers_scattered.png"),
    "x_office_address_book"    : os.path.join(IMG_PATH, "context/x_office_address_book.png")
}

icons = {
    "new"         : os.path.join(IMG_PATH, "document_new.png"),
    "inbox"       : os.path.join(IMG_PATH, "inbox.png"),
    "calendar"    : os.path.join(IMG_PATH, "office_calendar.png"),
    "next"        : os.path.join(IMG_PATH, "next_actions.png"),
    "projects"    : os.path.join(IMG_PATH, "projects.png"),
    "contexts"    : os.path.join(IMG_PATH, "contexts.png"),
    "completed"   : os.path.join(IMG_PATH, "complete.png"),
    "sync"        : os.path.join(IMG_PATH, "shuffle_icon.png"),
    "main"        : os.path.join(IMG_PATH, "shuffle_icon.png"),
    "syncfrom"    : os.path.join(IMG_PATH, "from.png"),
    "syncto"      : os.path.join(IMG_PATH, "to.png"),
    "syncconflict": os.path.join(IMG_PATH, "shuffle_icon.png"),
}
