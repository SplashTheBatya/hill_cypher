import itertools
from matrix_scaling import *
from base_coder import *

a = ord('а')
rus_char = ''.join([chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)])
special_char = {33: '.', 34: ',', 35: ' ', 36: '?'}

russian_alph_dict = dict(list(enumerate(rus_char)))
russian_alph_dict.update(special_char)


# Рекурсивный расширенный алгоритм Евклида
def gcd_extended(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return div, y - (num2 // num1) * x, x


# Функция шифровки
def hill_cipher(phrase: str, lang_crypt_dict: dict, key_word: str):
    """

    :param phrase: Сообщение, которое нужно зашифровать
    :param lang_crypt_dict: Словарь языка шифруемого сообщения
    :param key_word: Ключевое слово, которое является ключом шифрования
    :return: Зашифрованное сообщение

    Получает необходимые параметры шифровки, раскладывает ключевое слово в матрицу по словарю языка кодировки,
    после чего разбивает сообщение на части равные размерности матрицы ключевого слова
    и по частям кодирует посредством матричного умножения
    """
    crypt_phrase = ''
    try:
        phrase_list = coder(list(phrase.lower()), lang_crypt_dict)
        key_word_list = coder(list(key_word.lower()), lang_crypt_dict)
    except ValueError as ex:
        raise ValueError('Несоответсвующий словарь')
    else:
        if np.sqrt(len(key_word_list)) != int(np.sqrt(len(key_word_list))):
            raise TypeError('Ключевое слово неподходящей длины: длина должна иметь целочисленный корень')
        else:
            arr = col = np.sqrt(len(key_word_list))
            key_matrix = np.array(key_word_list).reshape(int(arr), int(col))

        chunks = [phrase_list[x:x + key_matrix.shape[0]] for x in range(0, len(phrase_list), key_matrix.shape[0])]

        for item in chunks:
            while len(item) < key_matrix.shape[0]:
                item.append(35)

        multiplied_list = []

        for item in chunks:
            multiplied_list.append(np.dot(item, key_matrix))

        moduled_list = []

        for item in multiplied_list:
            moduled_list.append(np.mod(item, len(lang_crypt_dict)))

        decoded_cypher_list = []

        for item in moduled_list:
            decoded_cypher_list.append(decoder(item, lang_crypt_dict))

        crypt_phrase_list = list(itertools.chain.from_iterable(decoded_cypher_list))
        crypt_phrase = ''
        for item in crypt_phrase_list:
            crypt_phrase += item

    return crypt_phrase.upper()


# Функция дешифровки
def hill_decipher(crypted_phrase: str, lang_crypt_dict: dict, key_word: str):
    """

    :param crypted_phrase: Фраза для дешифровки
    :param lang_crypt_dict: Словарь языка на котором зашифрованно сообщение
    :param key_word: Ключевое слово по которому зашифрованно сообщение
    :return: Расшифрованное сообщение

    Получает необходимые для дешифровки данные.
    Затем строит обратную матрицу кодового слова по модулю словаря кодировки,
    после чего разбивает сообщение на соответсвующие размерности матрицы кодового слова части
    и расшифровывает их.
    """
    try:
        crypted_phrase_list = coder(list(crypted_phrase.lower()), lang_crypt_dict)
        key_word_list = coder(list(key_word.lower()), lang_crypt_dict)
    except ValueError as ex:
        raise ValueError('Несоответсвующий словарь')
    else:
        if np.sqrt(len(key_word_list)) != int(np.sqrt(len(key_word_list))):
            raise TypeError('Ключевое слово неподходящей длины: длина должна иметь целочисленный корень')
        else:
            arr = col = np.sqrt(len(key_word_list))
            key_matrix = np.array(key_word_list).reshape(int(arr), int(col))
        chunks = [crypted_phrase_list[x:x + key_matrix.shape[0]] for x in
                  range(0, len(crypted_phrase_list), key_matrix.shape[0])]

        matrix_det = np.around(np.linalg.det(key_matrix))
        euclid_algorithm_data = gcd_extended((int(np.around(matrix_det))), len(lang_crypt_dict))

        x = euclid_algorithm_data[1]

        # Вычисление обратной детерменанты по модулю
        reversed_det = 0
        if (matrix_det < 0) & (euclid_algorithm_data[1] > 0):
            reversed_det = x
        elif (matrix_det > 0) & (euclid_algorithm_data[1] < 0):
            reversed_det = x + len(lang_crypt_dict)
        elif (matrix_det > 0) & (euclid_algorithm_data[1] > 0):
            reversed_det = euclid_algorithm_data[1]
        elif (matrix_det < 0) & (euclid_algorithm_data[1] < 0):
            reversed_det = -euclid_algorithm_data[1]

        # Создание обратной матрицы по модулю
        alg_min_key_matrix = cofactor_matrix(key_matrix)
        absolute_alg_min_key_matrix = np.absolute(alg_min_key_matrix)
        sing_matrix = np.sign(alg_min_key_matrix)
        moduled_absolute_alg_min_key_matrix = np.mod(absolute_alg_min_key_matrix, len(lang_crypt_dict))
        moduled_alg_min_key_matrix = np.multiply(moduled_absolute_alg_min_key_matrix, sing_matrix)
        moduled_alg_min_key_matrix_on_determinant = np.multiply(moduled_alg_min_key_matrix, reversed_det)
        moduled_alg_min_key_matrix_on_determinant_abs = np.absolute(moduled_alg_min_key_matrix_on_determinant)
        moduled_alg_min_key_matrix_on_determinant_moduled = np.mod(moduled_alg_min_key_matrix_on_determinant_abs,
                                                                   len(lang_crypt_dict))
        moduled_alg_min_key_matrix_on_determinant_moduled = np.multiply(
            moduled_alg_min_key_matrix_on_determinant_moduled,
            sing_matrix)
        trasponeted_decode_matrix = np.matrix.transpose(moduled_alg_min_key_matrix_on_determinant_moduled)
        trasponeted_decode_matrix = np.where(trasponeted_decode_matrix < 0,
                                             trasponeted_decode_matrix + len(lang_crypt_dict),
                                             trasponeted_decode_matrix)

        # Применение матрицы дешифровки
        multiplied_list = []

        for item in chunks:
            multiplied_list.append(np.dot(item, trasponeted_decode_matrix))

        moduled_list = []

        for item in multiplied_list:
            moduled_list.append(np.mod(item, len(lang_crypt_dict)))

        decoded_cypher_list = []
        for item in moduled_list:
            decoded_cypher_list.append(decoder(item, lang_crypt_dict))

        decrypt_phrase_list = list(itertools.chain.from_iterable(decoded_cypher_list))
        decrypt_phrase = ''
        for item in decrypt_phrase_list:
            decrypt_phrase += item

    return decrypt_phrase.upper()


text = 'ЗАШИФРОВАННЫЙ ТЕКСТ ВСЕМ ОЧЕНЬ ИНТЕРЕСНО'
key_word = 'ТРАНСЦЕНДЕНТНЫЙЯ'
print(f'Исходное сообщение: {text}')
crypt_text = hill_cipher(text, russian_alph_dict, key_word)
print(f'Зашифрованное сообщение: {crypt_text}')
decrypt_text = hill_decipher(crypt_text, russian_alph_dict, key_word)
print(f'Расшифрованное сообщение: {decrypt_text}')
