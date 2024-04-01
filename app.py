import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
from tools.functions import count_faces,recognize_user,is_valid_photo

"""
# Cognitive Enviroment
Sistema para validação de Identidade
Carregue uma foto do Nicolas Cage e valide seu acesso
"""

uploaded_file = st.file_uploader('Tente uma outra imagem', type=["png", "jpg"])
if uploaded_file is not None:
    bytes_data = bytearray(uploaded_file.getvalue())

camera = st.camera_input("Tire sua foto", help="Lembre-se de permitir ao seu navegador o acesso a sua câmera.")


if camera is not None:
    bytes_data =bytearray(camera.getvalue())
    print(type(camera.getvalue()))
   
if camera or uploaded_file:
    with st.spinner('Classificando imagem...'):
        if is_valid_photo(bytes_data):
            n=count_faces(bytes_data)
            if n==1:
                name=recognize_user(bytes_data)
                if name =='Usuário não identificado':
                    st.warning('Usuário não identificado')
                else:
                    st.info(f'Seja bem vindo {name}')
                    st.success('Imagem Reconhecida')
            else:
                st.warning('Apenas uma pessoa por imagem')
        else:
            st.warning('Imagem Inválida: Fraude')


