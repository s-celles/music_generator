"""
Générateur de musique par chaînes de Markov

Ce module implémente des chaînes de Markov d'ordre 1 et 2 pour générer
de nouvelles mélodies à partir d'une mélodie source. Le programme analyse
les probabilités de transition entre les notes et utilise ces informations
pour créer de nouvelles séquences musicales qui conservent certaines
caractéristiques statistiques de la mélodie originale.

Utilisation:
    python markov_music.py

Dépendances externes:
    - numpy
    - midiutil
"""

# Import des bibliothèques nécessaires
import random
import numpy as np
from midiutil import MIDIFile


def construire_matrice_transition(sequence):
    """
    Construit une matrice de transition pour une chaîne de Markov d'ordre 1.

    La matrice de transition contient les probabilités de passer d'une note
    à une autre, calculées à partir de la fréquence de ces transitions dans
    la séquence d'entrée.

    Args:
        sequence (list): Une liste de notes musicales (ex: ["C", "D", "E", ...])

    Returns:
        dict: Un dictionnaire de dictionnaires représentant la matrice de transition.
              Le format est {note_actuelle: {note_suivante: probabilité, ...}, ...}
    """
    # Dictionnaire pour stocker les transitions
    transitions = {}

    # Compter les transitions
    for i in range(len(sequence) - 1):
        note_actuelle = sequence[i]
        note_suivante = sequence[i + 1]

        # Si la note actuelle n'est pas encore dans le dictionnaire, l'initialiser
        if note_actuelle not in transitions:
            transitions[note_actuelle] = {}

        # Incrémenter le compteur pour cette transition
        if note_suivante in transitions[note_actuelle]:
            transitions[note_actuelle][note_suivante] += 1
        else:
            transitions[note_actuelle][note_suivante] = 1

    # Convertir les compteurs en probabilités
    matrice_proba = {}
    for note_actuelle, suivantes in transitions.items():
        total = sum(suivantes.values())
        matrice_proba[note_actuelle] = {
            note_suivante: count / total for note_suivante, count in suivantes.items()
        }

    return matrice_proba


def construire_matrice_transition_ordre2(sequence):
    """
    Construit une matrice de transition pour une chaîne de Markov d'ordre 2.

    Dans une chaîne de Markov d'ordre 2, l'état est défini par les deux notes
    précédentes, ce qui permet de capturer des motifs musicaux plus complexes.

    Args:
        sequence (list): Une liste de notes musicales (ex: ["C", "D", "E", ...])

    Returns:
        dict: Un dictionnaire où les clés sont des tuples de deux notes (état actuel)
              et les valeurs sont des dictionnaires {note_suivante: probabilité, ...}
    """
    transitions = {}

    for i in range(len(sequence) - 2):
        etat_actuel = (sequence[i], sequence[i + 1])  # Paire de notes
        note_suivante = sequence[i + 2]

        if etat_actuel not in transitions:
            transitions[etat_actuel] = {}

        if note_suivante in transitions[etat_actuel]:
            transitions[etat_actuel][note_suivante] += 1
        else:
            transitions[etat_actuel][note_suivante] = 1

    # Convertir en probabilités
    matrice_proba = {}
    for etat, suivantes in transitions.items():
        total = sum(suivantes.values())
        matrice_proba[etat] = {
            note_suivante: count / total for note_suivante, count in suivantes.items()
        }

    return matrice_proba


def generer_melodie(matrice, note_depart, longueur):
    """
    Génère une mélodie à partir d'une matrice de transition de Markov d'ordre 1.

    Le processus commence par la note de départ, puis choisit les notes suivantes
    en fonction des probabilités dans la matrice de transition.

    Args:
        matrice (dict): La matrice de transition d'ordre 1
        note_depart (str): La première note de la mélodie générée
        longueur (int): Le nombre total de notes à générer

    Returns:
        list: La séquence de notes générée
    """
    melodie = [note_depart]
    note_actuelle = note_depart

    for _ in range(longueur - 1):
        # Si la note actuelle n'est pas dans la matrice, choisir une note aléatoire
        if note_actuelle not in matrice:
            note_actuelle = random.choice(list(matrice.keys()))
            melodie.append(note_actuelle)
            continue

        # Obtenir les probabilités de transition depuis la note actuelle
        possibilites = matrice[note_actuelle]

        # Choisir la prochaine note en fonction des probabilités
        note_suivante = random.choices(
            list(possibilites.keys()), weights=list(possibilites.values()), k=1
        )[0]

        melodie.append(note_suivante)
        note_actuelle = note_suivante

    return melodie


