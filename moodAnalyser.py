from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()

client = OpenAI(
    api_key= os.getenv("GPT_API_KEY"),
)

negativeFolder = './fbMood/moodAnalyzes/negative.json'
neutralFolder = './fbMood/moodAnalyzes/neutral.json'
positiveFolder = './fbMood/moodAnalyzes/positive.json'

#file = '/insta_scrape'
singleFile = '/fb_scrape_'

#jsonFiles = './instaScrapes'
jsonFiles = './facebookScrapes2'

index = 29

while index < 65:
    scanFile = f'{jsonFiles}/{singleFile}{index}.json'
    print('analysing file', index)
    if not os.path.isfile(scanFile):
        print(f"Fil mangler: {scanFile}")
        index += 1
        continue

    # Læs JSON-fil og indlæs data
    with open(scanFile, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Fejl ved indlæsning af JSON-fil: {e}")


    for comment in data["comments"]:
        # Indsæt nødvendige metadata
        comment["videoTitel"] = data["videoTitle"]
        comment["videoLikes"] = data["likes"] or 'undefined'

        # Prompt GPT til at klassificere kommentaren
        prompt = f"""
        Du skal udføre en sentimentanalyse på følgende kommentar. 
        Din opgave er at klassificere stemningen som enten 'negativ', 'neutral' eller 'positiv'. 
        Efter klassificeringen skal du give en kort forklaring på, hvorfor du har valgt denne stemning. 
        Vær opmærksom på:
        - Sarkasme eller ironi (fx brug af positivt sprog til at udtrykke negativitet).
        - Emojis og symboler, der kan indikere følelser.
        - Konteksten i kommentaren, selv hvis den er kort.
        - Blandede følelser: vælg den dominerende stemning, og angiv hvorfor.
        - Meget korte eller uforståelige kommentarer: svar '[Neutral]: Utilstrækkelig information til vurdering.'

        Kommentar: "{comment['comment']}"
        VIGTIGT - Svar kun i dette format:
        Stemning: Forklaring
        """
        completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",
        )
        #sentiment = completion.choices[0].message.content.strip().lower()
        response = completion.choices[0].message.content.strip().lower()
        sentiment, explanation = response.split(": ", 1)
        print(sentiment)

        comment["Sentinment_Mood"] = sentiment
        comment["Sentinment_Mood_Reason"] = explanation

        # Definer filsti baseret på sentiment
        if sentiment in ["negative", "negativ", "[negativ]", "[negative]"]:
            file_path = negativeFolder
        elif sentiment in ["neutral", "[neutral]"]:
            file_path = neutralFolder
        elif sentiment in ["positive", "positiv", "[positiv]", "[positive]"]:
            file_path = positiveFolder
        else:
            print(f"Uventet sentiment: {sentiment}")
            continue

        # Læs eksisterende data i filen
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    existing_data = []  # Hvis filen er tom, start med en tom liste
                else:
                    existing_data = json.loads(content)  # Indlæs eksisterende data
        except FileNotFoundError:
            existing_data = []  # Hvis filen ikke findes, start med en tom liste
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError i {file_path}: {e}")
            existing_data = []  # Hvis der er en JSON-fejl, start med en tom liste

        # Tilføj den nye kommentar
        existing_data.append(comment)

        # Skriv opdateret data tilbage til filen
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)



    index += 1