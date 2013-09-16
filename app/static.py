import os

from settings import IMG_PATH

styles = {
    1 :"* { background-color: #DEDFEF; color: #5A6984 }",
    2 :"* { background-color: #D6E1EF; color: #296DFF }",
    3 :"* { background-color: #D6D8F3; color: #1804CE }",
    4 :"* { background-color: #D8CCED; color: #562AA1 }",
    5 :"* { background-color: #EFDFE7; color: #885163 }",
    6 :"* { background-color: #F3D7D6; color: #CE0214 }",
    7 :"* { background-color: #5A6784; color: #CED3E7 }",
    8 :"* { background-color: #2D67F3; color: #C6DBFF }",
    9 :"* { background-color: #1800CA; color: #C6C3F7 }",
    10:"* { background-color: #5626A1; color: #E7D7F7 }",
    11:"* { background-color: #845163; color: #E7D3DE }",
    12:"* { background-color: #C60008; color: #F7C3C6 }",
    13:"* { background-color: #F3E3D6; color: #EB7521 }",
    14:"* { background-color: #EFD3AD; color: #AD6D10 }",
    15:"* { background-color: #EFE3B5; color: #A58A10 }",
    16:"* { background-color: #F7F3CE; color: #636131 }",
    17:"* { background-color: #EDF3E3; color: #639A31 }",
    18:"* { background-color: #E7EBE7; color: #006531 }",
    19:"* { background-color: #EB6F14; color: #FFEFDE }",
    20:"* { background-color: #B56D10; color: #F7DBB5 }",
    21:"* { background-color: #AB8C10; color: #EFE7B5 }",
    22:"* { background-color: #616331; color: #FFFFD6 }",
    23:"* { background-color: #639A31; color: #F7FFEF }",
    24:"* { background-color: #006531; color: #EFF3EF }"
}

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
    "new"        : os.path.join(IMG_PATH, "document_new.png"),
    "inbox"      : os.path.join(IMG_PATH, "inbox.png"),
    "calendar"   : os.path.join(IMG_PATH, "office_calendar.png"),
    "next"       : os.path.join(IMG_PATH, "next_actions.png"),
    "projects"   : os.path.join(IMG_PATH, "projects.png"),
    "contexts"   : os.path.join(IMG_PATH, "contexts.png"),
    "completed"  : os.path.join(IMG_PATH, "complete.png"),
    "sync"       : os.path.join(IMG_PATH, "shuffle_icon.png"),
    "main"       : os.path.join(IMG_PATH, "shuffle_icon.png"),
}
