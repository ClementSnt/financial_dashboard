# Dashboard d'Analyse Financière

Ce projet est une application interactive développée sur Streamlit, permettant d'explorer et de comparer les données financières d'entreprises cotées en bourse. 
Il combine extraction de données via API, retraitement et manipulation des indicateurs clés, et visualisation dynamique.

---

# Objectifs

- Extraire des données financières via une API (en l'occurence celle d'Alpha Vantage)
- Cleaner et fusionner les données en un fichier tampon '.csv' (pour contourner la limite de 25 requêtes/jour de l'API)
- Visualiser les KPIs financiers et comparer les performances de différentes entreprises via des graphiques interactifs (courbes, radar, scatter)

---

# Technologies utilisées

- **Python**
- **Streamlit** (interface web)
- **Pandas / NumPy** (manipulation de données)
- **Plotly** (visualisations interactives)
- **Requests** (appel API)
- **CSV** (stockage local)

---

# Fonctionnalités du Dashboard

- Filtres dynamiques : industrie, entreprise, année fiscale, ratios
- Line plots : suivi de multiples ratios dans le temps
- Radar chart : performance globale multi-métriques
- Scatter plot : positionnement P/E vs. marge, taille des points ajusté à la valeur du market cap
- Tableaux dynamiques : vue synthétique des données par entreprise