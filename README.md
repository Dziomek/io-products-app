# io-products-app

## venv

Po zaciągnięciu projektu tworzymy venv z poziomu folderu z projektem (robimy to tylko raz):
- pip install virtualenv
- virtualenv venv

Po stworzeniu venv wchodzimy do Windowsowego cmd (z poziomu PyCharma w terminalu raczej nie zadziała) i wchodzimy do folderu z projektem.
Z poziomu folderu z projektem:
- venv\Scripts\activate

Po pokazaniu się przy ścieżce po lewej stronie napisu (venv) oznaczającego, że aktywowaliśmy venv instalujemy requirementsy:
- pip install -r requirements.txt

Po zainstalowaniu wybieramy interpreter w PyCharmie:
- add interpreter, następnie existing environment

Jeśli wybralismy interpreter możemy startować serwer Flaska.

## start Flaska
 run znajduje się w __init__.py.

## start Reacta

Z poziomu folderu z Reactem: 
- npm install - zaciąga potrzebne moduły
- npm start - startuje serwer Reacta
