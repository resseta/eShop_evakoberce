# eShop EvaKoberce

Vítejte v projektu eShop EvaKoberce! Tento projekt je online obchod napsaný na Django, který uživatelům umožňuje prohlížet, nakupovat zboží, vybírat barvu materiálů a lemování.

## Instalace
```bash
pip install django
```

## 
```bash
pip instal Pillow
```

```bash
pip freeze > requirements.txt
```
## Nastavení

Chcete-li tento projekt nasadit lokálně, postupujte podle následujících kroků:

1. Klonujte úložiště do počítače:
    ```bash
    git clone https://github.com/yourusername/eShop_evakoberce.git
    cd eShop_evakoberce
    ```

2. Vytvořte virtuální prostředí a aktivujte jej:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Pro Windows
    source .venv/bin/activate  # Pro macOS/Linux
    ```
### Konfigurace

## Struktura projektu
- evakoberce - nastavení projektu
  - `__innit__.py` - nazbytné k nastavení cesty k modulu
  - `asgi.py` - nebudeme používat
  - `settings.py` - nastavení našeho projektu
  - `urls.py` - v tomto soubouru nastavujem url cestu
  - `wsgi.py`

### Database (`Models`)
We can generate ER diagram in Pycharm PRO:
python manage.py graph_models viewer --pydot -g -o ./files/erd_viewer_d.png


3. Nastavte závislosti ze souboru`requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. Aplikujte migrace databáze:
    ```bash
    python manage.py migrate
    ```

5. Spusťte vývojový server:
    ```bash
    python manage.py runserver
    ```

## Použití

### Hlavní příkazy

- Nastartování serveru:
    ```bash
    python manage.py runserver
    ```

- Vytvoření superusera: 
    ```bash
    python manage.py createsuperuser 
    ```

- # doplnění databáze (produkty) doplnění přes administrátora

- Spouštění testů:
    ```bash
    pytest
    ```

