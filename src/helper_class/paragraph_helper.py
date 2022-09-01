ELSA_MAX_CHARACTER = 128


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
    anchor_str = [", and",", they",", I", ", a "," because", ", begins",", with","–",", but",", then",": ",", or",", new",", including",", "," ?"," and","?"," but"]
    for a in anchor_str[::-1]:
        if a in long_string:
            sub_string_1 = long_string.split(a,1)[0]
            sub_string_2 = a[2:] + long_string.split(a,1)[1]
            if len(long_string) > ELSA_MAX_CHARACTER:
                return split_long_string(sub_string_1)+split_long_string(sub_string_2)
    else: return [long_string]

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
    list_special_characters = ["\"","@","”","“"]
    for c in list_special_characters:
        full_script = full_script.replace(c,"")
    return full_script

def replace_special_character_with_dot(full_script):
    list_special_characters = ["!"]
    for c in list_special_characters:
        full_script = full_script.replace(c,".")
    return full_script

print("\n".join(get_paragraph_by_list_format()))
for idx,s in enumerate(get_paragraph_by_list_format()):
    if len(s) > 128:
        print(f"{idx} {len(s)} {s}")