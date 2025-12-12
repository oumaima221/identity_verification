# Architecture du Système de Vérification d'Identité

## Vue d'Ensemble

Ce document décrit l'architecture technique du système de vérification d'identité pour les cartes nationales tunisiennes. Le système est conçu pour être modulaire, scalable et sécurisé.

## Architecture Générale

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Web)                          │
│  - Upload de carte d'identité                                │
│  - Capture de selfie en temps réel                           │
│  - Affichage des résultats                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Django Backend                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Views      │  │   Models     │  │   URLs       │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
│  ┌──────▼─────────────────▼──────────────────▼───────┐      │
│  │         Application Logic Layer                    │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   YOLOv5     │ │  PaddleOCR   │ │  CompreFace  │
│  Detection   │ │  Text Extract│ │ Face Compare │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │
       └────────────────┼─────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   MongoDB    │ │  Hadoop HDFS │ │   OpenCV     │
│   Database   │ │  File Storage│ │  dlib (EAR)  │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Composants Principaux

### 1. Backend Django

#### Structure des Applications

- **`identity_verification/`** : Configuration principale du projet Django
  - `settings.py` : Configuration de l'application
  - `urls.py` : Routage principal
  - `wsgi.py` : Interface WSGI pour le déploiement

- **`verify/`** : Application principale de vérification
  - `models.py` : Modèles de données MongoDB
  - `views.py` : Logique métier et endpoints API
  - `urls.py` : Routage de l'application
  - `compare_face/` : Module de comparaison faciale
  - `ml_models/` : Modèles de machine learning

#### Flux de Données

##### Pipeline d'Extraction de Données

1. **Upload de l'Image**
   - L'utilisateur upload une image de carte d'identité
   - Validation du format et de la taille
   - Sauvegarde temporaire dans `media/temp/`

2. **Détection des Zones (YOLOv5)**
   - Le modèle YOLOv5 détecte les zones critiques :
     - Nom (name)
     - Prénom (prenom)
     - Numéro CIN (id)
     - Photo d'identité (photo)
   - Retourne les coordonnées des bounding boxes

3. **Découpage des Régions**
   - Chaque zone détectée est découpée en image séparée
   - Les images sont sauvegardées dans un dossier temporaire

4. **Reconnaissance de Texte (PaddleOCR)**
   - PaddleOCR traite chaque image découpée
   - Extraction du texte avec support arabe/latin
   - Nettoyage et validation des données extraites

5. **Validation et Stockage**
   - Vérification de l'existence dans MongoDB
   - Sauvegarde des données extraites
   - Upload vers Hadoop HDFS (optionnel)

##### Pipeline de Vérification Faciale

1. **Capture du Selfie**
   - L'utilisateur capture un selfie via webcam
   - Validation de l'image

2. **Détection de Vivacité**
   - **OpenCV** : Détection de visage et d'yeux avec Haar Cascades
   - **dlib** : Détection de 68 points de repère faciaux
   - **Calcul EAR** : Eye Aspect Ratio pour détecter les clignements
   - Vérification que le visage est réel (anti-spoofing)

3. **Encodage de l'Image**
   - Conversion de l'image en Base64
   - Préparation pour l'API CompreFace

4. **Comparaison Faciale**
   - Envoi de la photo d'identité et du selfie à CompreFace
   - Calcul du score de similarité
   - Décision de vérification (seuil : 0.88)

5. **Sauvegarde des Résultats**
   - Stockage du résultat dans MongoDB
   - Logs d'audit pour traçabilité

### 2. Modèles de Machine Learning

#### YOLOv5

- **Rôle** : Détection d'objets pour localiser les champs sur la carte
- **Entraînement** : Modèle personnalisé entraîné sur des cartes tunisiennes
- **Classes détectées** :
  - `name` : Nom de famille
  - `prenom` : Prénom
  - `id` : Numéro CIN
  - `photo` : Photo d'identité

#### PaddleOCR

