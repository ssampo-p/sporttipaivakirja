# Sporttipaivakirja
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* Käyttäjä pystyy lisäämään sovellukseen omia urheilusuorituksia / treenejään. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään treenejä / urheilusuorituksia
* Käyttäjä näkee sovelluksessa omat, sekä muiden lisäämät urheilusuoritukset. Myös ilman käyttäjää voi tarkastella urheilusuorituksia.
* Käyttäjä pystyy etsimään urheilusuorituksia suorituksen vaativuuden tai lajin perusteella. Myös hakusanalla hakeminen toimii. Hakusanaa verrataan suoritusten lajeihin ja treenien tasoon.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän urheilusuoritusten määrän viimeisen 7 ja 30 päivän ajalta, listaa kaikki suoritukset sekä mahdollistaa suoritusten muokkaamisen ja poistamisen.
* Käyttäjä pystyy luokittelemaan oman suorituksensa, lajin tai harjoituksen vaativuuden perusteella
* Käyttäjä pystyy reagoimaan muiden urheilusuorituksiin sovelluksessa kommentoimalla ja tarvittaessa poistamaan omat kommenttinsa

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

## Toiminta suurella tietomäärällä
- testidatan määrä
```
user_count = 1000
workout_count = 10**5
comment_count = 10**6
```
- Kokeillaan käyttäjän sivulle menemistä->
```
elapsed time: 5.8 s
127.0.0.1 - - [12/Dec/2025 13:12:57] "GET /user_page/2 HTTP/1.1" 200 -
```

- Tässä haun nopeuden esimerkki kun ladataan "workouts" sivu -->
```
elapsed time: 0.32 s
127.0.0.1 - - [12/Dec/2025 12:15:38] "GET /workouts/1 HTTP/1.1" 200 -
```
- Esimerkki: kokeillaan eri hakuja ja ladataan tulokset -->
```
elapsed time: 0.26 s
127.0.0.1 - - [12/Dec/2025 12:33:45] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Jääkiekko HTTP/1.1" 200 -

elapsed time: 0.52 s
127.0.0.1 - - [12/Dec/2025 12:27:29] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Kuntosali HTTP/1.1" 200 -

elapsed time: 0.26 s
127.0.0.1 - - [12/Dec/2025 12:34:33] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Pyöräily HTTP/1.1" 200 -

elapsed time: 0.46 s
127.0.0.1 - - [12/Dec/2025 12:35:03] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Padel HTTP/1.1" 200 -
```
#### Huomaamme, että sovellus toimii hitaasti jos käyttäjän omalle sivulle mennään, myös "kaikki urheilusuoritukset" sivulla viivettä alkaa esiintyä latauksissa
- Lisää dataa ->  
```
Määrät nyt:

workout_count = 10**6
comment_count = 10**7
```
-  Datan lisäämisen jälkeen, latausajat alkavat jo olla todella hitaita ->
```
elapsed time: 3.19 s
127.0.0.1 - - [12/Dec/2025 12:43:42] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Jääkiekko HTTP/1.1" 200 -

elapsed time: 4.58 s
127.0.0.1 - - [12/Dec/2025 12:44:15] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Lentopallo HTTP/1.1" 200 -
```
- Tällä määrällä dataa, käyttäjäsivun lataaminen alkaa käydä jo tuskalliseksi (Testissä latasin sivua minuutin ilman tuloksia)

#### Luodaan indeksejä
```
db.execute("CREATE INDEX idx_workouts ON workouts (sent_at DESC)")             
db.execute("CREATE INDEX idx_workouts_sort ON workouts (sport, sent_at DESC)") 
db.execute("CREATE INDEX idx_comments ON comments (workout_id, sent_at DESC)") 
```

- näillä tietokannan indeksöinneillä toiminta nopeutui huomattavasti
```
elapsed time: 0.04 s
127.0.0.1 - - [12/Dec/2025 14:23:36] "GET /workouts/1 HTTP/1.1" 200 -

elapsed time: 0.01 s
127.0.0.1 - - [12/Dec/2025 14:24:09] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Jääkiekko HTTP/1.1" 200 -

elapsed time: 0.01 s
127.0.0.1 - - [12/Dec/2025 14:24:23] "GET /workouts/sort_workouts/?workout_level=all&workout_type=Tennis HTTP/1.1" 200 -
```
- Myös ilman, että käyttäjäsivut sisältävät sivutusta, niin käyttäjäsivun pystyy nyt lataamaan kohtuullisessa ajassa, vaikka dataa onkin paljon
```
elapsed time: 0.86 s
127.0.0.1 - - [12/Dec/2025 14:24:40] "GET /user_page/1 HTTP/1.1" 200 -
```
#### Parannettavaa kuitenkin löytyy. Sovelluksen kehittämisellä ja tietokannan optimoimisella olisi sovelluksesta mahdollista saada vieläkin nopeampi. 