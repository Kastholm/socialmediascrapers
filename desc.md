1. Et python program med GPT, hvor GPT læser en JSON fil og kan udføre kommandoerne nedenunder.
2. Gennemgå 100 JSON posts, en JSON post ad gangen og kig på kommentarene.
3. Kommentarene og dens data skal fordeles mellem negative, neutrale, positive kommentarer. Der findes en fil til hver af disse kommentartyper 'negativ.json', 'neutral.json', 'positiv.json' hvor dataen skal indsættes. Der skal ikke oprettes en ny fil for hver kommentar, men i stedet skal en fil rumme alle negative kommentarer fx, samme gælder for de 2 andre filer.
Du skal kun analyserer øverste kommentars type. De replies som er på kommentaren skal blot videresendes med kommentaren til den fil der vælges. Dette gøres da vi kun ønsker at analyserer humøret på øverste kommentar og derefter analyserer måden der bliver svaret på i denne kommentartråd, det er derfor vigtigt at replies til en given kommentar ikke frasorteres samt ikke analyseres.
4. Hver kommentar du fordeler rundt, skal have tre nye felter der hedder "videoTitel", "videoUrl" og "videoLikes", det skal være den originale posts "videoTitel", "videoUrl" og "videoLikes", som blot skal følge med, så vi senere kan differentierer kommentarene.

Her ses et eksempel.
Alt dataen fra kommentaren skal med i samme JSON struktur som original, dog er "videoTitel", "videoUrl" og "videoLikes" inkluderet:
        {
            "videoTitel": "Titel",
            "videoUrl": "URL",
            "videoLikes" "likes",
            "user": "Anonymous",
            "likes": "3 likes",
            "timestamp": "2022-11-18",
            "comment": "Tak @3danmark & @fc_kobenhavn for opbakningen 🧡 Vi glæder os til masser af smil i Parken 😃⚽️🫶🏼",
            "replies": [
                {
                    "user": "3danmark",
                    "likes": "0",
                    "timestamp": "2022-11-18",
                    "comment": "Det gør vi bestemt også 🫶🏼🥰"
                }
            ]
        },