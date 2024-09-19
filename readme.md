# Project ehopu EVAkoberce

## Instalace a nastavení
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

# Vytvoření projektu na Django

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
