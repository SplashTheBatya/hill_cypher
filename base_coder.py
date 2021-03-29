# Набор функций для кодировки по словарю

def coder(phrase_list: list, lang_crypt_dict: dict):
    coded_list = []
    for char in phrase_list:
        for key, item in lang_crypt_dict.items():
            if item == char:
                coded_list.append(key)
    return coded_list


def decoder(phrase_list: list, lang_crypt_dict: dict):
    decoded_list = []
    for char in phrase_list:
        for key, item in lang_crypt_dict.items():
            if key == char:
                decoded_list.append(item)
    return decoded_list
