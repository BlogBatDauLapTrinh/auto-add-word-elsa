from time import sleep
from helper_class.adb_helper import ADBHelper
import helper_class.json_file_helper as json_helper
import helper_class.paragraph_helper as paragraph_helper

class AutoAddStudySetELSA():

    def __init__(self):
        self.adb_helper = ADBHelper()
        self.plus_button_for_adding_study_set_x, self.plus_button_for_adding_study_set_y, self.study_set_name_input_x, self.study_set_name_input_y, self.category_dropdown_x, self.category_dropdown_y, self.ok_option_x, self.ok_option_y, self.blue_add_phrases_button_x, self.blue_add_phrases_button_y, self.search_bar_input_x, self.search_bar_input_y, self.plus_button_x, self.plus_button_y, self.finish_text_x, self.finish_text_y, self.central_add_phrases_button_x, self.central_add_phrases_button_y = json_helper.get_all_icon_positions()

    def add_complete_script_to_ELSA(self,set_name=None):
        if set_name == None: set_name = paragraph_helper.get_paragraph_by_list_format()[0]
        list_sentences =  paragraph_helper.get_paragraph_by_list_format()[1:]
        self.adb_helper.click_at_point(
            self.plus_button_for_adding_study_set_x, self.plus_button_for_adding_study_set_y)
        self.wait_for_loading_screen()
        self.adb_helper.click_at_point(
            self.study_set_name_input_x, self.study_set_name_input_y)
        self.adb_helper.input_text(set_name)
        self.adb_helper.click_enter_keyboard()
        self.adb_helper.click_at_point(
            self.category_dropdown_x, self.category_dropdown_y)
        self.adb_helper.click_at_point(self.ok_option_x, self.ok_option_y)
        for sentence in list_sentences:
            print(sentence)
            self.adb_helper.click_at_point(
                self.blue_add_phrases_button_x, self.blue_add_phrases_button_y)
            self.adb_helper.click_at_point(
                self.search_bar_input_x, self.search_bar_input_y)
            self.adb_helper.input_text(sentence)
            self.adb_helper.click_enter_keyboard()
            self.wait_for_loading_screen()
            self.adb_helper.click_at_point(
                self.plus_button_x, self.plus_button_y)
        # self.adb_helper.navigate_backward()
        self.adb_helper.click_at_point(self.finish_text_x, self.finish_text_y)
        self.wait_for_loading_screen()

    def add_multiple_study_sets_for_file():
        pass

    def wait_for_loading_screen(self):
        while self.adb_helper.is_showing_dialog():
            sleep(0.1)


autoAddELSA = AutoAddStudySetELSA()
autoAddELSA.add_complete_script_to_ELSA()