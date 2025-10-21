
print("Work in progress. Module intention: download/unzip/filter\
      all of the data from the cornell corpa automatically")

'''
import os
import requests


# get config 
url = "https://zissou.infosci.cornell.edu/convokit/datasets/download_config.json"
resp = requests.get(url)
resp.raise_for_status()
config = resp.json()

dataset_urls = config["DatasetURLs"]

os.makedirs("convokit_zips", exist_ok=True)

for key, value in dataset_urls.items():
    os.makedirs(f"convokit_zips/{key}", exist_ok=True)


    # Choose a local filename
    filename = os.path.join("convokit_zips", f"{dataset}.zip")
    
    print(f"⬇️ Downloading {dataset} ...")
    with requests.get(zip_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print(f"✅ Saved {filename}")
'''