# 📈 Dashboard d'Analyse Financière

🔗 **[Accéder au dashboard interactif](https://financialdashboard-cs.streamlit.app)**

---

Ce projet est une application interactive développée avec **Streamlit**, permettant d'explorer et de comparer les données financières d’entreprises cotées en bourse. Il combine **extraction via API**, **nettoyage des données**, **calcul d’indicateurs clés**, et **visualisation dynamique**.

---

## 🎯 Objectifs

- **Extraction des données via l’API d’Alpha Vantage** ([site officiel](https://www.alphavantage.co))  
  → J’ai récupéré les bilans, comptes de résultats, historiques de dividendes, cours boursiers ainsi que les taux de change pour convertir les données en USD.  
  ➤ Une partie de cette requête est visible dans `data_extraction_sample.py`

- **Nettoyage & fusion** dans un fichier `.csv` tampon, pour contourner la limite de 25 requêtes/jour imposée par l'API.  
  ➤ Un extrait des données est disponible dans `financial_data.csv`

- **Construction du dashboard** : visualisation des principaux **KPIs financiers** utilisés dans mes analyses, avec la possibilité de comparer plusieurs entreprises d’un même secteur.
  ➤ Code disponible dans `app_dashboard.py`
  ⚠️ *Seule une sélection d’entreprises est disponible dans cette version publique.*

---

## ⚙️ Technologies utilisées

- Python
- Requests (API)
- Pandas / NumPy
- Plotly
- Streamlit

---

## ⚙️ Fonctionnalités du dashboard

- **Filtres dynamiques** : par secteur, entreprise, année fiscale, ratio
- **Line plots** : évolution d’un ratio sur plusieurs années
- **Radar chart** : comparaison multi-métriques
- **Scatter plot** : positionnement P/E vs marge nette (taille = capitalisation)
- **Tableaux dynamiques** : vue synthétique des données clés par entreprise

---
