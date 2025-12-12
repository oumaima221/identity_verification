# Guide de Nettoyage du Projet

Ce guide vous aidera à nettoyer votre projet avant de le pousser sur GitHub de manière professionnelle.

## Fichiers à Supprimer

### 1. Fichiers Temporaires

```bash
# Supprimer tous les fichiers temp_target_*
rm -f temp_target*

# Supprimer les dossiers temporaires
rm -rf temp_target_*
```

### 2. Environnements Virtuels

```bash
# Supprimer les environnements virtuels (ils sont dans .gitignore)
rm -rf venv/
rm -rf verify/venv/
rm -rf verify/compare_face/CompreFace-master/CompreFace-master/myenv/
```

### 3. Fichiers de Cache Python

```bash
# Supprimer __pycache__
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete
```

### 4. Fichiers de Base de Données Locaux

```bash
# Supprimer les bases de données SQLite
rm -f db.sqlite3
rm -f *.db
```

### 5. Fichiers de Build

```bash
# Supprimer les fichiers de build Python
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
```

### 6. Fichiers CompreFace (à supprimer du repo)

Le dossier `CompreFace-master` ne devrait pas être dans le repository. CompreFace doit être installé séparément.

```bash
# Supprimer CompreFace du repository (il sera dans .gitignore)
rm -rf verify/compare_face/CompreFace-master/
```

**Note :** CompreFace doit être installé séparément via Docker ou installation manuelle.

### 7. Fichiers de Logs

```bash
# Supprimer les fichiers de logs
rm -f *.log
rm -rf logs/
```

### 8. Fichiers de Fichiers Temporaires de Django

```bash
# Nettoyer les fichiers médias temporaires (si nécessaire)
rm -rf media/temp/*
```

## Script de Nettoyage Automatique

Créez un script `cleanup.sh` :

```bash
#!/bin/bash

echo "🧹 Nettoyage du projet..."

# Fichiers temporaires
echo "Suppression des fichiers temporaires..."
rm -f temp_target* 2>/dev/null

# Cache Python
echo "Suppression du cache Python..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Base de données
echo "Suppression des bases de données locales..."
rm -f db.sqlite3 *.db 2>/dev/null

# Build files
echo "Suppression des fichiers de build..."
rm -rf build/ dist/ *.egg-info/ 2>/dev/null

# Logs
echo "Suppression des logs..."
rm -f *.log 2>/dev/null

# CompreFace (garder seulement si nécessaire pour référence)
# rm -rf verify/compare_face/CompreFace-master/

echo "✅ Nettoyage terminé!"
```

Rendre le script exécutable :

```bash
chmod +x cleanup.sh
./cleanup.sh
```

## Vérification Avant le Commit

### 1. Vérifier les Fichiers à Commiter

```bash
git status
```

### 2. Vérifier que les Fichiers Sensibles sont Ignorés

```bash
# Vérifier .env
git check-ignore -v .env

# Vérifier les fichiers de modèles ML
git check-ignore -v verify/static/models/*.dat
git check-ignore -v verify/ml_models/**/*.pt
```

### 3. Vérifier la Taille des Fichiers

```bash
# Voir les plus gros fichiers
find . -type f -size +10M -not -path "./.git/*" -not -path "./venv/*"
```

### 4. Vérifier le .gitignore

Assurez-vous que `.gitignore` contient :

```
# Fichiers temporaires
temp_target*

# Environnements virtuels
venv/
verify/venv/
verify/compare_face/CompreFace-master/CompreFace-master/myenv/

# Cache Python
__pycache__/
*.pyc
*.pyo

# Base de données
*.sqlite3
*.db

# Fichiers sensibles
.env

# Modèles ML (trop volumineux)
*.pt
*.dat
*.h5
*.pkl

# CompreFace
verify/compare_face/CompreFace-master/
```

## Structure Recommandée pour GitHub

Votre repository GitHub devrait contenir :

```
✅ README.md
✅ ARCHITECTURE.md
✅ CONTRIBUTING.md
✅ SETUP.md
✅ DEPLOYMENT.md
✅ PROJECT_STRUCTURE.md
✅ LICENSE
✅ .gitignore
✅ requirements.txt
✅ env.example
✅ manage.py
✅ settings.py
✅ urls.py
✅ verify/ (code source)
❌ venv/ (ignoré)
❌ .env (ignoré)
❌ *.pt (modèles ML - ignorés)
❌ temp_target* (fichiers temporaires - ignorés)
❌ CompreFace-master/ (à installer séparément)
```

## Commandes Git Recommandées

### Premier Commit

```bash
# Initialiser Git (si pas déjà fait)
git init

# Ajouter tous les fichiers (respectant .gitignore)
git add .

# Vérifier ce qui sera commité
git status

# Commit initial
git commit -m "feat: Initial commit with professional project structure

- Add comprehensive README with installation guide
- Add architecture documentation
- Add contributing guidelines
- Add setup and deployment guides
- Configure Django settings with environment variables
- Add proper .gitignore for Python/Django project
- Organize project structure professionally"

# Ajouter le remote
git remote add origin https://github.com/yasmine-png/identity_verification.git

# Push vers GitHub
git branch -M main
git push -u origin main
```

### Commits Suivants

```bash
# Vérifier les changements
git status

# Ajouter les fichiers modifiés
git add .

# Commit avec message descriptif
git commit -m "type: Description du changement"

# Push
git push origin main
```

## Checklist Avant le Push

- [ ] Tous les fichiers temporaires supprimés
- [ ] Cache Python nettoyé
- [ ] Base de données locale supprimée
- [ ] .env non commité (vérifié avec git check-ignore)
- [ ] Modèles ML non commités (trop volumineux)
- [ ] CompreFace supprimé du repo (à installer séparément)
- [ ] .gitignore à jour
- [ ] README.md complet et professionnel
- [ ] Documentation à jour
- [ ] requirements.txt à jour
- [ ] Pas de secrets dans le code
- [ ] Structure du projet organisée

## Notes Importantes

1. **Ne jamais commiter** :
   - Fichiers `.env` avec des secrets
   - Modèles ML (utiliser Git LFS si nécessaire)
   - Fichiers de base de données
   - Environnements virtuels

2. **CompreFace** :
   - Ne doit pas être dans le repository
   - Doit être installé séparément
   - Ajouter des instructions dans README.md

3. **Modèles ML** :
   - Trop volumineux pour Git standard
   - Utiliser Git LFS ou un service de stockage cloud
   - Documenter où les télécharger dans README.md

## Après le Push

1. Vérifier que le repository GitHub est propre
2. Ajouter une description au repository
3. Ajouter des topics/tags appropriés
4. Configurer les paramètres du repository (branches protégées, etc.)
5. Créer des releases si nécessaire

---

**Résultat attendu** : Un repository GitHub professionnel, bien organisé, avec une documentation complète et un code propre ! 🚀

