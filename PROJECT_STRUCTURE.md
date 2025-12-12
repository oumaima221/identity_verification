# Structure du Projet

Ce document décrit la structure complète du projet et l'organisation des fichiers.

## Structure des Dossiers

```
identity_verification/
│
├── identity_verification/          # Configuration Django principale
│   ├── __init__.py
│   ├── settings.py                 # Configuration de l'application
│   ├── urls.py                     # URLs principales du projet
│   ├── wsgi.py                     # Interface WSGI pour production
│   └── asgi.py                     # Interface ASGI (optionnel)
│
├── verify/                         # Application principale
│   ├── __init__.py
│   ├── admin.py                    # Configuration admin Django
│   ├── apps.py                     # Configuration de l'application
│   ├── models.py                   # Modèles de données MongoDB
│   ├── views.py                    # Vues et logique métier
│   ├── urls.py                     # URLs de l'application
│   ├── tests.py                    # Tests unitaires
│   ├── settings.py                 # Paramètres spécifiques (si nécessaire)
│   ├── duplicate.py                # Détection de doublons
│   ├── check_mongo.py              # Script de vérification MongoDB
│   │
│   ├── compare_face/               # Module de comparaison faciale
│   │   ├── __init__.py
│   │   ├── views.py                # Vues de comparaison faciale
│   │   ├── urls.py                 # URLs de comparaison
│   │   └── CompreFace-master/      # (À supprimer - doit être installé séparément)
│   │
│   ├── ml_models/                  # Modèles de Machine Learning
│   │   └── process_image.py        # Traitement YOLOv5 et OCR
│   │   └── yolo_training/          # Modèles YOLOv5
│   │       └── exp_fixed/
│   │           └── weights/
│   │               └── best.pt     # Modèle YOLOv5 entraîné
│   │
│   ├── static/                     # Fichiers statiques
│   │   ├── css/                    # Feuilles de style
│   │   ├── js/                     # JavaScript
│   │   └── models/                 # Modèles ML (dlib, etc.)
│   │       └── shape_predictor_68_face_landmarks.dat
│   │
│   └── templates/                  # Templates HTML
│       └── verify/
│           ├── upload.html         # Page d'upload
│           └── compare_faces.html  # Page de comparaison
│
├── media/                          # Fichiers uploadés (ignoré par git)
│   └── temp/                       # Fichiers temporaires
│
├── staticfiles/                    # Fichiers statiques collectés (production)
│
├── migrations/                     # Migrations Django
│   └── __init__.py
│
├── manage.py                       # Script de gestion Django
├── requirements.txt                # Dépendances Python
├── .gitignore                      # Fichiers ignorés par Git
├── env.example                     # Exemple de configuration
├── README.md                       # Documentation principale
├── ARCHITECTURE.md                 # Documentation d'architecture
├── CONTRIBUTING.md                 # Guide de contribution
├── SETUP.md                        # Guide d'installation
├── LICENSE                         # Licence du projet
└── PROJECT_STRUCTURE.md            # Ce fichier
```

## Description des Composants

### Configuration Django (`identity_verification/`)

- **`settings.py`** : Configuration principale de Django
  - Variables d'environnement
  - Configuration de la base de données
  - Paramètres de sécurité
  - Configuration des fichiers statiques et médias

- **`urls.py`** : Routage principal
  - Inclut les URLs de l'application `verify`
  - Configuration de l'admin Django

### Application Principale (`verify/`)

#### Modèles (`models.py`)

- **`IdentityInfo`** : Modèle MongoDB pour stocker les informations d'identité
  - `photo_name` : Nom du fichier photo
  - `id_number` : Numéro CIN
  - `first_name` : Prénom
  - `last_name` : Nom de famille
  - `created_at` : Date de création

#### Vues (`views.py`)

