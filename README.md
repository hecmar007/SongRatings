# SongRatings

Repositori pel codi del Treball de Fi de grau del doble grau de Matemàtiques i Eginyeria Informàtica de l'Héctor Balsells Roure.

main.py: Script per obtenir les qualificacions donades per un model de llenguatge als diferents temes de la lletra d'una cançó. Per utilitzar:

python main.py -n "Nom cançó" [-a "Nom artista"] [-m "chatgpt o gemini"]

També fa falta crear un .env amb totes les API keys necessaries, seguint aquest esquema:

GENIUS_API_KEY=KEY
GENAI_API_KEY=KEY
OPENAI_API_KEY=KEY