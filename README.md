# Dashboard d'Analyse Financière 📈

-----> Lien vers le dashboard : https://financialdashboard-cs.streamlit.app

Ce projet est une application interactive développée sur Streamlit, permettant d'explorer et de comparer les données financières d'entreprises cotées en bourse. 
Il combine extraction de données via API, retraitement et manipulation des indicateurs clés, et visualisation dynamique.

---

# Objectifs 🎯

- Extraction des données via l'API d'Alpha Vantage : https://www.alphavantage.co
J'ai extrait les données du bilan, du compte de résultats, l'historique des dividendes, le cours de l'action ainsi que les taux de          change pour convertir les données en USD.
Une partie de cette requête est disponible dans data_extraction_sample.py

- Cleaner et fusionner les données en un fichier tampon '.csv' pour contourner la limite de 25 requêtes/jour de l'API.
Une partie des données est disponible dans financial_data.csv
  
- Construction d'un dashboard interactif me permettant de visualiser les principaux KPIs financiers que j'utilise régulièrement dans mes analyses et comparer les performances de différentes entreprises par secteur d'activité via des graphiques (courbes, radar, scatter) et tableaux récapitulatifs
  ⚠️ **Seule une partie des entreprises est disponible dans cette version publique** ⚠️

---

# Technologies utilisées ⚙️

- **Python**
- **Requests** (appel API)
- **Pandas / NumPy**
- **Plotly**
- **Streamlit** 

---

# Fonctionnalités du Dashboard ⚙️

- Filtres dynamiques : industries, entreprises, années fiscales, ratios
- Line plots : évolution de multiples ratios préalablement sélectionnés dans les filtres
- Radar chart : performance globale multi-métriques
- Scatter plot : positionnement P/E vs. marge, la taille des points est ajustée à la valeur de la capitalisation boursière
- Tableaux dynamiques : vue synthétique des données par entreprise
