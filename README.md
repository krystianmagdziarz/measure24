### Środowisko interatkwyne

1. Zainstaluj python3 dodając interpreter do zmiennych środowiskowych;
2. Utwórz wirtualne środowisko w /measure24/measure24/facebook_test
`` 
python -m venv /sciezka_do/measure24/measure24/facebook_test
``
3. Uruchom wirtualne środowisko
``/sciezka_do/measure24/measure24/facebook_test/venv/Scripts/activate``
4. Rozpocznij sekwecję testującą
``/sciezka_do/measure24/measure24/facebook_test/test.py``

### Wersja serwerowa

1. Uruchom środowisko
``docker-composer up --build``

Panel dostępny jest pod adresem 
``localhost:8000/admin``\
Dane do bazy danych i dane logowania znajdują się w:
``.env``

### Zmiany handler-ów DOM

- Odbywają się za pomocą zmiennych w plikach ``common/facebook.py`` oraz ``facebook_test/test.py``
```python
tag_attr = "class"
tag_value = "dn"
```

### Brak powiadomień e-mail
- Należy uzupełnić plik .env w dane dostępowe serwera SMTP.
