import math
import os

ELSA_MAX_CHARACTER = 128
WORD_PER_SET = 30


def get_paragraph_by_list_format():
    with open("input_text/single_script.txt",'r') as f:
        list_sentences = replace_special_character_with_dot(remove_special_character("".join(add_dot_at_the_end_of_sentence(f.readlines())))).split(".")
    clean_list_sentences = []
    for sentence in list_sentences:
        if len(sentence) > ELSA_MAX_CHARACTER:
            clean_list_sentences += split_long_string(sentence)
        else:
            pass 
            clean_list_sentences += [sentence]
    return [sentence.strip() for sentence in clean_list_sentences]

def split_long_string(long_string):
    anchor_str = [", and",", they",", a ",", begins",", with","— ",", but",", then",": ",", or",", new",", including",", "]
    for a in anchor_str[::-1]:
        if a in long_string:
            return [long_string.split(a,1)[0],a[2:] + long_string.split(a,1)[1]]
    return [long_string]

def add_dot_at_the_end_of_sentence(list_sentences:list):
    clean_list_sentences = []
    for sentence in list_sentences:
        if "!\n" in sentence:
            sentence = sentence.replace("!\n",".\n")
        elif "?\n" in sentence:
            sentence = sentence.replace("?\n",".\n")
        elif ".\n" not in sentence:
            sentence = sentence.replace("\n",".\n")
        clean_list_sentences += [sentence]
    return clean_list_sentences

def remove_special_character(full_script:str):
    list_special_characters = ["\"","@","—"]
    for c in list_special_characters:
        full_script = full_script.replace(c,"")
    return full_script

def replace_special_character_with_dot(full_script):
    list_special_characters = ["!"]
    for c in list_special_characters:
        full_script = full_script.replace(c,".")
    return full_script

# print("\n".join(get_paragraph_by_list_format()))
# for idx,s in enumerate(get_paragraph_by_list_format()):
#     # if len(s) > 128:
#         print(f"{idx} {len(s)} {s}")

def split_word_set():
    remove_old_files()
    with open("input_text/phrases_list.txt",'r') as f:
        list_word = [phrase.replace("\n","") for phrase in f.readlines()]
    number_of_study_set = math.ceil(len(list_word)/WORD_PER_SET)
    for index_file in range(number_of_study_set):
        for phrase_index in range(WORD_PER_SET*index_file,WORD_PER_SET*(index_file+1)):
            with open(f"input_text/splited_study_set/set_number_{index_file}",'a') as f:
                try:
                    f.writelines(f"{list_word[phrase_index]}\n")                
                except: pass

def remove_old_files(file_name_pattern = "set_number_*",path_to_dir="input_text/splited_study_set"):
    os.system("rm -rf input_text/splited_study_set")
    os.mkdir("input_text/splited_study_set")
