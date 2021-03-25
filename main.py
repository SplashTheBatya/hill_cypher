import numpy as np
import itertools


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


a = ord('а')
rus_char = ''.join([chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)])
special_char = {33: '.', 34: ',', 35: ' ', 36: '?'}

russian_alph_dict = dict(list(enumerate(rus_char)))
russian_alph_dict.update(special_char)

text = 'ЗАШИФРОВАННЫЙ ТЕКСТ'

text_list = list(text.lower())

coded_text = coder(text_list, russian_alph_dict)

key_word = 'АЛЬПИНИЗМ'

key_word_list = coder(list(key_word.lower()), russian_alph_dict)

key_matrix = np.array(key_word_list).reshape(3, 3)

chunks = [text_list[x:x+key_matrix.shape[0]] for x in range(0, len(text_list), key_matrix.shape[0])]

for item in chunks:
    while len(item) < key_matrix.shape[0]:
        item.append(' ')

for item in range(len(chunks)):
    chunks[item] = coder(chunks[item], russian_alph_dict)

# print(chunks)
# print(key_matrix)
multiplied_list = []

for item in chunks:
    multiplied_list.append(np.dot(item, key_matrix))

# print(multiplied_list)

moduled_list = []

for item in multiplied_list:
    moduled_list.append(np.mod(item, len(russian_alph_dict)))

print(moduled_list)

decoded_cypher_list = []

for item in moduled_list:
    decoded_cypher_list.append(decoder(item, russian_alph_dict))

print(decoded_cypher_list)

crypt_phrase_list = list(itertools.chain.from_iterable(decoded_cypher_list))
crypt_phrase = ''
for item in crypt_phrase_list:
    crypt_phrase += item

crypt_phrase = crypt_phrase.upper()
print(crypt_phrase)


