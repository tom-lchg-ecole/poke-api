import asyncio
import aiohttp
import time
from typing import List, Dict


async def appel_api_robuste_async(session, url, max_tentatives=3, delai_base=1):
    tentative = 0

    while tentative < max_tentatives:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"succes": True, "data": data, "message": "Requête réussie", "url": url}

                elif response.status == 429:
                    tentative += 1
                    delai = delai_base * (2 ** (tentative - 1))
                    print(f"Erreur 429 sur {url}: Pause de {delai}s...")

                    if tentative < max_tentatives:
                        await asyncio.sleep(delai)
                        continue
                    else:
                        return {
                            "succes": False,
                            "data": None,
                            "message": "Erreur 429: Limite de requêtes atteinte",
                            "url": url
                        }

                elif response.status == 400:
                    return {
                        "succes": False,
                        "data": None,
                        "message": "Erreur 400: Requête invalide",
                        "url": url
                    }

                elif response.status == 401:
                    return {
                        "succes": False,
                        "data": None,
                        "message": "Erreur 401: Non autorisé",
                        "url": url
                    }

                elif response.status == 403:
                    return {
                        "succes": False,
                        "data": None,
                        "message": "Erreur 403: Accès interdit",
                        "url": url
                    }

                elif response.status == 404:
                    return {
                        "succes": False,
                        "data": None,
                        "message": "Erreur 404: Ressource introuvable",
                        "url": url
                    }

                elif response.status in [500, 503]:
                    tentative += 1
                    delai = delai_base * (2 ** (tentative - 1))
                    print(f"Erreur {response.status} sur {url}: Tentative {tentative}/{max_tentatives}...")

                    if tentative < max_tentatives:
                        await asyncio.sleep(delai)
                        continue
                    else:
                        return {
                            "succes": False,
                            "data": None,
                            "message": f"Erreur {response.status}: Serveur ne répond pas",
                            "url": url
                        }

                else:
                    return {
                        "succes": False,
                        "data": None,
                        "message": f"Erreur {response.status}: Erreur inattendue",
                        "url": url
                    }

        except asyncio.TimeoutError:
            tentative += 1
            print(f"Timeout sur {url}: Tentative {tentative}/{max_tentatives}...")

            if tentative < max_tentatives:
                await asyncio.sleep(delai_base)
                continue
            else:
                return {
                    "succes": False,
                    "data": None,
                    "message": "Timeout: Requête expirée",
                    "url": url
                }

        except aiohttp.ClientError as e:
            tentative += 1
            print(f"Erreur de connexion sur {url}: {str(e)}")

            if tentative < max_tentatives:
                await asyncio.sleep(delai_base)
                continue
            else:
                return {
                    "succes": False,
                    "data": None,
                    "message": f"Erreur de connexion: {str(e)}",
                    "url": url
                }

        except Exception as e:
            return {
                "succes": False,
                "data": None,
                "message": f"Erreur inattendue: {str(e)}",
                "url": url
            }

    return {
        "succes": False,
        "data": None,
        "message": f"échec après {max_tentatives} tentatives",
        "url": url
    }


async def batch_requetes(urls: List[str], taille_batch=50):
    resultats = []

    connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
    async with aiohttp.ClientSession(connector=connector) as session:
        for i in range(0, len(urls), taille_batch):
            batch = urls[i:i + taille_batch]
            print(f"\nTraitement du batch {i//taille_batch + 1}/{(len(urls) + taille_batch - 1)//taille_batch}")

            tasks = [appel_api_robuste_async(session, url) for url in batch]
            batch_resultats = await asyncio.gather(*tasks)
            resultats.extend(batch_resultats)

            if i + taille_batch < len(urls):
                await asyncio.sleep(0.1)

    return resultats


async def simuler_charge_elevee(nombre_requetes=1000):
    print(f"\n{'='*60}")
    print(f"Simulation de charge élevée: {nombre_requetes} requêtes")
    print(f"{'='*60}")

    urls = [f"https://pokeapi.co/api/v2/pokemon/{i % 150 + 1}" for i in range(nombre_requetes)]

    debut = time.time()
    resultats = await batch_requetes(urls, taille_batch=50)
    duree = time.time() - debut

    succes = sum(1 for r in resultats if r["succes"])
    echecs = len(resultats) - succes

    print(f"\n{'='*60}")
    print(f"Résultats de la simulation:")
    print(f"{'='*60}")
    print(f"Nombre total de requêtes: {len(resultats)}")
    print(f"Requêtes réussies: {succes} ({succes/len(resultats)*100:.2f}%)")
    print(f"Requêtes échouées: {echecs} ({echecs/len(resultats)*100:.2f}%)")
    print(f"Temps total: {duree:.2f} secondes")
    print(f"Débit: {len(resultats)/duree:.2f} requête/seconde")
    print(f"{'='*60}")

    return resultats


