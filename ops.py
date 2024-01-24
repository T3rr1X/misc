import random as rd
from itertools import combinations
import streamlit as st

LETTERS = list('abcdefghijklmnopqrstuvwxyz')
LETTERS_ = LETTERS * 100


####-------------------------------------------------####
#  CRITTO                                               #
####-------------------------------------------------####

def generate_key(key: str):
    multiplier = 1
    if key.isupper():
        key = key.lower()
    elif key.isnumeric():
        key = LETTERS[int(key)]
        st.write(key)
    elif '*' in key:
        key2 = key
        key = key2.replace(' ', '').split('*')[0]
        multiplier = int(key2.replace(' ', '').split('*')[1])
    if False in [True if k in LETTERS else False for k in key]:
        raise ValueError('one or more charachter in key is not parsable')
    return [LETTERS.index(k) * multiplier for k in key]


def derivate_key(str1: str, str2: str):
    numbers1 = generate_key(str1)
    numbers2 = generate_key(str2)
    st.write(numbers1, numbers2)
    differncies = [abs(d1 - d2) for d1, d2 in zip(numbers1, numbers2)]
    for d in differncies:
        if d < 0:
            raise ValueError("Perhaps you're trying to convert in the inverse order")
    return "".join([LETTERS[d] for d in differncies])


def extend_key(string, key):
    press = key * (len(string) // len(key))
    remained = len(string) - len(key)
    for i in range(remained):
        press.append(key[i])
    return press


def _add(c: str, k: int):
    place = LETTERS.index(c)
    return LETTERS_[place + k]


def _sub(c: str, k: int):
    place = LETTERS.index(c)
    return LETTERS_[place - k]


def obtain_spaces(string: str):
    indecies = []
    for i, s in enumerate(string):
        if s == ' ':
            indecies.append(i)
    return indecies


def re_add_spaces(string: list, spaces_ind: list):
    string2 = []
    plus = 0
    for i, s in enumerate(string):
        if (i + plus) not in spaces_ind:
            string2.append(s)
        else:
            string2.append(' ')
            string2.append(s)
            plus += 1
    return string2


def decrypt(string, key_, skip_spaces=True):
    if string.isupper():
        string = string.lower()
    if skip_spaces:
        spaces_index = obtain_spaces(string=string)
    string = string.replace(' ', '')
    key = generate_key(key_)
    key = extend_key(string, key * (len(string) // len(key)))
    dec_string = []
    for s, k in zip(string, key):
        dec_string.append(_sub(s, k))

    if skip_spaces:
        dec_string = re_add_spaces(dec_string, spaces_index)
    return "".join(dec_string)


def crypt(string, key_, skip_spaces=True):
    if string.isupper():
        string = string.lower()
    if skip_spaces:
        spaces_index = obtain_spaces(string=string)
    string = string.replace(' ', '')
    key = generate_key(key_)
    key = extend_key(string, key * (len(string) // len(key)))
    dec_string = []
    for s, k in zip(string, key):
        dec_string.append(_add(s, k))

    if skip_spaces:
        dec_string = re_add_spaces(dec_string, spaces_index)
    return "".join(dec_string)


####-------------------------------------------------####
#  CORRIERE                                             #
####-------------------------------------------------####

def factorial(n):
    f = 1
    for i in range(n):
        f *= n - i
    return f


def n_on_k(n, k) -> int:
    onner = factorial(n)
    downer = factorial(k) * factorial(n - k)
    return int(onner / downer)


def get_total_weight(l, index=2):
    s = 0
    for l in l:
        s += l[index]
    return s


def maximize(packs: tuple, post=4, portata=245):
    # for i in range(n_on_k(len(packs), post)):
    combs = combinations(packs, post)
    combs = tuple(combs)
    # print(len(comb))
    values = {}
    for comb in combs:
        peso = get_total_weight(comb)
        if peso <= portata:
            values[tuple([c[0] for c in comb])] = get_total_weight(comb, index=1)

    massimo = max(values, key=lambda x: values[x])
    return massimo, values[massimo]


def create_bituple_fromlist(l: list, prefix):
    if len(l) % 2 != 0:
        raise Exception('List length must be pair')
    t = []
    for i in range(0, len(l), 2):
        t.append((prefix + str(i // 2 + 1), l[i], l[i + 1]))
    return t


def corrier_to_streamlit():
    st.subheader('Corriere')
    text = st.text_input('Inserisci come  200 12 100 20...')
    portata = st.text_input('Inserisci Portata Massima')
    posti = st.text_input('Inserisci il numero di pacchi per slot')
    prefisso = st.text_input('Inserisci il prefisso M, P...')
    if prefisso == '':
        prefisso = 'M'
    if len(portata) > 0:
        portata = int(portata)
    if len(text) > 2:
        IN = text.replace(', ', ',').replace(',', ' ').split()
        IN = [int(n) for n in IN]
        packs = tuple(create_bituple_fromlist(IN, prefisso))
        res = maximize(packs, portata=portata, post=3)
        st.subheader(f"Il valore massimo ottenibile è :blue[{res[1]}] ottenuto con :red[{res[0]}]")


def crittografia_to_streamlit():
    choic = ['Cripta', 'Decripta', 'Deriva Chiave']
    choi = st.selectbox('Seleziona il tipo', choic)
    if choi == 'Cripta':
        testo = st.text_input('Inserisci il testo da criptare')
        chiave = st.text_input('Inserisci la chiave (una frase di lunghezza n > 0 o un numero intero)')
        if len(testo) > 0 and len(chiave) > 0:
            crypted = crypt(testo, key_=chiave, skip_spaces=True)
            st.subheader(f"Il testo Criptato è :blue[{crypted}]")
    elif choi == 'Decripta':
        testo = st.text_input('Inserisci il testo da decriptare')
        chiave = st.text_input('Inserisci la chiave (una frase di lunghezza n > 0 o un numero intero)')
        if len(testo) > 0 and len(chiave) > 0:
            crypted = decrypt(testo, key_=chiave, skip_spaces=True)
            st.subheader(f"Il testo Decriptato è :blue[{crypted}]")

    elif choi == 'Deriva Chiave':
        testo1 = st.text_input('Inserisci il testo A')
        testo2 = st.text_input('Inserisci il testo B')
        st.write("ATTENZIONE, l'ordine dei testi è importante")
        if len(testo1) > 0 and len(testo2) > 0:
            crypted = derivate_key(testo1, testo2)
            st.subheader(f"Il testo Decriptato è :blue[{crypted}]")




if __name__ == '__main__':
    # print(decrypt('SFQVCCMJDB EFNPDSBUJDB', 'b'))
    packs = (
        ('P1', 150, 450),
        ('P2', 115, 205),
        ('P3', 60, 160),
        ('P4', 140, 380),
        ('P5', 70, 125),
        ('P6', 150, 200)
    )
    print(maximize(packs=packs, portata=600, post=3))

    problems = ['Crittografia', 'Corriere']
    select = st.selectbox('Scegli il problema da risolvere', problems)
    if select == 'Corriere':
        corrier_to_streamlit()
    elif select == 'Crittografia':
        crittografia_to_streamlit()
