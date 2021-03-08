import json

with open('keyQiwi.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

QIWI_PRIV_KEY = text['key']
