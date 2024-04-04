from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pathlib import Path

df = pd.read_csv(Path(__file__).parent / "datasets/" / "Spotify.csv")

#limpiando df original
columnas_importantes = ['Danceability', 'Energy', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Valence', 'Tempo']

df_musica = df.dropna(subset=columnas_importantes)
# df_musica = df.drop(["Url_spotify", "Url_youtube", "Channel", "Comments", "Description", "Licensed", "official_video"], axis=1)

matriz_musica = df_musica[columnas_importantes].to_numpy()

matriz_similitud = cosine_similarity(matriz_musica)

# prompt: create a function for get best recomendation for one song

def get_best_recommendations(nombre_cancion, artista, matriz_similaridad, df_user):
    """
    Returns the name of the song that is most similar to the given song.

    Args:
        nombre_cancion: The name of the song to find the best recommendation for.
        artista: El nombre del artista de la cancion
        matriz_similaridad: A 2D array of cosine similarities between all pairs of songs.

    Returns:
        array de elementos recomendados que contiene el Track, Artist y uri de la cancion
    """

    # Get the index of the given song in the similarity matrix.
    df_canciones = df_musica[df_musica["Track"].str.contains(nombre_cancion, regex=False)]
    
    if not df_canciones.empty:
        index_cancion = df_canciones.index[0]
    else:
        index_cancion = df_musica[df_musica["Artist"] == artista].index[0]

    # Obtener los indices con mayor similaridad para la canción
    similar_song_indexes = matriz_similaridad[index_cancion].argsort()[::-1][3:10]

    # Obtener orden según importancia
    mean_user = df_user[columnas_importantes].mean().to_numpy()
    idxs = mean_user.argsort()[-5:][::-1]
    orden_columnas = df_user[columnas_importantes].columns[idxs].to_list()

    # Ordenar según importancia de columnas
    canciones_ordenadas = df_musica.iloc[similar_song_indexes].sort_values(by=orden_columnas, ascending=False)

    # Obtener los nombres de las canciones más similares
    canciones_similares = canciones_ordenadas[["Track", "Artist", "Uri"]].to_numpy()

    # Retornas los nombres de las canciones más similares
    return canciones_similares

def filtro_colaborativo(df_usuarios_canciones:pd.DataFrame, id_usuario:str):
    df_transformed = df_usuarios_canciones.replace({0: -1}).fillna(0)

    idx_user = df_usuarios_canciones[df_usuarios_canciones.id == id_usuario].index
    matriz_similitud_usuarios = cosine_similarity(df_transformed)
    

    



    # Obtener preferencias del usuario
    user_preferences = df_transformed.iloc[idx_user, 1:].reset_index(drop=True).loc[0]

    # Calcular la similitud de los usuarios
    user_similarity = matriz_similitud_usuarios[idx_user]


def crear_df_user(data):
    df_user = pd.DataFrame(data, columns=["Track", "Artist"])
    return pd.merge(df_user, df_musica, on=["Track", "Artist"], how="inner")
