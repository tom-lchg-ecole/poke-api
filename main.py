import requests
from q1_commune import appel_api_robuste


def afficher_statistiques_pokemon():
    nom_ou_id = input("Entrez le nom ou l'ID du Pokémon: ").lower()

    url = f"https://pokeapi.co/api/v2/pokemon/{nom_ou_id}"
    data = appel_api_robuste(url)["data"]

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


def comparer_deux_pokemon():
    pokemon1 = input("Entrez le nom ou l'ID du premier Pokémon: ").lower()
    pokemon2 = input("Entrez le nom ou l'ID du deuxième Pokémon: ").lower()

    url1 = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}"
    url2 = f"https://pokeapi.co/api/v2/pokemon/{pokemon2}"

    data1 = appel_api_robuste(url1)["data"]
    data2 = appel_api_robuste(url2)["data"]


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


def analyser_type_pokemon():
    type_pokemon = input("Entrez le type de Pokémon (ex: fire, water, dragon): ").lower()

    url = f"https://pokeapi.co/api/v2/type/{type_pokemon}"
    data = appel_api_robuste(url)["data"]

    liste_pokemon = data['pokemon']
    nombre_pokemon = len(liste_pokemon)

    print(f"\n=== Analyse du type {type_pokemon.capitalize()} ===")
    print(f"Nombre de Pokémon de type {type_pokemon}: {nombre_pokemon}")

    print(f"\nCalcul de la moyenne des HP (sur un échantillon de {min(50, nombre_pokemon)} Pokémon)...")

    total_hp = 0
    count_hp = 0

    for i, poke in enumerate(liste_pokemon[:50]):
        pokemon_url = poke['pokemon']['url']
        pokemon_response = requests.get(pokemon_url)

        if pokemon_response.status_code == 200:
            pokemon_data = pokemon_response.json()
            hp = next(s['base_stat'] for s in pokemon_data['stats'] if s['stat']['name'] == 'hp')
            total_hp += hp
            count_hp += 1

    if count_hp > 0:
        moyenne_hp = total_hp / count_hp
        print(f"Moyenne des points de vie (HP): {moyenne_hp:.2f}")
    else:
        print("Impossible de calculer la moyenne des HP")


def simuler_combat():
    pokemon1 = input("Entrez le nom ou l'ID du premier Pokémon: ").lower()
    pokemon2 = input("Entrez le nom ou l'ID du deuxième Pokémon: ").lower()

    url1 = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}"
    url2 = f"https://pokeapi.co/api/v2/pokemon/{pokemon2}"

    data1 = appel_api_robuste(url1)["data"]
    data2 = appel_api_robuste(url2)["data"]

    hp1 = next(s['base_stat'] for s in data1['stats'] if s['stat']['name'] == 'hp')
    attaque1 = next(s['base_stat'] for s in data1['stats'] if s['stat']['name'] == 'attack')
    defense1 = next(s['base_stat'] for s in data1['stats'] if s['stat']['name'] == 'defense')

    hp2 = next(s['base_stat'] for s in data2['stats'] if s['stat']['name'] == 'hp')
    attaque2 = next(s['base_stat'] for s in data2['stats'] if s['stat']['name'] == 'attack')
    defense2 = next(s['base_stat'] for s in data2['stats'] if s['stat']['name'] == 'defense')

    print(f"\n=== Combat entre {data1['name'].capitalize()} et {data2['name'].capitalize()} ===")
    print(f"\n{data1['name'].capitalize()}: HP={hp1}, Attaque={attaque1}, Défense={defense1}")
    print(f"{data2['name'].capitalize()}: HP={hp2}, Attaque={attaque2}, Défense={defense2}")

    degats_totaux_1 = 0
    degats_totaux_2 = 0

    for tour in range(1, 6):
        degats_1_vers_2 = max(1, attaque1 - defense2 // 2)
        degats_2_vers_1 = max(1, attaque2 - defense1 // 2)

        degats_totaux_1 += degats_1_vers_2
        degats_totaux_2 += degats_2_vers_1

        print(f"\nTour {tour}:")
        print(f"  {data1['name'].capitalize()} inflige {degats_1_vers_2} dégâts à {data2['name'].capitalize()}")
        print(f"  {data2['name'].capitalize()} inflige {degats_2_vers_1} dégâts à {data1['name'].capitalize()}")

    print(f"\n=== Résultat final ===")
    print(f"Dégâts totaux infligés par {data1['name'].capitalize()}: {degats_totaux_1}")
    print(f"Dégâts totaux infligés par {data2['name'].capitalize()}: {degats_totaux_2}")

    if degats_totaux_1 > degats_totaux_2:
        print(f"\n🏆 {data1['name'].capitalize()} remporte le combat!")
    elif degats_totaux_2 > degats_totaux_1:
        print(f"\n🏆 {data2['name'].capitalize()} remporte le combat!")
    else:
        print(f"\n🤝 Match nul!")


def menu_principal():
    while True:
        print("\n" + "="*50)
        print("=== MENU PRINCIPAL - PokéAPI ===")
        print("="*50)
        print("1. Afficher les statistiques d'un Pokémon")
        print("2. Comparer deux Pokémon")
        print("3. Analyser un type de Pokémon")
        print("4. Simuler un combat entre deux Pokémon")
        print("5. Quitter")
        print("="*50)

        choix = input("\nChoisissez une option (1-5): ")

        if choix == "1":
            afficher_statistiques_pokemon()
        elif choix == "2":
            comparer_deux_pokemon()
        elif choix == "3":
            analyser_type_pokemon()
        elif choix == "4":
            simuler_combat()
        elif choix == "5":
            print("\nAu revoir!")
            break
        else:
            print("\nOption invalide. Veuillez choisir entre 1 et 5.")


if __name__ == "__main__":
    menu_principal()