def generer_melodie_ordre2(matrice, notes_depart, longueur):
    """
    Génère une mélodie à partir d'une matrice de transition de Markov d'ordre 2.

    Le processus commence par les deux notes de départ, puis choisit les notes
    suivantes en fonction des probabilités associées à chaque paire de notes.

    Args:
        matrice (dict): La matrice de transition d'ordre 2
        notes_depart (tuple): Les deux premières notes de la mélodie (n1, n2)
        longueur (int): Le nombre total de notes à générer

    Returns:
        list: La séquence de notes générée

    Raises:
        ValueError: Si moins de deux notes de départ sont fournies
    """
    if len(notes_depart) < 2:
        raise ValueError(
            "Pour une chaîne d'ordre 2, il faut au moins 2 notes de départ"
        )

    melodie = list(notes_depart)
    etat_actuel = (notes_depart[0], notes_depart[1])

    for _ in range(longueur - 2):
        # Si l'état actuel n'est pas dans la matrice, choisir un nouvel état aléatoire
        if etat_actuel not in matrice:
            nouvel_etat = random.choice(list(matrice.keys()))
            melodie.append(nouvel_etat[1])  # Ajouter seulement la deuxième note
            etat_actuel = (etat_actuel[1], nouvel_etat[1])
            continue

        # Obtenir les probabilités de transition depuis l'état actuel
        possibilites = matrice[etat_actuel]

        # Choisir la prochaine note en fonction des probabilités
        note_suivante = random.choices(
            list(possibilites.keys()), weights=list(possibilites.values()), k=1
        )[0]

        melodie.append(note_suivante)
        etat_actuel = (etat_actuel[1], note_suivante)

    return melodie


def generer_durees(longueur, durees_possibles=[0.5, 1, 2]):
    """
    Génère des durées aléatoires pour une séquence de notes.

    Cette fonction est simplifiée par rapport à une vraie chaîne de Markov
    pour les durées, et se contente de choisir aléatoirement parmi un
    ensemble de durées possibles.

    Args:
        longueur (int): Le nombre de durées à générer
        durees_possibles (list, optional): Liste des durées possibles en temps
                                         (0.5=croche, 1=noire, 2=blanche)

    Returns:
        list: Une liste de durées pour chaque note
    """
    return [random.choice(durees_possibles) for _ in range(longueur)]


def creer_fichier_midi(notes, durees, tempo=120, nom_fichier="melodie_generee.mid"):
    """
    Crée un fichier MIDI à partir d'une séquence de notes et de durées.

    Convertit les noms de notes (C, D, E...) en valeurs MIDI et génère
    un fichier MIDI jouable avec les durées spécifiées.

    Args:
        notes (list): Liste des noms de notes (ex: ["C", "E", "G", ...])
        durees (list): Liste des durées correspondantes (ex: [1, 0.5, 2, ...])
        nom_fichier (str, optional): Nom du fichier MIDI à créer

    Returns:
        None: Le résultat est écrit dans un fichier
    """
    # Conversion des noms de notes en valeurs MIDI
    note_to_midi = {
        "C": 60,
        "C#": 61,
        "Db": 61,
        "D": 62,
        "D#": 63,
        "Eb": 63,
        "E": 64,
        "F": 65,
        "F#": 66,
        "Gb": 66,
        "G": 67,
        "G#": 68,
        "Ab": 68,
        "A": 69,
        "A#": 70,
        "Bb": 70,
        "B": 71,
    }

    # Créer un fichier MIDI avec 1 piste
    midi = MIDIFile(1)

    track = 0
    time = 0
    # tempo = 120  # BPM
    channel = 0
    volume = 100  # 0-127

    # Ajouter le nom de la piste et le tempo
    midi.addTrackName(track, time, "Mélodie générée par chaîne de Markov")
    midi.addTempo(track, time, tempo)

    # Ajouter les notes
    for note, duree in zip(notes, durees):
        if note in note_to_midi:
            midi.addNote(track, channel, note_to_midi[note], time, duree, volume)
            time += duree

    # Écrire le fichier MIDI
    with open(nom_fichier, "wb") as output_file:
        midi.writeFile(output_file)

    print(f"Fichier MIDI créé : {nom_fichier}")


