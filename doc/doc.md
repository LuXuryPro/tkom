# TKOM - Projekt - dokumentacja końcowa
Wykonał:
Radosław Załuska

# Treść zadania
>Celem zadania jest analiza składniowa komunikacji protokołu HTTP zapisanej w
>plikach tekstowych (wczytywanie z plików pcap byłoby dodatkowym atutem) i
>możliwość wyszukiwania interesujących komunikacji, z wykorzystaniem
>zaproponowanego prostego języka wyszukiwania. Przykładowe interesujące
>połączenia protokołu HTTP przedstawione jest poniżej. Jest ono charakteryzowane
>między innymi: metodą POST, URL-em zawierającym podciąg phsys.php oraz
>wysłanymi danymi postaci "data=xxx", gdzie xxx to liczby szesnastkowe.


## Opis zakładanej funkcjonalności
Program będzie umożliwiał filtrowanie zadanego zestawu zapytań HTTP za pomocą
prostego języka filtrowania. W filtrze będzie można wybrać jakie pola z
zapytania wyświetlić oraz na jakiej podstawie filtrować.

## Gramatyka
### HTTP Request
```bnf
Slash       ::= "/"
NewLine     ::= "CRLF"
Signature   ::= "HTTP"
Colon       ::= ":"
Dot         ::= "."
Char        ::= "A-Za-z0-9!@#$%^&*()_-+="
String      ::= Char*
Digit       ::= "0-9"

HTTPRequest ::= Status NewLine Headers NewLine Body NewLine
Status      ::= Method URL Signature Slash Version
Method      ::= String
URL         ::= Slash (String Slash | String)*
Version     ::= Digit Dot Digit
StatusCode  ::= Digit Digit Digit
Headers     ::= Header*
Header      ::= Key Colon Value NewLine
Body        ::= String
Key         ::= String
```


![
HTTPRequest ::= Status NewLine Headers NewLine Body NewLine
](diagram-1/diagram/HTTPRequest.png)

![
Status     ::= Method URL Signature Slash Version
](diagram-1/diagram/Status.png)

![
Method     ::= String
](diagram-1/diagram/Method.png)

![
URL        ::= Slash (String Slash | String)*
](diagram-1/diagram/URL.png)

![
Version    ::= digit dot digit
](diagram-1/diagram/Version.png)

![
StatusCode ::= digit digit digit
](diagram-1/diagram/StatusCode.png)

![
Headers    ::= Header*
](diagram-1/diagram/Headers.png)

![
Header     ::= Key Colon Value NewLine
](diagram-1/diagram/Header.png)

![
Body       ::= String
](diagram-1/diagram/Body.png)

![
Key        ::= String
](diagram-1/diagram/Key.png)

\newpage

### Język zapytań
```bnf
Char            ::= "A-Za-z0-9!@#$%^&*()_-+="
String          ::= Char*
MatchOperator   ::= "=~"
NotOperator     ::= "not"
EqOperator      ::= "=="
Comma           ::= ","
AndOperator     ::= "and"
OrOperator      ::= "or"
LeftBrace       ::= "("
RightBrace      ::= ")"
Quote           ::= '"'
Keyword         ::= 'if'

Query           ::= Field | Field Keyword Expression
Field           ::= String (Comma Field)*
Header          ::= Key
Key             ::= String
Expression      ::= Term (OrOperator Term)*
Term            ::= Factor (AndOperator Factor)*
Factor          ::= Constant| NotOperator Factor | (Expression)
Constant        ::= EqExpression|MatchExpression
EqExpression    ::= Field EqOperator Val
MatchExpression ::= Field MatchOperator Val
Val             ::= Quote String Quote
```

![
Query      ::= Field | Field Keyword Expression
](diagram-2/diagram/Query.png)

![
Field     ::=  String (Comma Field)*
](diagram-2/diagram/Field.png)

![
Header     ::= Key
](diagram-2/diagram/Header.png)

![
Key        ::= String
](diagram-2/diagram/Key.png)

![
Expression ::= LeftBrace Expression RightBrace
](diagram-2/diagram/Expression.png)

![
NotExpression ::= NotOperator Expression
](diagram-2/diagram/NotExpression.png)

![
MatchExpression ::= Field MatchOperator Val
](diagram-2/diagram/MatchExpression.png)

![
Val            ::= Quote String Quote
](diagram-2/diagram/Val.png)

\newpage

### Wymagania funkcjonalne
- możliwość przefiltrowania zestawu zapytań HTTP na postawie wprowadzonego przez
użytkownika zapytania
- parsowanie zapytań HTTP
- parsowanie prostego języka filtrowania

## Obsługa błędów
Program będzie wychwytywał błędy na każdym poziomie analizy. Moduł skanera
będzie informował o niepoprawnych tokenach. Parser będzie wychwytywał błędy
ziązanie z nieprawidłową kolejnością tokenów niezgodną z gramatyką.  W przypadku
zapytania HTTP błąd w pakiecie będzie powodował jego odrzucenie i przejście do
następnego wraz z wypisaniem komunikatu na stderr. Błąd w zapytaniu filtrującym
będzie podowował zatrzymanie programu i wypisanie komunikatu. Oba typy błędów
będą opatrzone informacją o dokładnym miejscu wystąpienia błędy (nr wiersza i
kolumna) w celu łatwej jego poprawy przez użytkownika.

