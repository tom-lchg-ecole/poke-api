import requests
import time


def appel_api_robuste(url, max_tentatives=3, delai_base=1):
    tentative = 0

    while tentative < max_tentatives:
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                return {"succes": True, "data": response.json(), "message": "Requête réussie"}

            elif response.status_code == 429:
                tentative += 1
                delai = delai_base * (2 ** (tentative - 1))
                print(f"Erreur 429: Trop de requêtes. Pause de {delai} secondes...")

                if tentative < max_tentatives:
                    time.sleep(delai)
                    continue
                else:
                    return {
                        "succes": False,
                        "data": None,
                        "message": "Erreur 429: Limite de requêtes atteinte. Réessayez plus tard."
                    }

            elif response.status_code == 400:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Erreur 400: Requête invalide. Vérifiez les paramètres."
                }

            elif response.status_code == 401:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Erreur 401: Non autorisé. Token absent ou invalide."
                }

            elif response.status_code == 403:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Erreur 403: Accès interdit."
                }

            elif response.status_code == 404:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Erreur 404: Ressource introuvable."
                }

            elif response.status_code in [500, 503]:
                tentative += 1
                delai = delai_base * (2 ** (tentative - 1))
                print(f"Erreur {response.status_code}: Problème serveur. Tentative {tentative}/{max_tentatives}...")

                if tentative < max_tentatives:
                    time.sleep(delai)
                    continue
                else:
                    return {
                        "succes": False,
                        "data": None,
                        "message": f"Erreur {response.status_code}: Le serveur ne répond pas après {max_tentatives} tentatives."
                    }

            else:
                return {
                    "succes": False,
                    "data": None,
                    "message": f"Erreur {response.status_code}: Erreur inattendue."
                }

        except requests.exceptions.Timeout:
            tentative += 1
            print(f"Timeout: La requête a pris trop de temps. Tentative {tentative}/{max_tentatives}...")

            if tentative < max_tentatives:
                time.sleep(delai_base)
                continue
            else:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Timeout: La requête a expiré après plusieurs tentatives."
                }

        except requests.exceptions.ConnectionError:
            tentative += 1
            print(f"Erreur de connexion. Tentative {tentative}/{max_tentatives}...")

            if tentative < max_tentatives:
                time.sleep(delai_base)
                continue
            else:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Erreur de connexion: Impossible de se connecter à l'API."
                }

        except Exception as e:
            return {
                "succes": False,
                "data": None,
                "message": f"Erreur inattendue: {str(e)}"
            }

    return {
        "succes": False,
        "data": None,
        "message": f"Échec après {max_tentatives} tentatives."
    }