async def comparer_pokemon_async(pokemon1: str, pokemon2: str):
    url1 = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}"
    url2 = f"https://pokeapi.co/api/v2/pokemon/{pokemon2}"

    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            appel_api_robuste_async(session, url1),
            appel_api_robuste_async(session, url2)
        ]
        resultats = await asyncio.gather(*tasks)

    resultat1, resultat2 = resultats

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


async def analyser_type_pokemon_async(type_pokemon: str):
    url = f"https://pokeapi.co/api/v2/type/{type_pokemon}"

    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        resultat = await appel_api_robuste_async(session, url)

        if not resultat["succes"]:
            print(f"\n{resultat['message']}")
            return

        data = resultat["data"]
        liste_pokemon = data['pokemon']
        nombre_pokemon = len(liste_pokemon)

        print(f"\n=== Analyse du type {type_pokemon.capitalize()} ===")
        print(f"Nombre de Pokémon de type {type_pokemon}: {nombre_pokemon}")

        echantillon = min(50, nombre_pokemon)
        print(f"\nCalcul de la moyenne des HP (sur un échantillon de {echantillon} Pokémon)...")

        urls_pokemon = [p['pokemon']['url'] for p in liste_pokemon[:echantillon]]
        tasks = [appel_api_robuste_async(session, url) for url in urls_pokemon]
        resultats_pokemon = await asyncio.gather(*tasks)

        total_hp = 0
        count_hp = 0

        for resultat_poke in resultats_pokemon:
            if resultat_poke["succes"]:
                pokemon_data = resultat_poke["data"]
                hp = next(s['base_stat'] for s in pokemon_data['stats'] if s['stat']['name'] == 'hp')
                total_hp += hp
                count_hp += 1

        if count_hp > 0:
            moyenne_hp = total_hp / count_hp
            print(f"Moyenne des points de vie (HP): {moyenne_hp:.2f}")
        else:
            print("Impossible de calculer la moyenne des HP")


async def test_comparaison_performance():
    print("\n" + "="*60)
    print("Test de comparaison: Synchrone vs Asynchrone")
    print("="*60)

    nombre_requetes = 100
    urls = [f"https://pokeapi.co/api/v2/pokemon/{i % 150 + 1}" for i in range(nombre_requetes)]

    print(f"\nTest avec {nombre_requetes} requêtes...")

    debut = time.time()
    resultats = await batch_requetes(urls, taille_batch=25)
    duree_async = time.time() - debut

    succes = sum(1 for r in resultats if r["succes"])

    print(f"\n{'='*60}")
    print(f"Résultats Asynchrones:")
    print(f"  Durée: {duree_async:.2f} secondes")
    print(f"  Débit: {nombre_requetes/duree_async:.2f} requêtes/seconde")
    print(f"  Taux de succès: {succes/nombre_requetes*100:.2f}%")
    print(f"{'='*60}")


async def menu_principal():
    while True:
        print("\n" + "="*60)
        print("=== MENU PRINCIPAL - PokéAPI (Version Asynchrone) ===")
        print("="*60)
        print("1. Simuler une charge élevée (100 requêtes)")
        print("2. Simuler une charge très élevée (1000 requêtes)")
        print("3. Simuler une charge massive (5000 requêtes)")
        print("4. Comparer deux Pokémon (async)")
        print("5. Analyser un type de Pokémon (async)")
        print("6. Test de comparaison de performance")
        print("7. Quitter")
        print("="*60)

        choix = input("\nChoisissez une option (1-7): ")

        if choix == "1":
            await simuler_charge_elevee(100)
        elif choix == "2":
            await simuler_charge_elevee(1000)
        elif choix == "3":
            await simuler_charge_elevee(5000)
        elif choix == "4":
            pokemon1 = input("Entrez le nom ou l'ID du premier Pokémon: ").lower()
            pokemon2 = input("Entrez le nom ou l'ID du deuxième Pokémon: ").lower()
            await comparer_pokemon_async(pokemon1, pokemon2)
        elif choix == "5":
            type_pokemon = input("Entrez le type de Pokémon (ex: fire, water, dragon): ").lower()
            await analyser_type_pokemon_async(type_pokemon)
        elif choix == "6":
            await test_comparaison_performance()
        elif choix == "7":
            print("\nAu revoir!")
            break
        else:
            print("\nOption invalide. Veuillez choisir entre 1 et 7.")


if __name__ == "__main__":
    asyncio.run(menu_principal())
