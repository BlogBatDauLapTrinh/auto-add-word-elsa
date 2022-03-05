with open('tienganhlachuyennho.txt','r') as f:
    phrases_list = f.readlines()

with open('tienganhlachuyennho.txt','w') as f:
    f.writelines('')



for idx,phrase in enumerate(phrases_list):
    if idx%2==1:
        with open('tienganhlachuyennho.txt','a') as f:
            # phrases_list = f.readlines()
            f.writelines(phrase)

        # print(phrase)