- **`upload_view`** : Page d'upload de photos
- **`accept_photo`** : Traitement de l'image de carte d'identité
  - Upload vers Hadoop HDFS
  - Détection YOLOv5
  - Extraction OCR
  - Validation et stockage MongoDB

#### Module de Comparaison Faciale (`compare_face/`)

- **`views.py`** : Vues de comparaison faciale
  - **`compare_faces_page`** : Page de comparaison
  - **`compare_faces_with_images`** : API de comparaison
    - Détection de vivacité
    - Détection de clignement
    - Comparaison via CompreFace
    - Sauvegarde des résultats

#### Modèles ML (`ml_models/`)

- **`process_image.py`** : Fonctions de traitement d'image
  - **`process_image_with_yolo`** : Détection des zones avec YOLOv5
  - **`extract_text_from_crops`** : Extraction de texte avec PaddleOCR

### Fichiers Statiques (`static/`)

- **CSS** : Styles pour l'interface web
- **JavaScript** : Scripts frontend
- **Models** : Modèles ML (dlib shape predictor)

### Templates (`templates/`)

- **`upload.html`** : Interface d'upload de carte d'identité
- **`compare_faces.html`** : Interface de capture et comparaison faciale

## Fichiers de Configuration

### `requirements.txt`

Liste de toutes les dépendances Python nécessaires :
- Django 3.1.12
- djongo (connecteur MongoDB)
- PyTorch (pour YOLOv5)
- OpenCV (traitement d'images)
- PaddleOCR (OCR)
- dlib (détection faciale)
- Et autres dépendances...

### `.gitignore`

Fichiers et dossiers ignorés par Git :
- Environnements virtuels
- Fichiers Python compilés
- Fichiers de base de données
- Fichiers médias
- Fichiers temporaires
- Modèles ML (trop volumineux)

### `env.example`

Template de configuration avec toutes les variables d'environnement nécessaires.

## Fichiers de Documentation

- **`README.md`** : Documentation principale du projet
- **`ARCHITECTURE.md`** : Documentation technique de l'architecture
- **`CONTRIBUTING.md`** : Guide pour les contributeurs
- **`SETUP.md`** : Guide d'installation détaillé
- **`PROJECT_STRUCTURE.md`** : Ce fichier

## Fichiers à Créer/Configurer

### Modèles ML Requis

1. **dlib shape predictor**
   - Emplacement : `verify/static/models/shape_predictor_68_face_landmarks.dat`
   - Téléchargement : http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

2. **Modèle YOLOv5**
   - Emplacement : `verify/ml_models/yolo_training/exp_fixed/weights/best.pt`
   - À entraîner ou utiliser un modèle pré-entraîné

### Fichiers de Configuration

1. **`.env`** : Créer à partir de `env.example`
2. **`db.sqlite3`** : Créé automatiquement par Django (si utilisé)

## Organisation Recommandée pour le Développement

### Séparation des Préoccupations

- **`models.py`** : Définition des données
- **`views.py`** : Logique métier et endpoints API
- **`urls.py`** : Routage
- **`templates/`** : Présentation
- **`static/`** : Assets statiques
- **`ml_models/`** : Code de machine learning

### Bonnes Pratiques

1. **Ne pas commiter** :
   - Fichiers de modèles ML (trop volumineux)
   - Fichiers `.env` (contient des secrets)
   - Fichiers temporaires
   - Environnements virtuels

2. **Documenter** :
   - Toutes les fonctions importantes
   - Les changements majeurs
   - Les dépendances externes

3. **Tester** :
   - Ajouter des tests pour les nouvelles fonctionnalités
   - Vérifier la compatibilité avec les dépendances

## Notes Importantes

- Le dossier `CompreFace-master` dans `verify/compare_face/` ne devrait pas être dans le repository. CompreFace doit être installé séparément.
- Les fichiers temporaires `temp_target_*` doivent être nettoyés régulièrement.
- Les modèles ML doivent être stockés séparément (Git LFS ou service de stockage cloud).