## Sposób uruchomienia
```bash
cat input.txt | ./http-filter "method if host == "elka.pw.edu.pl"" > output.txt
./http-filter "url, host if not method=="GET""-i input.txt > output.txt
./http-filter "content-type if connection == "keep-alive" -i input.intput -o output.txt
```


# Przykład działania (przypadek testowy)
## Plik wejściowy (tylko requesty http)
```
================================================================================
GET /pypcapfile/ HTTP/1.1
Host: kisom.github.io
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36
Referer: http://pythonhosted.org/pypcapfile/intro.html
Accept-Encoding: gzip, deflate, sdch
Accept-Language: pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4
If-Modified-Since: Thu, 10 Jan 2013 00:09:50 GMT

================================================================================
GET /questions/4948043/pcap-python-library HTTP/1.1
Host: stackoverflow.com
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36
Referer: https://www.google.pl/
Accept-Encoding: gzip, deflate, sdch
Accept-Language: pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4
If-Modified-Since: Wed, 20 Apr 2016 20:42:08 GMT

================================================================================
GET / HTTP/1.1
Host: www.wp.pl
Cookie: SID=f8cdc2
Accept: */*
Connection: keep-alive
Accept-Encoding: gzip, deflate
User-Agent: python-requests/2.9.1

================================================================================
GET / HTTP/1.1
Host: twitch.tv
Accept: */*
Connection: keep-alive
Accept-Encoding: gzip, deflate
User-Agent: python-requests/2.9.1

================================================================================
POST / HTTP/1.1
Host: twitch.tv
Content-Length: 9
Accept: */*
User-Agent: python-requests/2.9.1
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Accept-Encoding: gzip, deflate

test=test

```

## Rezultat wykonania przykładowych filtrów na podanym pliku wejściowym
```bash
$ cat input.txt | ./http-filter 'method,url if host == "www.wp.pl"'
##########
method = POST
url = /plugins/phsys.php

$ cat input.txt | ./http-filter 'method,url if user-agent =~ "python"'
##########
method = POST
url = /plugins/phsys.php
##########
method = GET
url = /

$ cat input.txt | ./http-filter 'body if method == "POST"'
##########
body = user=asd&pass=asd

```

# Projekt realizacji parsowania zapytań HTTP
## Source
Moduł Source będzie służył w analizie pakietów HTTP aby uzystać listę pakietów
HTTP z pliku. Będzie można go podmienić na inny jeśli format pliku wejściowego
się zmieni. Moduł będzie zwracać obiekt HTTPRequest w którym znajdować się
będzie informacja o numerze lini i kolumny w celu podania miejca wystąpienia
błędu. Będzie on realizował dwie najważniejsze funkcje:

- otwieranie pliku z pakietami lub czytanie go z stdin
- podawanie następnego pakietu z pliku (funkcja next\_packet())

## Analizator leksykalny (skaner)
Analizator leksykalny będzie dokonywał rozbioru na tokeny. Będzie on rozpoznawał
czy nie pojawiły się nieznane ciągi np samotny symbol "CR" bez "LF" do pary.
Będzie odczytywał źródło zaptania znak po znaku. Na jego wyjściu pojawią się
kolejne tokeny. Będzie on udostępniał funkcje:

- tokenize - dokonanie skanowania zapytania HTTP
- next\_token - zwrócenie następnego tokenu. Pierwsze wykonanie zwraca pierwszy
token
- prev\_token - zwrócenie poprzedniego tokenu. Jeśli jesteśmy na pierwszym
tokenie to otrzymamy błąd.

## Analizator syntaktyczny (parser)
Parser będzie budował drzewo rozbioru na podstawie gramatyki zapytania HTTP.
Zostanie zastosowany algorytm rekursywnie zstępujący (RD). Jeśli próba
zbudowania drzewa rozbioru przebiegnie pomyślnie to moduł będzie podawał na
wyjściu kolejne numery użytych produkcji w wyprowadzeniu lewostronnym.

## Analizator semantyczny
Moduł ten będzie analizował pakiet i będzie stwierdzał czy użyte pola są
poprawne, np czy w polu method jest "GET" lub "POST" itp a nie coś nielegalnego
dla HTTP. Pakiety niepoprawne zostaną odrzucone. Analizator semantyczny generuje
na wyjściu abstrakcyjny obiekt zapytania http z odpowiednimi polami do których
łatwo można się odwołać w programie.

# Projekt realizacji dla prostego języka filtrowania
Analizator leksykalny, syntaktyczny i semantyczny analogicznie jak w przypadku
parsera zapytań. W tym przypadku nie ma modułu Source gdyż zapytanie trafia do
programu z linii poleceń i nie ma potrzeby odczytywać go z pliku. Zadanie
śledzenia numeru kolumny przejmie moduł Query znacząco uproszczony w porównaniu
do HTTPRequest.

# Algorytm działania
```python
1. Oczytaj parametry z lini poleceń
2. Dokonaj parsowania filtru pakietów. Jeśli nie było błędów do idź dalej
3. Wczytaj zapytania http
4. Dla każdego zapytania:
    1. Parsuj zapytanie
    2. Jeśli zapytanie pasuje do otrzymanego z filtru wzorca
        1. Wypisz wymagane w filtrze pola z pakietu
```

