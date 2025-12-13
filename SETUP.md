# Guide d'Installation et de Configuration

Ce guide vous aidera à installer et configurer le système de vérification d'identité sur votre machine locale.

## Prérequis Système

### Logiciels Requis

1. **Python 3.8 ou supérieur**
   ```bash
   python --version
   # ou
   python3 --version
   ```

2. **MongoDB 4.4 ou supérieur**
   - [Télécharger MongoDB](https://www.mongodb.com/try/download/community)
   - Installation et démarrage :
     ```bash
     # Linux
     sudo systemctl start mongod
     
     # macOS (avec Homebrew)
     brew services start mongodb-community
     
     # Windows
     # Utiliser MongoDB Compass ou le service Windows
     ```

3. **Git** (pour cloner le repository)
   ```bash
   git --version
   ```

### Services Optionnels

- **Hadoop HDFS** : Pour le stockage distribué (optionnel)
- **CompreFace** : Service de reconnaissance faciale (peut être lancé via Docker)

## Installation Étape par Étape

### 1. Cloner le Repository

```bash
git clone https://github.com/oumaima221/identity_verification.git
cd identity_verification
```

### 2. Créer un Environnement Virtuel

**Linux/macOS :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les Dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note :** L'installation peut prendre plusieurs minutes car elle inclut PyTorch, OpenCV, et d'autres bibliothèques lourdes.

### 4. Configurer les Variables d'Environnement

Copiez le fichier d'exemple et modifiez-le :

```bash
# Linux/macOS
cp env.example .env

# Windows
copy env.example .env
```

Éditez le fichier `.env` avec vos configurations :

```env
SECRET_KEY=votre-clé-secrète-générée
DEBUG=True
MONGODB_HOST=localhost
MONGODB_PORT=27017
# ... autres configurations
```

**Générer une SECRET_KEY :**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 5. Configurer MongoDB

#### Créer un Utilisateur Admin (si nécessaire)

```bash
mongo
```

Dans le shell MongoDB :
```javascript
use admin
db.createUser({
  user: "admin",
  pwd: "admin",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
})
```

#### Créer la Base de Données

```javascript
use identity_verification_db
db.createCollection("identityinfo")
```

### 6. Télécharger les Modèles ML

#### Modèle dlib (Shape Predictor)

1. Téléchargez le fichier depuis [dlib.net](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
2. Décompressez-le
3. Placez-le dans : `verify/static/models/shape_predictor_68_face_landmarks.dat`

```bash
mkdir -p verify/static/models
# Téléchargez et placez le fichier dans ce dossier
```

#### Modèle YOLOv5

1. Entraînez votre modèle YOLOv5 ou utilisez un modèle pré-entraîné
2. Placez le fichier `.pt` dans : `verify/ml_models/yolo_training/exp_fixed/weights/best.pt`

```bash
mkdir -p verify/ml_models/yolo_training/exp_fixed/weights
# Placez votre modèle best.pt dans ce dossier
```

### 7. Configurer CompreFace (Optionnel mais Recommandé)

#### Option A : Docker (Recommandé)

```bash
cd verify/compare_face
docker-compose up -d
```

#### Option B : Installation Manuelle

Suivez les instructions sur [CompreFace GitHub](https://github.com/exadel-inc/CompreFace)

**Configuration des Clés API :**

1. Accédez à l'interface CompreFace (généralement `http://localhost:8000`)
2. Créez une application
3. Générez les clés API pour :
   - Detection
   - Recognition
   - Verification
4. Ajoutez ces clés dans votre fichier `.env`

### 8. Appliquer les Migrations Django

```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Créer un Superutilisateur (Optionnel)

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte administrateur.

### 10. Collecter les Fichiers Statiques

```bash
python manage.py collectstatic --noinput
```

### 11. Lancer le Serveur de Développement

```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

## Vérification de l'Installation

### Tester la Connexion MongoDB

```bash
python verify/check_mongo.py
```

### Tester l'API

1. Accédez à `http://localhost:8000`
2. Uploadez une image de carte d'identité
3. Vérifiez que les données sont extraites correctement

## Configuration Hadoop HDFS (Optionnel)

Si vous souhaitez utiliser Hadoop HDFS pour le stockage distribué :

### 1. Installer Hadoop

Suivez le [guide d'installation Hadoop](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)

### 2. Configurer les Chemins

Dans votre fichier `.env` :
```env
HADOOP_BIN_PATH=/chemin/vers/hadoop/bin/hdfs
HADOOP_CONF_DIR=/chemin/vers/hadoop/etc/hadoop
HDFS_TARGET_DIR=/ids
```

### 3. Tester la Connexion

```bash
hdfs dfs -ls /
```

## Dépannage

### Problème : MongoDB ne démarre pas

**Linux :**
```bash
sudo systemctl status mongod
sudo systemctl start mongod
```

**Vérifier les logs :**
```bash
sudo tail -f /var/log/mongodb/mongod.log
```

### Problème : Erreur d'import de modules

Assurez-vous que l'environnement virtuel est activé et que toutes les dépendances sont installées :

```bash
pip install -r requirements.txt --force-reinstall
```

### Problème : Modèles ML introuvables

Vérifiez que les fichiers de modèles sont aux bons emplacements :

```bash
# Vérifier dlib
ls -la verify/static/models/shape_predictor_68_face_landmarks.dat

# Vérifier YOLOv5
ls -la verify/ml_models/yolo_training/exp_fixed/weights/best.pt
```

### Problème : CompreFace ne répond pas

1. Vérifiez que le service est démarré :
   ```bash
   docker ps  # Si utilisé avec Docker
   ```

2. Vérifiez l'URL dans `.env` :
   ```env
   COMPREFACE_SERVER_URL=http://localhost:8000
   ```

3. Testez l'API :
   ```bash
   curl http://localhost:8000/api/v1/status
   ```

### Problème : Erreurs de permissions

**Linux/macOS :**
```bash
chmod +x manage.py
sudo chown -R $USER:$USER .
```

## Structure des Dossiers Requis

Assurez-vous que ces dossiers existent :

```
identity_verification/
├── verify/
│   ├── static/
│   │   └── models/          # Modèles dlib
│   ├── ml_models/
│   │   └── yolo_training/
│   │       └── exp_fixed/
│   │           └── weights/  # Modèle YOLOv5
│   └── templates/
│       └── verify/           # Templates HTML
├── media/
│   └── temp/                 # Fichiers temporaires
└── staticfiles/              # Fichiers statiques collectés
```

Créez les dossiers manquants :

```bash
mkdir -p verify/static/models
mkdir -p verify/ml_models/yolo_training/exp_fixed/weights
mkdir -p verify/templates/verify
mkdir -p media/temp
```

## Prochaines Étapes

Une fois l'installation terminée :

1. Consultez le [README.md](README.md) pour comprendre le fonctionnement
2. Lisez [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre l'architecture
3. Consultez [CONTRIBUTING.md](CONTRIBUTING.md) si vous souhaitez contribuer

## Support

Pour toute question ou problème :
- Ouvrez une [issue](https://github.com/oumaima221/identity_verification/issues) sur GitHub
- Consultez la documentation dans le dossier `docs/`

