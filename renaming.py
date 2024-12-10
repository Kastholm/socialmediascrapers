import os

dir_path = r'./tiktokScrapes'

# Gennemgå filerne og omdøb dem
for index, file in enumerate(os.listdir(dir_path)):
    if os.path.isfile(os.path.join(dir_path, file)) and file.startswith("scrape"):
        source = os.path.join(dir_path, file)
        dest = os.path.join(dir_path, f'tiktok_scrape{index}.json')
        os.rename(source, dest)
        print(f"Renamed {source} to {dest} successfully.")
