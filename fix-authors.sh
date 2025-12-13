#!/bin/bash
git filter-branch -f --env-filter '
OLD_EMAIL="yboukraiem@gmail.com"
CORRECT_NAME="oumaima221"
CORRECT_EMAIL="oumaima221@users.noreply.github.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ] || [ "$GIT_AUTHOR_NAME" = "yasmine-png" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