def analyser_distribution(sequence):
    """
    Analyse la distribution des notes dans une séquence musicale.

    Calcule la fréquence relative de chaque note dans la séquence,
    permettant de comparer les caractéristiques statistiques de
    différentes mélodies.

    Args:
        sequence (list): Une liste de notes musicales

    Returns:
        dict: Un dictionnaire {note: fréquence_relative, ...}
    """
    distribution = {}

    for note in sequence:
        if note in distribution:
            distribution[note] += 1
        else:
            distribution[note] = 1

    total = len(sequence)
    distribution_proba = {note: count / total for note, count in distribution.items()}

    return distribution_proba


def melodie_au_clair_de_la_lune():
    melodie_source = [
        "C",
        "C",
        "C",
        "D",
        "E",
        "D",
        "C",
        "E",
        "D",
        "D",
        "C",
        "C",
        "C",
        "C",
        "D",
        "E",
        "D",
        "C",
        "E",
        "D",
        "D",
        "C",
        "D",
        "D",
        "D",
        "D",
        "A",
        "A",
        "D",
        "C",
        "B",
        "A",
        "G",
        "C",
        "C",
        "C",
        "D",
        "E",
        "D",
        "C",
        "E",
        "D",
        "D",
        "C",
    ]

    # Durées des notes (en temps, 1.0 = noire)
    # Simplifié pour correspondre à la mélodie
    durees_source = [
        1,
        1,
        1,
        1,
        2,
        2,
        1,
        1,
        1,
        1,
        4,
        1,
        1,
        1,
        1,
        2,
        2,
        1,
        1,
        1,
        1,
        4,
        1,
        1,
        1,
        1,
        2,
        2,
        1,
        1,
        1,
        1,
        4,
        1,
        1,
        1,
        1,
        2,
        2,
        1,
        1,
        1,
        1,
        4,
    ]

    return melodie_source, durees_source


def melodie_marseillaise():
    """
    Retourne la mélodie de La Marseillaise en notation musicale et ses durées.

    La mélodie est simplifiée et limitée aux premières mesures emblématiques
    de l'hymne national français, adaptée pour le traitement par chaînes de Markov.

    Returns:
        tuple: Un tuple contenant deux listes:
            - La séquence de notes de La Marseillaise
            - Les durées correspondantes
    """
    # Début de La Marseillaise en Do majeur
    # "Allons enfants de la patrie, le jour de gloire est arrivé"
    melodie_source = [
        "F",
        "F",
        "F",
        "D",
        "G",
        "G",  # Allons en-fants de la
        "A",
        "A",
        "Bb",
        "G",  # pa-tri-e
        "A",
        "Bb",
        "C",
        "C",
        "Bb",
        "A",  # Le jour de gloire est ar-
        "G",
        "F",
        "F",  # ri-vé
        "Bb",
        "Bb",
        "Bb",
        "A",
        "G",
        "A",  # Contre nous de la ty-
        "Bb",
        "G",
        "A",
        "F",  # ran-ni-e
        "G",
        "G",
        "A",
        "G",
        "F",
        "E",  # L'éten-dard san-glant est
        "D",
        "C",
        "C",  # le-vé
        "C",
        "C",
        "D",
        "E",
        "F",  # L'éten-dard san-glant
        "F",
        "G",
        "A",
        "Bb",
        "C",  # est le-vé
    ]

    # Durées approximatives (en temps, 1.0 = noire)
    durees_source = [
        1,
        0.5,
        0.5,
        1,
        1,
        1,  # Allons en-fants de la
        0.5,
        0.5,
        1,
        2,  # pa-tri-e
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,  # Le jour de gloire est ar-
        1,
        1,
        2,  # ri-vé
        1,
        0.5,
        0.5,
        1,
        1,
        1,  # Contre nous de la ty-
        0.5,
        0.5,
        1,
        2,  # ran-ni-e
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,  # L'éten-dard san-glant est
        1,
        1,
        2,  # le-vé
        0.5,
        0.5,
        0.5,
        0.5,
        1,  # L'éten-dard san-glant
        0.5,
        0.5,
        0.5,
        0.5,
        2,  # est le-vé
    ]

    return melodie_source, durees_source


def main():
    """
    Fonction principale qui exécute le processus complet de génération musicale.

    Cette fonction:
    1. Définit une mélodie source
    2. Construit des matrices de transition d'ordre 1 et 2
    3. Génère de nouvelles mélodies avec ces matrices
    4. Crée des fichiers MIDI pour la mélodie originale et les mélodies générées
    5. Compare les distributions de notes entre les différentes mélodies
    """
    # Définir une graine aléatoire pour la reproductibilité
    random.seed(0)  # Commenter cette ligne pour des résultats différents

    # Choisir une mélodie source
    melodie_source, durees_source = melodie_au_clair_de_la_lune()
    tempo = 120  # BPM

    # melodie_source, durees_source = melodie_marseillaise()
    # tempo = 80  # BPM

    # 1. Définition de la mélodie source en notation musicale
    # Les notes de la mélodie (Do majeur) - Au Clair de la Lune
    # 2. Construire la matrice de transition pour la mélodie source
    matrice_transition = construire_matrice_transition(melodie_source)

    # Afficher la matrice de transition
    print("Matrice de transition pour la mélodie source:")
    for note, transitions in matrice_transition.items():
        print(f"Note {note} -> {transitions}")

    # 3. Construire la matrice de transition d'ordre 2
    matrice_transition_ordre2 = construire_matrice_transition_ordre2(melodie_source)

    # 4. Générer une mélodie avec la chaîne de Markov d'ordre 1
    print("\nGénération d'une mélodie avec une chaîne de Markov d'ordre 1:")
    melodie_ordre1 = generer_melodie(matrice_transition, "C", 30)
    print(" ".join(melodie_ordre1))

    # 5. Générer une mélodie avec la chaîne de Markov d'ordre 2
    print("\nGénération d'une mélodie avec une chaîne de Markov d'ordre 2:")
    melodie_ordre2 = generer_melodie_ordre2(matrice_transition_ordre2, ("C", "C"), 30)
    print(" ".join(melodie_ordre2))

    # 6. Générer des durées pour les notes
    durees_ordre1 = generer_durees(len(melodie_ordre1))
    durees_ordre2 = generer_durees(len(melodie_ordre2))

    # 7. Créer des fichiers MIDI
    # Générer le fichier MIDI du morceau original
    creer_fichier_midi(
        melodie_source, durees_source, tempo, "melodie_source_original.mid"
    )
    print("Fichier MIDI du morceau original créé")

    # Créer les fichiers MIDI des mélodies générées
    creer_fichier_midi(
        melodie_ordre1, durees_ordre1, tempo, "melodie_markov_ordre1.mid"
    )
    creer_fichier_midi(
        melodie_ordre2, durees_ordre2, tempo, "melodie_markov_ordre2.mid"
    )
    print("Fichiers MIDI des mélodies générées créés")

    # 8. Comparer les distributions des notes
    print("\nDistribution des notes dans la mélodie source originale:")
    print(analyser_distribution(melodie_source))

    print("\nDistribution des notes dans la mélodie générée (ordre 1):")
    print(analyser_distribution(melodie_ordre1))

    print("\nDistribution des notes dans la mélodie générée (ordre 2):")
    print(analyser_distribution(melodie_ordre2))


if __name__ == "__main__":
    main()
