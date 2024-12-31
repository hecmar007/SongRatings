import lyricsgenius
import openai
import os
import google.generativeai as genai
import re
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

def get_gemini_response(song_lyrics, full_response=False):
    # Get the GENAI API key from environment variables
    genai_api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=genai_api_key)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    if full_response:
        response = chat_session.send_message(f"""Estoy explorando las letras de diferentes canciones, y me gustaría que evaluaras si la siguiente canción contiene estos temas: empatía, creatividad, toma de decisiones, relaciones interpersonales saludables, resiliencia, racismo, sexismo, abuso de sustancias, violencia, contenido sexual. Explora estos temas como si fueras un oyente escuchando la canción por primera vez.
        
        {song_lyrics}
        
       Para cada tema, da una puntuación del 0 al 10 según cuán presente y relevante sea el tema en la letra. Para cada puntuación, especifica exactamente qué línea o líneas de la letra has utilizado para justificarla.""")
    else:
        response = chat_session.send_message(f"""Estoy explorando las letras de diferentes canciones, y me gustaría que evaluaras si la siguiente canción contiene estos temas: empatía, creatividad, toma de decisiones, relaciones interpersonales saludables, resiliencia, racismo, sexismo, abuso de sustancias, violencia, contenido sexual. Explora estos temas como si fueras un oyente escuchando la canción por primera vez. 
        
        {song_lyrics}
        
        Para cada tema, da una tabla con una puntuación del 0 al 10 para cada tema según cuán presente y relevante sea el tema en la letra.""")

    return response.text


def get_chatgpt_response(song_lyrics, format_instructions=None):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    os.environ.setdefault("OPENAI_API_KEY", openai_api_key)

    prompt = f"""Estoy explorando las letras de diferentes canciones, y me gustaría que evaluaras si la siguiente canción contiene estos temas: empatía, creatividad, toma de decisiones, relaciones interpersonales saludables, resiliencia, racismo, sexismo, abuso de sustancias, violencia, contenido sexual. Explora estos temas como si fueras un oyente escuchando la canción por primera vez.
        
        {song_lyrics}
        
       Para cada tema, da una puntuación del 0 al 10 según cuán presente y relevante sea el tema en la letra. Para cada puntuación, especifica exactamente qué línea o líneas de la letra has utilizado para justificarla."""
    

    if format_instructions:
        prompt += f"\n\n{format_instructions}"

    client = openai.OpenAI()

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion


# Initialize the Genius API client with the key from the .env file
genius_api_key = os.getenv('GENIUS_API_KEY')
genius = lyricsgenius.Genius(genius_api_key)

def get_song_lyrics(song_name, artist_name=None):
    if artist_name:
        song = genius.search_song(song_name, artist=artist_name)
    else:
        song = genius.search_song(song_name)
    if song:
        return song.lyrics
    else:
        print("Song not found!")


def display_ratings(output):
    ratings = [int(match.group(1)) for match in re.finditer(r'\|\s+\w.*?\|\s+(\d+)\s+\|', output)]
    if len(ratings) == 10:
        print(ratings)
    else:
        print("Something went wrong. Please try again")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze song lyrics using APIs.")
    parser.add_argument("-n", "--name", required=True, help="Name of the song to analyze")
    parser.add_argument("-a", "--artist", help="Name of the artist (optional)")
    parser.add_argument("-m", "--model", help="Which model to use, chatGPT or Gemini (Gemini default)")
    args = parser.parse_args()

    song_name = args.name
    artist_name = args.artist
    model_name = args.model
    lyrics = get_song_lyrics(song_name, artist_name)

    if lyrics:
        if model_name != None and model_name.lower() == "chatgpt":
            print("Using ChatGPT")
            output = get_chatgpt_response(lyrics)
        else:
            print("Using Gemini")
            output = get_gemini_response(lyrics)
        display_ratings(output)
    else:
        print("Unable to retrieve lyrics.")