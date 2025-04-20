# Générateur de musique par chaînes de Markov

Ce projet implémente un générateur de musique utilisant des chaînes de Markov d'ordre variable pour créer de nouvelles mélodies à partir d'airs connus. En analysant les motifs et transitions dans des mélodies existantes, le programme génère de nouvelles séquences musicales qui conservent certaines caractéristiques statistiques de l'original.

## Concept

Les chaînes de Markov sont des processus stochastiques où la probabilité d'un état futur dépend uniquement de l'état présent. Dans le contexte musical :
- Une chaîne d'ordre 1 prédit la prochaine note uniquement en fonction de la note actuelle
- Une chaîne d'ordre 2 utilise les deux dernières notes pour prédire la suivante
- Une chaîne d'ordre n utilise les n dernières notes pour déterminer la suivante

Plus l'ordre est élevé, plus la mélodie générée ressemble à l'original, mais avec moins de variations créatives.

## Fonctionnalités

- Analyse de mélodies en utilisant des chaînes de Markov d'ordre variable (1 à n)
- Génération de nouvelles mélodies basées sur les matrices de transition
- Création de fichiers MIDI jouables pour les mélodies originales et générées
- Analyse comparative des distributions de notes
- Mélodies préprogrammées : "Au Clair de la Lune" et "La Marseillaise"
- Interface interactive pour le choix des mélodies et paramètres

## Utilisation

### Prérequis

```
pip install numpy midiutil
```

### Exécution de base

```python
python main_ordre_1_et_2.py.py
```

Le programme vous proposera de choisir une mélodie source et générera plusieurs variations en utilisant des chaînes de Markov d'ordres différents.

### Écoute des résultats

Les fichiers MIDI générés peuvent être lus avec n'importe quel lecteur compatible MIDI :
- Windows Media Player (sous Windows)
- VLC Media Player (toutes plateformes)
- MuseScore (pour visualiser également la partition)

## Structure du code

Le projet est organisé en plusieurs modules fonctionnels :

- **Construction des matrices de transition** : Analyse des séquences et calcul des probabilités
- **Génération de mélodies** : Création de nouvelles séquences à partir des matrices
- **Utilitaires MIDI** : Conversion des séquences en fichiers musicaux jouables
- **Analyse statistique** : Comparaison entre les mélodies originales et générées
- **Mélodies prédéfinies** : Codage des mélodies connues en notation musicale
- **Interface utilisateur** : Fonctions interactives pour l'expérimentation

## Exemple d'utilisation avancée

```python
# Import du module
from markov_music import *

# Charger une mélodie prédéfinie
melodie, durees = melodie_au_clair_de_la_lune()

# Construire une matrice de transition d'ordre 3
matrice = construire_matrice_transition_ordre_n(melodie, n=3)

# Générer une nouvelle mélodie de 40 notes
nouvelle_melodie = generer_melodie_ordre_n(matrice, melodie[:3], 40, n=3)

# Créer un fichier MIDI
creer_fichier_midi(nouvelle_melodie, generer_durees(len(nouvelle_melodie)), tempo=120, nom_fichier="nouvelle_melodie.mid")
```

## Applications pédagogiques

Ce projet est particulièrement adapté pour illustrer plusieurs concepts :
- Probabilités conditionnelles et chaînes de Markov
- Analyse statistique de motifs
- Génération procédurale de contenu créatif
- Programmation modulaire en Python

## Extensions possibles

- Ajouter d'autres mélodies sources
- Implémenter des chaînes de Markov pour les durées (au lieu de les générer aléatoirement)
- Créer une interface graphique
- Ajouter l'analyse harmonique pour générer des accompagnements
- Permettre l'importation de fichiers MIDI externes

## Licence

Ce projet est disponible sous licence libre MIT.