- **Rôle** : Reconnaissance de texte (OCR)
- **Spécificités** :
  - Support de l'arabe et du latin
  - Optimisé pour les textes courbés et déformés
  - Traitement des images de qualité variable

#### dlib

- **Rôle** : Détection de points de repère faciaux
- **Fonctionnalité** : Calcul du Eye Aspect Ratio (EAR)
- **Formule EAR** :
  ```
  EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
  ```
  où p1-p6 sont les points de repère de l'œil

### 3. Base de Données

#### MongoDB

**Collection : `identityinfo`**

Structure des documents :
```json
{
  "_id": ObjectId("..."),
  "photo_name": "string",
  "id_number": "string",
  "first_name": "string",
  "last_name": "string",
  "created_at": ISODate("..."),
  "photo": Binary("...")  // Photo d'identité encodée
}
```

**Index** :
- `id_number` : Index unique pour éviter les doublons

#### Hadoop HDFS

- **Rôle** : Stockage distribué des images brutes
- **Avantages** :
  - Scalabilité horizontale
  - Tolérance aux pannes
  - Réplication automatique

### 4. Services Externes

#### CompreFace API

- **Rôle** : Service de reconnaissance faciale
- **Endpoints utilisés** :
  - `/api/v1/detection/detect` : Détection de visages
  - `/api/v1/recognition/recognize` : Reconnaissance faciale
  - `/api/v1/verification/verify` : Comparaison de deux visages

**Configuration** :
- URL du serveur : Configurable via variables d'environnement
- Clés API : Séparées par service (détection, reconnaissance, vérification)
- Seuil de vérification : 0.88 (configurable)

## Sécurité

### Mesures de Sécurité Implémentées

1. **Validation des Fichiers**
   - Vérification des extensions autorisées
   - Limitation de la taille des fichiers
   - Validation du contenu des images

2. **Détection de Vivacité**
   - Prévention des attaques par photo statique
   - Détection de clignement d'yeux
   - Vérification de la présence d'un visage réel

3. **Protection CSRF**
   - Tokens CSRF pour les requêtes POST
   - Validation côté serveur

4. **Gestion des Secrets**
   - Variables d'environnement pour les clés API
   - Exclusion des fichiers sensibles du contrôle de version

5. **Logs d'Audit**
   - Enregistrement de toutes les vérifications
   - Traçabilité des actions utilisateurs

## Scalabilité

### Optimisations Actuelles

- Utilisation de MongoDB pour un stockage flexible
- Stockage distribué avec Hadoop HDFS
- Traitement asynchrone des images (à implémenter)

### Améliorations Futures

- Mise en cache des résultats de vérification
- Traitement par lots (batch processing)
- Mise en queue avec Celery pour les tâches longues
- Load balancing pour le backend Django
- CDN pour les fichiers statiques

## Déploiement

### Environnement de Développement

- Django development server
- MongoDB local
- CompreFace en Docker

### Environnement de Production

- Gunicorn/uWSGI pour Django
- Nginx comme reverse proxy
- MongoDB cluster
- Hadoop HDFS cluster
- CompreFace en cluster
- SSL/TLS pour les communications sécurisées

## Monitoring et Logging

### Logs

- Logs Django pour les erreurs
- Logs MongoDB pour les requêtes
- Logs d'audit pour les vérifications

### Métriques à Surveiller

- Temps de traitement des images
- Taux de réussite des vérifications
- Utilisation des ressources (CPU, mémoire)
- Latence des API externes
- Taille de la base de données

## Diagrammes de Séquence

### Flux d'Extraction de Données

```
User → Django → YOLOv5 → Crop Images → PaddleOCR → Validate → MongoDB → HDFS
```

### Flux de Vérification Faciale

```
User → Django → OpenCV/dlib → Liveness Check → CompreFace → Compare → MongoDB
```

## Conclusion

Cette architecture modulaire permet une maintenance facile, une scalabilité horizontale et une sécurité renforcée. Chaque composant peut être amélioré ou remplacé indépendamment sans affecter l'ensemble du système.

