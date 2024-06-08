import requests

def get_street_names(city_code):
    url = f"https://api-adresse.data.gouv.fr/search/?q=citycode={city_code}&limit=100"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        street_names = []
        for feature in data['features']:
            if feature['properties']['type'] == 'street':
                street_names.append((feature['properties']['name'], feature['properties']['label']))
        return street_names
    else:
        print("Erreur lors de la requête pour obtenir les noms de rue :", response.status_code)
        return None

def get_street_info(numero, street_name, city_code):
    url = f"https://api-adresse.data.gouv.fr/search/?q={numero}+{street_name}&citycode={city_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erreur lors de la requête pour la rue", street_name, ":", response.status_code)
        return None

city_code = input("Veuillez entrer le code de la ville : ")
street_names = get_street_names(city_code)
if street_names:
    print("Informations sur les rues dans la ville :", city_code)
    with open('info.txt', 'w') as file:
        for street_name, label in street_names:
            numero = 0
            failed_attempts = 0
            print("Recherche des informations pour la rue :", street_name)
            while True:
                failed_attempts += 1
                if failed_attempts > 10:
                    print("Finito")
                    break
                street_info = get_street_info(numero, street_name, city_code)
                if street_info and 'features' in street_info and len(street_info['features']) > 0:
                    score = street_info['features'][0]['properties']['score']
                    if score > 0.90:
                        street_label = street_info['features'][0]['properties']['label']
                        print(f"{street_label}")
                        file.write(f"{street_label}\n")
                        failed_attempts -= 1
                    numero += 1
                else:
                    print("Aucune information trouvée pour la rue", street_name)
                    break
