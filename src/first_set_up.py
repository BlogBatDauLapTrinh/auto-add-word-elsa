from time import sleep
import helper_class.json_file_helper as json_file_helper
from core_class.icon_click_handler import IconClickHandler
from helper_class.adb_helper import ADBHelper
import os 

LIST_ICON_NAMES = 'plus_button_for_adding_study_set', 'study_set_name_input', 'category_dropdown', 'ok_option', 'blue_add_phrases_button', 'search_bar_input', 'plus_button', 'finish_text', 'central_add_phrases_button'


def locate_all_icon_positions():
    adb_helper = ADBHelper()
    icon_position_object = IconClickHandler()
    position_dict = dict()
    for icon_name in LIST_ICON_NAMES:
        icon_position_x,icon_position_y = icon_position_object.get_clicked_position(icon_name)
        position_dict[f'{icon_name}_x'],position_dict[f'{icon_name}_y'] = icon_position_x,icon_position_y
        adb_helper.click_at_point(icon_position_x,icon_position_y)
        if icon_name == 'study_set_name_input':
            adb_helper.input_text("TEST TO GET ICON POSITION")
            adb_helper.click_enter_keyboard()
        elif icon_name == 'search_bar_input':
            adb_helper.input_text("when you see this message from a study set, that means you locate all icon position precisely")
            adb_helper.click_enter_keyboard()
        while(icon_position_object.is_showing_dialog() and "category_dropdown" != icon_name):
            sleep(1)
        print(icon_name,(icon_position_x,icon_position_y))

    json_file_helper.dump_position_icons_to_file(position_dict)

os.system("touch input_text/single_script.txt")
# locate_all_icon_positions()