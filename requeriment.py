import streamlit as st
import pandas as pd


if "tracks" not in st.session_state:
    st.session_state.tracks = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

def add_track(titulo, artista, duracao, url):
    track = {
        "id": st.session_state.next_id,
        "titulo": titulo,
        "artista": artista,
        "duracao": duracao,
        "url": url
    }
    st.session_state.tracks.append(track)
    st.session_state.next_id += 1

def update_track(track_id, titulo=None, artista=None, duracao=None, url=None):
    for track in st.session_state.tracks:
        if track["id"] == track_id:
            if titulo: track["titulo"] = titulo
            if artista: track["artista"] = artista
            if duracao: track["duracao"] = duracao
            if url: track["url"] = url
            return True
    return False

def delete_track(track_id):
    st.session_state.tracks = [t for t in st.session_state.tracks if t["id"] != track_id]

st.title("DJ Playlist Manager")

st.header("Adicionar nova música")
with st.form("add_form"):
    titulo = st.text_input("Título")
    artista = st.text_input("Artista")
    duracao = st.number_input("Duração (segundos)", min_value=1, step=1)
    url = st.text_input("URL (opcional)")
    submitted = st.form_submit_button("Adicionar")
    if submitted:
        if not titulo or not artista:
            st.error("Campos 'Título' e 'Artista' são obrigatórios")
        else:
            add_track(titulo, artista, duracao, url)
            st.success(f"Música '{titulo}' adicionada!")

st.header("Playlist Atual")
if st.session_state.tracks:
    df = pd.DataFrame(st.session_state.tracks)
    st.dataframe(df)

    st.header("Editar / Deletar música")
    selected_id = st.selectbox("Selecione o ID da música", df["id"])
    selected_track = next((t for t in st.session_state.tracks if t["id"] == selected_id), None)

    if selected_track:
        with st.form("edit_form"):
            new_titulo = st.text_input("Título", value=selected_track["titulo"])
            new_artista = st.text_input("Artista", value=selected_track["artista"])
            new_duracao = st.number_input("Duração (segundos)", min_value=1, step=1, value=selected_track["duracao"])
            new_url = st.text_input("URL", value=selected_track["url"])
            update_submitted = st.form_submit_button("Atualizar")
            delete_submitted = st.form_submit_button("Deletar")
            
            if update_submitted:
                update_track(selected_id, new_titulo, new_artista, new_duracao, new_url)
                st.success("Música atualizada!")
            if delete_submitted:
                delete_track(selected_id)
                st.warning("Música deletada!")
else:
    st.info("Nenhuma música cadastrada ainda.")