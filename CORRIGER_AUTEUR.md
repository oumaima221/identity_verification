# Instructions pour corriger l'auteur des commits

Pour que tous les commits affichent **oumaima221** au lieu de **yasmine-png**, exécutez ces commandes dans l'ordre :

## 1. Configurer Git avec les bonnes informations

```bash
git config user.name "oumaima221"
git config user.email "oumaima221@users.noreply.github.com"
```

## 2. Changer l'auteur de tous les commits

```bash
git filter-branch -f --env-filter "
export GIT_AUTHOR_NAME='oumaima221'
export GIT_AUTHOR_EMAIL='oumaima221@users.noreply.github.com'
export GIT_COMMITTER_NAME='oumaima221'
export GIT_COMMITTER_EMAIL='oumaima221@users.noreply.github.com'
" --tag-name-filter cat -- --branches --tags
```

## 3. Vérifier que ça a fonctionné

```bash
git log --format="%h %an <%ae> %s" -5
```

Vous devriez voir **oumaima221** comme auteur de tous les commits.

## 4. Pousser vers GitHub

```bash
git push oumaima main:main --force
git push oumaima main:master --force
```

## Alternative (si filter-branch ne fonctionne pas)

Si la commande filter-branch prend trop de temps ou ne fonctionne pas, vous pouvez utiliser cette méthode :

```bash
# Pour chaque commit, utilisez :
git rebase -i HEAD~2
# Dans l'éditeur, changez "pick" en "edit" pour les commits à modifier
# Puis pour chaque commit :
git commit --amend --author="oumaima221 <oumaima221@users.noreply.github.com>" --no-edit
git rebase --continue
```

---

**Note importante :** Ces commandes réécrivent l'historique Git. Assurez-vous d'avoir une sauvegarde avant de les exécuter.

