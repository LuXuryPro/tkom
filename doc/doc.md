# TKOM - Projekt - dokumentacja

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
```


### Przykłady użycia
```
show Host if POST
show Endpoint if GET and Host == www.elka.pw.edu.pl
show Endpoint if GET == true and Host == www.elka.pw.edu.pl
show if body ~= 71717C6
count if DELETE
```
