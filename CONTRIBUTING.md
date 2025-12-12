# Guide de Contribution

Merci de votre intérêt pour contribuer au projet de Vérification d'Identité ! Ce document fournit des directives pour contribuer au projet.

## Code de Conduite

En participant à ce projet, vous acceptez de respecter notre code de conduite. Soyez respectueux et professionnel dans toutes vos interactions.

## Comment Contribuer

### Signaler un Bug

Si vous trouvez un bug, veuillez créer une issue avec :

- **Titre clair et descriptif**
- **Description détaillée** du problème
- **Steps to reproduce** : Étapes pour reproduire le bug
- **Comportement attendu** : Ce qui devrait se passer
- **Comportement actuel** : Ce qui se passe réellement
- **Screenshots** : Si applicable
- **Environnement** : OS, version Python, version Django, etc.

### Proposer une Fonctionnalité

Pour proposer une nouvelle fonctionnalité :

1. Créez une issue avec le label `enhancement`
2. Décrivez clairement la fonctionnalité et son utilité
3. Expliquez comment elle s'intègre au projet
4. Attendez les retours avant de commencer à coder

### Soumettre une Pull Request

1. **Fork le projet**
   ```bash
   git clone https://github.com/votre-username/identity_verification.git
   cd identity_verification
   ```

2. **Créer une branche**
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   # ou
   git checkout -b fix/correction-bug
   ```

3. **Faire vos modifications**
   - Suivez les conventions de code (voir ci-dessous)
   - Ajoutez des tests si nécessaire
   - Mettez à jour la documentation

4. **Tester vos modifications**
   ```bash
   python manage.py test
   ```

5. **Commit vos changements**
   ```bash
   git add .
   git commit -m "Description claire de vos changements"
   ```
   
   **Conventions de commit** :
   - `feat:` Nouvelle fonctionnalité
   - `fix:` Correction de bug
   - `docs:` Documentation
   - `style:` Formatage, point-virgules manquants, etc.
   - `refactor:` Refactorisation du code
   - `test:` Ajout de tests
   - `chore:` Maintenance

6. **Push vers votre fork**
   ```bash
   git push origin feature/ma-nouvelle-fonctionnalite
   ```

7. **Créer une Pull Request**
   - Allez sur GitHub
   - Cliquez sur "New Pull Request"
   - Sélectionnez votre branche
   - Remplissez le template de PR
   - Attendez la revue de code

## Conventions de Code

### Python

- Suivez [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utilisez des noms de variables descriptifs
- Ajoutez des docstrings pour les fonctions et classes
- Limitez les lignes à 100 caractères maximum

**Exemple** :
```python
def extract_text_from_image(image_path: str) -> dict:
    """
    Extrait le texte d'une image de carte d'identité.
    
    Args:
        image_path: Chemin vers l'image à traiter
        
    Returns:
        Dictionnaire contenant les données extraites
    """
    # Code ici
    pass
```

### Django

- Suivez les conventions Django
- Utilisez les vues basées sur les classes quand c'est approprié
- Validez les données d'entrée
- Utilisez les migrations pour les changements de modèle

### Structure des Fichiers

- Un fichier par classe/fonction principale
- Organisez les imports : standard library, third-party, local
- Gardez les fichiers sous 500 lignes si possible

## Tests

### Écrire des Tests

- Ajoutez des tests pour toute nouvelle fonctionnalité
- Les tests doivent être indépendants et reproductibles
- Utilisez des noms de test descriptifs

**Exemple** :
```python
from django.test import TestCase
from verify.models import IdentityInfo

class IdentityInfoModelTest(TestCase):
    def test_create_identity_info(self):
        """Test la création d'un IdentityInfo"""
        identity = IdentityInfo.objects.create(
            id_number="12345678",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(identity.id_number, "12345678")
```

### Exécuter les Tests

```bash
# Tous les tests
python manage.py test

# Tests d'une app spécifique
python manage.py test verify

# Tests d'un fichier spécifique
python manage.py test verify.tests

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
```

## Documentation

### Code Documentation

- Ajoutez des docstrings à toutes les fonctions et classes
- Utilisez le format Google ou NumPy pour les docstrings
- Documentez les paramètres et valeurs de retour

### README et Documentation

- Mettez à jour le README si vous ajoutez des fonctionnalités
- Ajoutez des exemples d'utilisation
- Documentez les changements de configuration

## Review Process

1. **Automated Checks** : Votre PR doit passer tous les tests automatisés
2. **Code Review** : Au moins un mainteneur doit approuver
3. **Feedback** : Répondez aux commentaires et faites les modifications nécessaires
4. **Merge** : Une fois approuvé, votre PR sera mergé

## Questions ?

Si vous avez des questions, n'hésitez pas à :
- Ouvrir une issue avec le label `question`
- Contacter les mainteneurs
- Consulter la documentation existante

## Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

Merci de contribuer au projet ! 🎉

