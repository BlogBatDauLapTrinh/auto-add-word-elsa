import json

def get_position():
    pass

def dump_position_icons_to_file(position_dict,file_name="stored_position.json"):
    position_json = json.dumps(position_dict,indent=4)
    with open(file_name,'w') as f:
        f.writelines(position_json)

def get_all_icon_positions():
    with open('stored_position.json', 'r') as f:
        position_json = json.loads("".join(f.readlines()))
        # print(",".join([f"self.{position}"for position in position_json.keys()]))
        return position_json['plus_button_for_adding_study_set_x'],position_json['plus_button_for_adding_study_set_y'],position_json['study_set_name_input_x'],position_json['study_set_name_input_y'],position_json['category_dropdown_x'],position_json['category_dropdown_y'],position_json['ok_option_x'],position_json['ok_option_y'],position_json['blue_add_phrases_button_x'],position_json['blue_add_phrases_button_y'],position_json['search_bar_input_x'],position_json['search_bar_input_y'],position_json['plus_button_x'],position_json['plus_button_y'],position_json['finish_text_x'],position_json['finish_text_y'],position_json['central_add_phrases_button_x'],position_json['central_add_phrases_button_y']

def get_icon_position(icon_name):
    with open('stored_position.json', 'r') as f:
        position_json = json.loads("".join(f.readlines()))
    return position_json[f'{icon_name}_x'],position_json[f'{icon_name}_y']