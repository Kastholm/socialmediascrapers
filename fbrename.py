import os

# Indsæt mappen, hvor filerne ligger
folder_path = "./facebookScrapes"
new_pathh = './fbScrapes'

# Få en liste over alle filer i mappen
files = os.listdir(folder_path)

# Filtrér filerne i den rigtige rækkefølge
files.sort()  # Sorterer alfabetisk

# Start counter for at generere korrekte navne
counter = 0

for file_name in files:
    # Tjek om filen ikke allerede følger navngivningsstandarden
    if not file_name.startswith("fb_scrape_"):
        # Generer det korrekte navn
        new_name = f"fb_scrape_{counter}.json"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(new_pathh, new_name)
        
        # Omdøb filen
        os.rename(old_path, new_path)
        
        print(f"Omdøbt: {file_name} -> {new_name}")
        counter += 1
    elif file_name.startswith("fb_scrape_"):
        # Hvis filnavnet allerede er korrekt, øges tælleren
        counter += 1
