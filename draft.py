from ppadb.client import Client
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import bs4


# with open('set_word/origin_word_list.txt','r') as f:
#     phrases_list = f.readlines()

# # with open('tienganhlachuyennho.txt','w') as f:
# #     f.writelines('')



# # for idx,phrase in enumerate(phrases_list):
# #     if idx%2==1:
# #         with open('tienganhlachuyennho.txt','a') as f:
# #             # phrases_list = f.readlines()
# #             f.writelines(phrase)

#         # print(phrase)

# for item in phrases_list:
#     if "?" in item and "?\n" not in item:
#         print(item)

MAX_PAGE = 50
def get_600_TOEIC_words():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    with open(f'transcript/600_TOEIC_words.txt','w') as f:
        f.writelines("")
    for index in range(MAX_PAGE):
        url = f"https://600tuvungtoeic.com/index.php?mod=lesson&id={index+1}"
        driver.get(url)
        detail_word_html = driver.page_source
        soup = bs4.BeautifulSoup(detail_word_html)
        for word in soup.find_all('div', class_="noidung"):
            en_word = word.find('span').get_text()
            with open(f'transcript/600_TOEIC_words.txt','a') as f:
                f.writelines(f"{en_word}\n")

def test_input_text():
    adb = Client()
    devices = adb.devices()
    if(len(devices) == 0):
        print('no device dettach')
    device = devices[0]


    phrase = "i'm very good today"
    print(phrase)
    device.shell(f'input text "{phrase}"')
