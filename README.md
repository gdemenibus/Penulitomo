# Penultimo
The objective of this bot is to handle role assignment as a reaction to
certain words. 
A generic implementation is provided, with an editable config file that can be
loaded.
A yaml file is used for config

## To DO:
- [X] Implement basic logic (Reaction to words and emojis)
- [ ] Abstract away what is being reacted to (Reaction files can be changed)
- [ ] Refactor code to be more legible and extendible
- [ ] Implement a config file

## Commands for Development:
Code formating:
```
pipenv run black
pipenv run isort
```
Style Enforcement:
```
pipenv run flake8
```
Testing:
```
pipenv run pytest --cov
```


