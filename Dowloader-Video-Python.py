import streamlit as st
import yt_dlp

st.title("Baixador Universal de Vídeos")

url = st.text_input("Cole o link do vídeo aqui:")
alturas_disponiveis = []
thumbnail = None
titulo_video = None

if url:
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formatos = info.get("formats", [])
            thumbnail = info.get("thumbnail")
            titulo_video = info.get("title")
            alturas = set()
            for f in formatos:
                if f.get("height") and f["height"] >= 180:
                    alturas.add(f["height"])
            alturas_disponiveis = sorted(alturas, reverse=True)
    except Exception as e:
        st.warning("Não foi possível verificar as qualidades disponíveis para este vídeo.")

if thumbnail:
    st.image(thumbnail, caption=titulo_video, width=400)

tipo = st.radio("O que você deseja baixar?", ("Vídeo", "Áudio"))

def nome_qualidade(altura):
    if altura >= 4320:
        return f"8K ({altura}p)"
    elif altura >= 2160:
        return f"4K ({altura}p)"
    elif altura >= 1440:
        return f"2K ({altura}p)"
    else:
        return f"{altura}p"

if tipo == "Vídeo":
    if alturas_disponiveis:
        opcoes_qualidade = [nome_qualidade(a) for a in alturas_disponiveis]
        qualidade_escolhida = st.radio("Escolha a qualidade", opcoes_qualidade)
        altura_escolhida = alturas_disponiveis[opcoes_qualidade.index(qualidade_escolhida)]
    else:
        st.info("Cole um link válido para ver as qualidades disponíveis.")
        altura_escolhida = None
else:
    qualidade_escolhida = None

if st.button("Baixar"):
    if tipo == "Vídeo" and altura_escolhida:
        formato = f"bestvideo[height<={altura_escolhida}]+bestaudio/best[height<={altura_escolhida}]"
    elif tipo == "Áudio":
        formato = "bestaudio/best"
    else:
        formato = "best"

    opcoes = {
        "format": formato,
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }

    if tipo == "Áudio":
        opcoes["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }]

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])

    st.success("Download concluído!")