def tester_gestion_erreurs():
    print("=== Test de la fonction de gestion d'erreurs API ===\n")

    print("1. Test avec un Pokémon valide (pikachu):")
    resultat = appel_api_robuste("https://pokeapi.co/api/v2/pokemon/pikachu")
    if resultat["succes"]:
        print(f"✓ {resultat['message']}")
        print(f"  Pokémon: {resultat['data']['name']}")
        print(f"  ID: {resultat['data']['id']}")
    else:
        print(f"✗ {resultat['message']}")

    print("\n2. Test avec un Pokémon inexistant (404):")
    resultat = appel_api_robuste("https://pokeapi.co/api/v2/pokemon/pokemoninexistant999999")
    if resultat["succes"]:
        print(f"✓ {resultat['message']}")
    else:
        print(f"✗ {resultat['message']}")

    print("\n3. Test avec une URL invalide (404):")
    resultat = appel_api_robuste("https://pokeapi.co/api/v2/endpointinvalide/test")
    if resultat["succes"]:
        print(f"✓ {resultat['message']}")
    else:
        print(f"✗ {resultat['message']}")

    print("\n4. Test avec un type valide (fire):")
    resultat = appel_api_robuste("https://pokeapi.co/api/v2/type/fire")
    if resultat["succes"]:
        print(f"✓ {resultat['message']}")
        print(f"  Type: {resultat['data']['name']}")
        print(f"  Nombre de Pokémon: {len(resultat['data']['pokemon'])}")
    else:
        print(f"✗ {resultat['message']}")



    nom_ou_id = input("Entrez le nom ou l'ID du Pokémon: ").lower()

    url = f"https://pokeapi.co/api/v2/pokemon/{nom_ou_id}"
    resultat = appel_api_robuste(url)

    if not resultat["succes"]:
        print(f"\n{resultat['message']}")
        return

    data = resultat["data"]

    print(f"\n=== Statistiques de {data['name'].capitalize()} ===")
    print(f"ID: {data['id']}")
    print(f"Taille: {data['height'] / 10} m")
    print(f"Poids: {data['weight'] / 10} kg")
    print(f"Types: {', '.join([t['type']['name'].capitalize() for t in data['types']])}")
    print(f"\nStatistiques de base:")

    for stat in data['stats']:
        nom_stat = stat['stat']['name']
        valeur_stat = stat['base_stat']

        if nom_stat == 'hp':
            print(f"  Points de vie (HP): {valeur_stat}")
        elif nom_stat == 'attack':
            print(f"  Attaque: {valeur_stat}")
        elif nom_stat == 'defense':
            print(f"  Défense: {valeur_stat}")
        elif nom_stat == 'special-attack':
            print(f"  Attaque spéciale: {valeur_stat}")
        elif nom_stat == 'special-defense':
            print(f"  Défense spéciale: {valeur_stat}")
        elif nom_stat == 'speed':
            print(f"  Vitesse: {valeur_stat}")


    pokemon1 = input("Entrez le nom ou l'ID du premier Pokémon: ").lower()
    pokemon2 = input("Entrez le nom ou l'ID du deuxième Pokémon: ").lower()

    url1 = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}"
    url2 = f"https://pokeapi.co/api/v2/pokemon/{pokemon2}"

    resultat1 = appel_api_robuste(url1)
    resultat2 = appel_api_robuste(url2)

    if not resultat1["succes"]:
        print(f"\nPokémon 1: {resultat1['message']}")
        return
    if not resultat2["succes"]:
        print(f"\nPokémon 2: {resultat2['message']}")
        return

    data1 = resultat1["data"]
    data2 = resultat2["data"]

    hp1 = next(s['base_stat'] for s in data1['stats'] if s['stat']['name'] == 'hp')
    attaque1 = next(s['base_stat'] for s in data1['stats'] if s['stat']['name'] == 'attack')

    hp2 = next(s['base_stat'] for s in data2['stats'] if s['stat']['name'] == 'hp')
    attaque2 = next(s['base_stat'] for s in data2['stats'] if s['stat']['name'] == 'attack')

    print(f"\n=== Comparaison entre {data1['name'].capitalize()} et {data2['name'].capitalize()} ===")
    print(f"\n{data1['name'].capitalize()}:")
    print(f"  Points de vie: {hp1}")
    print(f"  Attaque: {attaque1}")

    print(f"\n{data2['name'].capitalize()}:")
    print(f"  Points de vie: {hp2}")
    print(f"  Attaque: {attaque2}")

    print("\n=== Résultat ===")

    if hp1 > hp2:
        print(f"{data1['name'].capitalize()} a plus de points de vie ({hp1} vs {hp2})")
    elif hp2 > hp1:
        print(f"{data2['name'].capitalize()} a plus de points de vie ({hp2} vs {hp1})")
    else:
        print(f"Les deux Pokémon ont le même nombre de points de vie ({hp1})")

    if attaque1 > attaque2:
        print(f"{data1['name'].capitalize()} a plus d'attaque ({attaque1} vs {attaque2})")
    elif attaque2 > attaque1:
        print(f"{data2['name'].capitalize()} a plus d'attaque ({attaque2} vs {attaque1})")
    else:
        print(f"Les deux Pokémon ont la même attaque ({attaque1})")

    total1 = hp1 + attaque1
    total2 = hp2 + attaque2

    if total1 > total2:
        print(f"\n🏆 {data1['name'].capitalize()} est le plus fort (total: {total1} vs {total2})")
    elif total2 > total1:
        print(f"\n🏆 {data2['name'].capitalize()} est le plus fort (total: {total2} vs {total1})")
    else:
        print(f"\n🤝 Les deux Pokémon sont à égalité (total: {total1})")


