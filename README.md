# Sporttipaivakirja
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* Käyttäjä pystyy lisäämään sovellukseen omia urheilusuorituksia / treenejään. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään treenejä / urheilusuorituksia
* Käyttäjä näkee sovelluksessa omat, sekä muiden lisäämät urheilusuoritukset 
* Käyttäjä pystyy etsimään urheilusuorituksia suorituksen vaativuuden tai lajin perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään, että muiden käyttäjien lisäämiä urheilusuorituksia
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän urheilusuoritukset ja mahdollistaa niiden poistamisen ja muokkaamisen.
* Käyttäjä pystyy luokittelemaan oman suorituksensa, lajin tai harjoituksen vaativuuden perusteella
* Käyttäjä pystyy reagoimaan muiden urheilusuorituksiin sovelluksessa kommentoimalla

## Sovelluksen asennus 

Kloonaa Git-repositorio

```
$ git clone https://github.com/ssampo-p/sporttipaivakirja.git
$ cd sporttipaivakirja
```




Asenna `flask`-kirjasto:

```
$ pip install flask
```

Sovellus luo käynnistyessään automaattisesti tietokannan nimeltä database.db

Voit käynnistää sovelluksen komennolla:

```
$ flask run
```
Paina Ctrl + C lopettaaksesi sovelluksen terminaalissa.


