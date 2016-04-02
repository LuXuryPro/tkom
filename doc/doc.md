# TKOM - Projekt - dokumentacja

>Celem zadania jest analiza składniowa komunikacji protokołu HTTP zapisanej w
>plikach tekstowych (wczytywanie z plików pcap byłoby dodatkowym atutem) i
>możliwość wyszukiwania interesujących komunikacji, z wykorzystaniem
>zaproponowanego prostego języka wyszukiwania. Przykładowe interesujące
>połączenia protokołu HTTP przedstawione jest poniżej. Jest ono charakteryzowane
>między innymi: metodą POST, URL-em zawierającym podciąg phsys.php oraz
>wysłanymi danymi postaci "data=xxx", gdzie xxx to liczby szesnastkowe.

## Składnia języka zapytań
```
OPERATION => show+HTTP_HEADER_LIST | count
SHOW_OPERATION => show+HTTP_HEADER_LIST | show
QUERY => OPERATION if CONDITION START LIMIT
START => from NUMBER | ε
LIMIT => up to NUMBER | ε
HTTP_HEADER_LIST => HTTP_HEADER | HTTP_HEADER_LIST+,+HTTP_HEADER
CONDITION =>  CONDITION_PART | CONDITION BOOL_OPERATOR CONDITION_PART
CONDITION_PART = CONDITION_PART_HTTP_HEADER | CONDITION_PART_HTTP_BODY
CONDITION_PART_HTTP_HEADER = HTTP_HEADER OPERATOR VALUE | HTTP_HEADER
CONDITION_PART_HTTP_BODY = body OPERATOR VALUE
VALUE => NUMBER | CHARACTER | VALUE+NUMBER | VALUE+CHARACTER
OPERATOR => == | ~= | !=
BOOL_OPERATOR => and | or
```

### Nazwy nagłówków
```
Wejście:

POST /plugins/phsys.php HTTP/1.1
Accept: , \x08\xba\x16, , , , , , , , , , , , , , , , , , , ,
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 6.3 rv:11.0) like Gecko
Host: exaltation.info
Content-Length: 645
Cache-Control: no-cache

data=5A18B30CFCDA6B5D347FC82E071717C65A2E29518F746DC9FC1514A25AAB26B64D95AF
CDD69ACFCB79CE26341F55BFEA3377FBCE8E6AF37374167724FAE23F7CF4E00792E81332E96
3C37981934916094CF384F97A4F33A738B6003A17CB769F9E9EA945BCA0C0DB6CD2799AB7B0
27C370E6B88E1CEF30C090130D051FD616C6FDD382AE15F85100633FB5E3BF3815D
```
```
Wyjście:
POST == true
Endpoint = /plugins/phsys.php
HTTPVersion == 1.1
Accept == , \x08\xba\x16, , , , , , , , , , , , , , , , , , , ,
Content-Type == application/x-www-form-urlencoded
User-Agent == Mozilla/5.0 (Windows NT 6.3 rv:11.0) like Gecko
Host == exaltation.info
Content-Length == 645
Cache-Control == no-cache
body == data=5A18B30CFCDA6B5D347FC82E071717C65A2E29518F746DC9FC1514A25AAB26
B64D95AFCDD69ACFCB79CE26341F55BFEA3377FBCE8E6AF37374167724FAE23F7CF4E00792E
81332E963C37981934916094CF384F97A4F33A738B6003A17CB769F9E9EA945BCA0C0DB6CD2
799AB7B027C370E6B88E1CEF30C090130D051FD616C6FDD382AE15F85100633FB5E3BF3815D
```


### Przykłady użycia
```
show Host if POST
show Endpoint if GET and Host == www.elka.pw.edu.pl
show Endpoint if GET == true and Host == www.elka.pw.edu.pl
show if body ~= 71717C6
count if DELETE
```
