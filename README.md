# 🧠 **Startup-Ideed** – AI-põhine ärimõtete generaator

## 🎯 Eesmärk

Luua veebipõhine platvorm, kus kasutaja saab:
- Sisestada huvivaldkonna või probleemi
- Genereerida automaatselt **ärimudeli**, **väärtuspakkumise** ja **sihtgrupi**
- Hallata ideid (enda või avalikult jagatavaid)
- Uurida statistikat ja genereerida sarnaseid variatsioone

---

## 🏗️ Tehniline ülevaade

| Tehnoloogia         | Kirjeldus                              |
|---------------------|-----------------------------------------|
| **Python / Django** | Raamistiku alus, adminliides, autentimine |
| **Bootstrap 5**     | Kujundus ja kasutajaliidese mugavus     |
| **OpenAI API**      | Äriideede genereerimine (ChatGPT kaudu) |
| **SQLite**          | Arenduse andmebaas                      |
| **qrcode + Pillow** | QR-koodide loomine avalikeks linkideks  |
| **dotenv**          | API võtmete turvaline haldamine         |

---

## 🔑 Peamised funktsioonid

✅ **Ideede genereerimine OpenAI abil**  
✅ **Ärimudel / väärtuspakkumine / sihtgrupp** eraldi väljadena  
✅ **“Genereeri sarnane”** funktsioon olemasoleva põhjal  
✅ **Viide originaalideele (kloonide päritolu)**  
✅ **Minu ideed** vaade (kasutajapõhine)  
✅ **Avalik jagamine + QR-kood**  
✅ **CSV ja PDF eksport**  
✅ **Admin statistikavaade** (top kasutajad, kloonide arv, keskmised pikkused)

---

## 🔒 Autentimine

- Kasutajate registreerimine ja sisselogimine
- Iga idee seotud konkreetse kasutajaga
- Ainult enda ideede nägemine ja kloonimine

---

## 📊 Admin funktsioonid

- Täielikult kohandatud admin.py
- Originaali lingid + readonly väljad
- Statistikanurk `/admin/ideas/startupidea/statistics/`
- Top kasutajad, kloonid, keskmised pikkused jne

---

## 🧩 Tulevikuideed (soovi korral arendamiseks)

- Ideede **kategooriad** ja **märgendamine**  
- Like’d ja kommentaarid (avalikus vaates)  
- Slack / Discord jagamine  
- Kasutaja dashboard (graafiline)  
- GPT põhine "idee täpsustamine" ja "võrdle versioone"  
- API-ühendus teiste platvormidega

---

## 📁 Struktuur (olulised failid)

```
Startup_Ideed/
├── ideas/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│       └── ideas/
│           ├── generate.html
│           ├── result.html
│           ├── my_ideas.html
│           ├── public_idea.html
│
├── templates/
│   └── admin/ideas/statistics.html
├── manage.py
└── .env (sisaldab OPENAI_API_KEY)
```

---
