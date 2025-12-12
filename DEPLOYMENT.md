# Guide de Déploiement

Ce guide explique comment déployer le système de vérification d'identité en production.

## Préparation pour GitHub

### 1. Nettoyer le Projet

Avant de pousser sur GitHub, assurez-vous de :

```bash
# Supprimer les fichiers temporaires
rm -rf temp_target_*
rm -rf verify/compare_face/CompreFace-master/CompreFace-master/myenv/
rm -rf verify/compare_face/CompreFace-master/CompreFace-master/__pycache__/

# Supprimer les fichiers de cache Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Supprimer les fichiers de base de données locaux
rm -f db.sqlite3

# Vérifier que .gitignore est à jour
```

### 2. Vérifier les Fichiers à Commiter

```bash
# Voir les fichiers qui seront ajoutés
git status

# Vérifier que les fichiers sensibles ne sont pas inclus
git check-ignore -v .env
```

### 3. Initialiser Git (si nécessaire)

```bash
git init
git add .
git commit -m "Initial commit: Professional project structure"
```

### 4. Ajouter le Remote GitHub

```bash
git remote add origin https://github.com/yasmine-png/identity_verification.git
git branch -M main
git push -u origin main
```

## Déploiement en Production

### Option 1 : Déploiement avec Docker

#### Créer un Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "identity_verification.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Créer docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles
    depends_on:
      - mongodb
      - compreface

  mongodb:
    image: mongo:4.4
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin
    volumes:
      - mongodb_data:/data/db

  compreface:
    image: exadel/compreface-api:latest
    ports:
      - "8001:8000"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=compreface

volumes:
  mongodb_data:
```

### Option 2 : Déploiement sur Serveur VPS

#### Prérequis Serveur

- Ubuntu 20.04+ ou similaire
- Python 3.8+
- Nginx
- Gunicorn
- MongoDB
- Supervisor (pour gérer les processus)

#### Étapes d'Installation

1. **Mettre à jour le système**

```bash
sudo apt update
sudo apt upgrade -y
```

2. **Installer Python et dépendances**

```bash
sudo apt install python3-pip python3-venv nginx supervisor -y
```

3. **Cloner le projet**

```bash
cd /var/www
sudo git clone https://github.com/yasmine-png/identity_verification.git
sudo chown -R $USER:$USER identity_verification
cd identity_verification
```

4. **Créer l'environnement virtuel**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

5. **Configurer les variables d'environnement**

```bash
cp env.example .env
nano .env
# Modifier les valeurs pour la production
```

6. **Configurer Gunicorn**

Créer `/etc/supervisor/conf.d/identity_verification.conf` :

```ini
[program:identity_verification]
command=/var/www/identity_verification/venv/bin/gunicorn identity_verification.wsgi:application --bind 127.0.0.1:8000
directory=/var/www/identity_verification
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/identity_verification.log
```

7. **Configurer Nginx**

Créer `/etc/nginx/sites-available/identity_verification` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location /static/ {
        alias /var/www/identity_verification/staticfiles/;
    }

    location /media/ {
        alias /var/www/identity_verification/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activer le site :

```bash
sudo ln -s /etc/nginx/sites-available/identity_verification /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

8. **Démarrer les services**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start identity_verification
```

### Option 3 : Déploiement sur Cloud (AWS, GCP, Azure)

#### AWS EC2

1. Lancer une instance EC2 (Ubuntu)
2. Configurer les groupes de sécurité (ports 80, 443, 22)
3. Suivre les étapes du déploiement VPS
4. Utiliser AWS RDS pour MongoDB (optionnel)
5. Utiliser S3 pour le stockage des fichiers (optionnel)

#### Heroku

1. Installer Heroku CLI
2. Créer un `Procfile` :

```
web: gunicorn identity_verification.wsgi:application
```

3. Déployer :

```bash
heroku create votre-app
git push heroku main
heroku run python manage.py migrate
```

## Configuration de Production

### Variables d'Environnement Critiques

```env
DEBUG=False
SECRET_KEY=clé-secrète-forte-et-aléatoire
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

### Sécurité

1. **HTTPS/SSL**
   - Utiliser Let's Encrypt pour un certificat SSL gratuit
   - Configurer Nginx pour rediriger HTTP vers HTTPS

2. **Firewall**
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

3. **Mises à jour**
   - Configurer les mises à jour automatiques
   - Surveiller les vulnérabilités

### Monitoring

1. **Logs**
   - Configurer la rotation des logs
   - Surveiller les erreurs

2. **Performance**
   - Utiliser un outil de monitoring (Sentry, New Relic)
   - Surveiller l'utilisation des ressources

## Sauvegarde

### Base de Données MongoDB

```bash
# Sauvegarde
mongodump --uri="mongodb://admin:admin@localhost:27017/identity_verification_db" --out=/backup/mongodb

# Restauration
mongorestore --uri="mongodb://admin:admin@localhost:27017/identity_verification_db" /backup/mongodb/identity_verification_db
```

### Fichiers Médias

```bash
# Sauvegarde
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Restauration
tar -xzf media_backup_YYYYMMDD.tar.gz
```

## Maintenance

### Mises à Jour

1. Mettre à jour le code :
   ```bash
   git pull origin main
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   sudo supervisorctl restart identity_verification
   ```

2. Mettre à jour les dépendances :
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

### Nettoyage

- Nettoyer les fichiers temporaires régulièrement
- Archiver les anciennes données
- Optimiser la base de données MongoDB

## Dépannage Production

### Vérifier les Logs

```bash
# Logs Gunicorn
sudo tail -f /var/log/identity_verification.log

# Logs Nginx
sudo tail -f /var/log/nginx/error.log

# Logs Supervisor
sudo supervisorctl tail -f identity_verification
```

### Redémarrer les Services

```bash
sudo supervisorctl restart identity_verification
sudo systemctl restart nginx
sudo systemctl restart mongod
```

## Checklist de Déploiement

- [ ] Variables d'environnement configurées
- [ ] DEBUG = False
- [ ] SECRET_KEY sécurisée
- [ ] ALLOWED_HOSTS configuré
- [ ] HTTPS/SSL configuré
- [ ] Base de données configurée
- [ ] Fichiers statiques collectés
- [ ] Migrations appliquées
- [ ] Firewall configuré
- [ ] Monitoring configuré
- [ ] Sauvegardes configurées
- [ ] Tests effectués

