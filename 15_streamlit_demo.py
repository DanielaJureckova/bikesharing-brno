import streamlit as st

st.title('Bikesharing Brno - hlavní titulek')
st.header('Toto je hlavička')
st.subheader('Toto je podhlavička')
st.text('Kuk test funguje')

data = {
    'Série A': [1, 2, 3, 4, 5],
    'Série B': [5, 4, 3, 2, 1],
    'Série C': [1, 4, 2, 3, 5]
}

st.write('Data v tabulce:')
st.dataframe(data)

st.line_chart(data)

if st.button('Tlačítko'):
    st.write('Bylo kliknuto na tlačítko!')

checkbox = st.checkbox('Zaškrtávací pole')
if checkbox:
    st.write('Zaškrtávací pole je zaškrtnuto!')

selection = st.selectbox('Výběrové pole', ['možnost 1', 'možnost 2', 'možnost 3'])
st.write('Vybrali jste:', selection)
