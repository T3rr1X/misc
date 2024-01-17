from AnagramThis import anagram_this
import streamlit as st

st.title('Analgram!')
st.write('Fottuto idiota, benvenuto')
st.write('e adesso che cazzo si fa, mi mette una nota?')
stringa_to = st.text_area('il testo in cui cercare')
search = st.text_input('Che cerco??')
if 'dio' in search:
    st.write('sempre con quel cazzo di dio')
elif 'gesù' in search:
    st.write('palese cazzo')
elif 'madonna':
    st.write('scontatissima')
result = anagram_this(stringa_to, search)


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


st.subheader(f'Ci sono {adjective(result)} nel testo che hai messo')
