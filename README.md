# Sporttipaivakirja
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* Käyttäjä pystyy lisäämään sovellukseen omia urheilusuorituksia / treenejään. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään treenejä / urheilusuorituksia
* Käyttäjä näkee sovelluksessa omat, sekä muiden lisäämät urheilusuoritukset. Myös ilman käyttäjää voi tarkastella urheilusuorituksia.
* Käyttäjä pystyy etsimään urheilusuorituksia suorituksen vaativuuden tai lajin perusteella. Myös hakusanalla hakeminen toimii. Hakusanaa verrataan suoritusten lajeihin ja treenien tasoon.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän urheilusuoritusten määrän viimeisen 7 ja 30 päivän ajalta, listaa kaikki suoritukset sekä mahdollistaa suoritusten muokkaamisen ja poistamisen.
* Käyttäjä pystyy luokittelemaan oman suorituksensa, lajin tai harjoituksen vaativuuden perusteella
* Käyttäjä pystyy reagoimaan muiden urheilusuorituksiin sovelluksessa kommentoimalla

## Sovelluksen asennus 

Kloonaa Git-repositorio

```
$ git clone https://github.com/ssampo-p/sporttipaivakirja.git
$ cd sporttipaivakirja/sovellus/app
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


