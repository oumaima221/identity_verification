# 🆔 Système de Vérification d'Identité - Cartes Nationales Tunisiennes

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.1.12-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un système avancé et automatisé de traitement et de vérification d'identité pour les cartes nationales tunisiennes, utilisant la vision par ordinateur, l'apprentissage profond et la reconnaissance faciale pour garantir une vérification d'identité sécurisée et précise.

## 📋 Table des Matières

- [Aperçu du Projet](#aperçu-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture Technique](#architecture-technique)
- [Technologies Utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [API Endpoints](#api-endpoints)
- [Développement](#développement)
- [Contributions](#contributions)
- [License](#license)

## 🎯 Aperçu du Projet

Ce projet implémente un système complet de vérification d'identité automatisé qui combine :

- **Détection et extraction automatique de données** depuis les cartes d'identité tunisiennes
- **Reconnaissance faciale** pour comparer les photos d'identité avec des selfies en temps réel
- **Détection de vivacité (Liveness Detection)** pour prévenir les attaques par spoofing
- **Stockage distribué** avec Hadoop HDFS pour gérer de grands volumes de données
- **Base de données NoSQL** avec MongoDB pour un stockage flexible et scalable

### Problématique

La vérification d'identité fiable, rapide et sécurisée reste un défi critique pour de nombreuses organisations. Les vérifications manuelles sont souvent sujettes aux erreurs et à la fraude. Ce système automatise les processus de vérification d'identité en utilisant l'intelligence artificielle, réduisant ainsi les erreurs humaines et minimisant les activités frauduleuses.

### Cas d'Usage

- **Services bancaires en ligne** : Vérification d'identité pour l'ouverture de comptes
- **Services gouvernementaux** : Authentification pour les services numériques
- **Plateformes d'identité numérique** : Vérification KYC (Know Your Customer)
- **E-commerce** : Vérification d'identité pour les transactions sensibles

## ✨ Fonctionnalités

### 1. Extraction Automatique de Données

- ✅ Détection automatique des zones critiques (Nom, Prénom, Numéro CIN) via YOLOv5
- ✅ Reconnaissance de texte optimisée pour l'arabe et le latin avec PaddleOCR
- ✅ Validation des données extraites
- ✅ Détection des doublons dans la base de données

### 2. Vérification Faciale

- ✅ Capture de selfie en temps réel via webcam
- ✅ Détection de visage et d'yeux avec OpenCV
- ✅ Comparaison faciale via CompreFace API
- ✅ Score de similarité configurable (seuil par défaut: 0.88)

### 3. Détection de Vivacité (Anti-Spoofing)

- ✅ Détection de clignement d'yeux avec dlib (68 points de repère faciaux)
- ✅ Calcul du Eye Aspect Ratio (EAR) pour confirmer la vivacité
- ✅ Prévention des attaques par photo statique ou vidéo

### 4. Stockage et Gestion des Données

- ✅ Stockage MongoDB pour les données structurées
- ✅ Intégration Hadoop HDFS pour le stockage distribué des images
- ✅ Logs d'audit pour toutes les vérifications

## 🏗️ Architecture Technique

### Pipeline d'Extraction de Données

```
1. Upload de la carte d'identité
   ↓
2. Détection des zones (YOLOv5)
   ↓
3. Découpage des régions détectées
   ↓
4. Reconnaissance de texte (PaddleOCR)
   ↓
5. Validation et stockage (MongoDB)
   ↓
6. Stockage distribué (Hadoop HDFS)
```

### Pipeline de Vérification Faciale

```
1. Capture de selfie en temps réel
   ↓
2. Détection de visage et d'yeux (OpenCV)
   ↓
3. Vérification de vivacité (dlib - EAR)
   ↓
4. Encodage Base64 de l'image
   ↓
5. Comparaison faciale (CompreFace API)
   ↓
6. Décision de vérification (score ≥ 0.88)
   ↓
7. Sauvegarde des résultats (MongoDB)
```

## 🛠️ Technologies Utilisées

### Backend
- **Django 3.1.12** - Framework web Python
- **MongoDB** - Base de données NoSQL
- **djongo** - Connecteur Django-MongoDB

### Machine Learning & Computer Vision
- **YOLOv5** - Détection d'objets pour localiser les champs sur la carte
- **PaddleOCR** - OCR optimisé pour l'arabe et le latin
- **OpenCV** - Traitement d'images et détection de visage
- **dlib** - Prédicteur de points de repère faciaux (68 points)

### Reconnaissance Faciale
- **CompreFace** - API open-source de reconnaissance faciale

### Big Data
- **Hadoop HDFS** - Système de fichiers distribué pour le stockage

### Autres
- **Python 3.8+** - Langage de programmation principal
- **Docker** - Conteneurisation (optionnel)

## 📦 Prérequis

- Python 3.8 ou supérieur
- MongoDB 4.4 ou supérieur
- Hadoop HDFS (optionnel, pour le stockage distribué)
- CompreFace API (service de reconnaissance faciale)
- Modèle YOLOv5 entraîné (fichier `.pt`)
- Modèle dlib shape predictor (`shape_predictor_68_face_landmarks.dat`)

## 🚀 Installation

### 1. Cloner le Repository

```bash
git clone https://github.com/oumaima221/identity_verification.git
cd identity_verification
```

### 2. Créer un Environnement Virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer MongoDB

Assurez-vous que MongoDB est installé et en cours d'exécution :

```bash
# Sur Linux/Mac
sudo systemctl start mongod

# Vérifier la connexion
mongo --eval "db.version()"
```

### 5. Configurer CompreFace

Suivez les instructions de [CompreFace](https://github.com/exadel-inc/CompreFace) pour installer et démarrer le service.

### 6. Configurer les Modèles

Placez les fichiers de modèles dans les emplacements appropriés :

#### Modèle YOLOv5

Le projet utilise YOLOv5 pour la détection des zones sur les cartes d'identité. Vous avez deux options :

**Option A : Utiliser un modèle pré-entraîné (pour tester)**
- Téléchargez un modèle pré-entraîné depuis [Ultralytics YOLOv5 Releases](https://github.com/ultralytics/yolov5/releases)
- Modèles disponibles : `yolov5s.pt`, `yolov5m.pt`, `yolov5l.pt`, `yolov5x.pt`
- Placez le fichier dans : `verify/ml_models/yolo_training/exp_fixed/weights/best.pt`

**Option B : Utiliser votre modèle personnalisé (recommandé)**
- Si vous avez entraîné un modèle personnalisé sur des cartes d'identité tunisiennes
- Placez votre fichier `best.pt` dans : `verify/ml_models/yolo_training/exp_fixed/weights/best.pt`

**Repository YOLOv5 :** [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)

**Documentation YOLOv5 :** [https://docs.ultralytics.com/yolov5/](https://docs.ultralytics.com/yolov5/)

#### Modèle dlib (Shape Predictor)

- Téléchargez le fichier depuis [dlib.net](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
- Décompressez-le et placez-le dans : `verify/static/models/shape_predictor_68_face_landmarks.dat`

```bash
# Créer le dossier si nécessaire
mkdir -p verify/static/models

# Télécharger et décompresser (Linux/Mac)
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
mv shape_predictor_68_face_landmarks.dat verify/static/models/
```

### 7. Configurer les Variables d'Environnement

Copiez `.env.example` vers `.env` et configurez les variables :

```bash
cp .env.example .env
```

Éditez `.env` avec vos configurations.

### 8. Appliquer les Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Créer un Superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 10. Lancer le Serveur de Développement

```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

## ⚙️ Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=identity_verification_db
MONGODB_USER=admin
MONGODB_PASSWORD=admin

# CompreFace API
COMPREFACE_SERVER_URL=http://localhost:8000
COMPREFACE_DETECTION_API_KEY=your-detection-api-key
COMPREFACE_RECOGNITION_API_KEY=your-recognition-api-key
COMPREFACE_VERIFICATION_API_KEY=your-verification-api-key
COMPREFACE_VERIFICATION_THRESHOLD=0.88

# Hadoop HDFS (optionnel)
HADOOP_BIN_PATH=/home/hadoop/hadoop/bin/hdfs
HADOOP_CONF_DIR=/home/hadoop/hadoop/etc/hadoop
HDFS_TARGET_DIR=/ids

# Chemins des modèles
YOLO_MODEL_PATH=verify/ml_models/yolo_training/exp_fixed/weights/best.pt
DLIB_MODEL_PATH=verify/static/models/shape_predictor_68_face_landmarks.dat
```

### Configuration Django

Les paramètres principaux sont dans `settings.py`. Assurez-vous de :

1. Configurer `BASE_DIR` correctement
2. Définir `SECRET_KEY` (utilisez une variable d'environnement en production)
3. Configurer `ALLOWED_HOSTS` pour la production
4. Configurer les chemins des fichiers statiques et médias

## 📖 Utilisation

### Interface Web

1. Accédez à `http://localhost:8000`
2. Uploadez une image de carte d'identité tunisienne
3. Le système extrait automatiquement les données
4. Capturez un selfie en temps réel
5. Le système compare les visages et affiche le résultat

### API Endpoints

Voir la section [API Endpoints](#api-endpoints) pour plus de détails.

## 📁 Structure du Projet

```
identity_verification/
├── identity_verification/          # Configuration Django principale
│   ├── __init__.py
│   ├── settings.py                 # Paramètres Django
│   ├── urls.py                     # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── verify/                         # Application principale
│   ├── __init__.py
│   ├── models.py                   # Modèles MongoDB
│   ├── views.py                    # Vues principales
│   ├── urls.py                     # URLs de l'application
│   ├── compare_face/               # Module de comparaison faciale
│   │   ├── views.py
│   │   └── urls.py
│   ├── ml_models/                  # Modèles ML (à créer)
│   │   └── process_image.py        # Traitement YOLOv5 et OCR
│   ├── static/                     # Fichiers statiques
│   │   └── models/                 # Modèles ML (dlib, etc.)
│   └── templates/                  # Templates HTML
│       ├── verify/
│       │   ├── upload.html
│       │   └── compare_faces.html
├── media/                          # Fichiers uploadés (ignoré par git)
│   └── temp/                       # Fichiers temporaires
├── manage.py
├── requirements.txt                # Dépendances Python
├── .env.example                    # Exemple de configuration
├── .gitignore
├── README.md                       # Ce fichier
├── ARCHITECTURE.md                 # Documentation d'architecture
└── CONTRIBUTING.md                 # Guide de contribution
```

## 🔌 API Endpoints

### 1. Upload de Carte d'Identité

**POST** `/accept-photo/`

Upload et traitement d'une image de carte d'identité.

**Request:**
- `photo`: Fichier image (multipart/form-data)

**Response:**
```json
{
  "status": "success",
  "message": "Photo processed and data saved.",
  "first_name": "Prénom",
  "last_name": "Nom",
  "id_number": "12345678",
  "person_exists": true
}
```

### 2. Comparaison Faciale

**POST** `/compare_face/verify-live-face/`

Comparaison d'un selfie avec la photo d'identité.

**Request:**
- `target_image`: Fichier image du selfie (multipart/form-data)

**Response:**
```json
{
  "status": "success",
  "data": {
    "liveness_passed": true,
    "eyes_closed": false,
    "blink_count": 0,
    "bounding_boxes": [...],
    "verified": true,
    "confidence": 0.92,
    "message": "Faces match"
  }
}
```

## 🔧 Développement

### Exécuter les Tests

```bash
python manage.py test
```

### Linting

```bash
# Installer pylint
pip install pylint

# Linter le code
pylint verify/
```

### Formatage du Code

```bash
# Installer black
pip install black

# Formater le code
black verify/
```

## 🤝 Contributions

Les contributions sont les bienvenues ! Veuillez lire [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails sur notre code de conduite et le processus de soumission de pull requests.

### Processus de Contribution

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Oumaima** - *Développement initial* - [oumaima221](https://github.com/oumaima221)
- **Yasmine** - *Développement initial* - [yasmine-png](https://github.com/yasmine-png)

## 🙏 Remerciements

- [YOLOv5](https://github.com/ultralytics/yolov5) - Détection d'objets pour localiser les champs sur les cartes d'identité
  - Repository : [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)
  - Documentation : [https://docs.ultralytics.com/yolov5/](https://docs.ultralytics.com/yolov5/)
  - Modèles pré-entraînés : [Releases](https://github.com/ultralytics/yolov5/releases)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - Reconnaissance de texte optimisée pour l'arabe et le latin
- [CompreFace](https://github.com/exadel-inc/CompreFace) - API open-source de reconnaissance faciale
- [dlib](http://dlib.net/) - Bibliothèque de détection de points de repère faciaux (68 points)

## 📞 Support

Pour toute question ou problème, veuillez ouvrir une [issue](https://github.com/oumaima221/identity_verification/issues) sur GitHub.

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !
