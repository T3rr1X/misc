import streamlit as st


def anagram_this(string_to_anagram, search_for):
    string_copy = list(string_to_anagram)
    wehave = {}
    for l in search_for:
        if l != ' ':
            wehave[l] = wehave.get(l, 0) + string_copy.count(l)

    return min(wehave.values())


def adjective(x):
    if x >= 0:
        return ''
    elif x >= 10:
        return 'solo'
    elif x >= 30:
        return 'adirittura'
    elif x >= 60:
        return 'ben'
    elif x >= 100:
        return 'BEN (cazzo fai Ben, adirittura 100!?)'

st.title('Analgram!')
st.write('Fottuto idiota, benvenuto')
# st.write('e adesso che cazzo si fa, mi mette una nota?')
stringa_to = st.text_area('il testo in cui cercare')
search = st.text_input('Che cerco??')
if 'dio' in search:
    st.write('sempre con quel cazzo di dio')
elif 'gesù' in search:
    st.write('palese cazzo')
elif 'madonna' in search:
    st.write('scontatissima')

if search:
    result = anagram_this(stringa_to, search)


    st.subheader(f'Ci sono {adjective(result)} {result} nel testo che hai messo')
