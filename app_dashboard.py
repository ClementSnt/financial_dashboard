import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative


df = pd.read_csv('financial_data.csv',sep=';', parse_dates=['fiscalDateEnding'])



# ----------------------------------- CALCUL DES RATIOS
# Partie Overview
df['marketCap'] = df['commonStockSharesOutstanding'] * df['stock_price']
df['RD_ratio'] = df['researchAndDevelopment'] / df['totalRevenue']
df['SGA_ratio'] = df['sellingGeneralAndAdministrative'] / df['totalRevenue']
df['detteRatio'] = df['totalLiabilities'] / df['totalAssets']
df['dividendYield'] = df['365 rolling'] / df['year_average']

# Partie Performance
df['grossMargin'] = pd.to_numeric(df['grossProfit'], errors='coerce') / pd.to_numeric(df['totalRevenue'], errors='coerce')
df['grossMargin'] = df['grossMargin'].replace([np.inf, -np.inf], np.nan).fillna(0)

df['Operating margin'] = df['operatingIncome'] / df['totalRevenue']
df['netMargin'] = df['netIncome'] / df['totalRevenue']
df['netMargin'] = df['netMargin'].replace([np.inf, -np.inf], np.nan).fillna(0)

df['ROE'] = df['netIncome'] / df['totalShareholderEquity']
df['ROA'] = df['netIncome'] / df['totalAssets']

df = df.sort_values(by=["symbol", "fiscalDateEnding"])
df["revenueGrowth"] = df.groupby("symbol")["totalRevenue"].pct_change()
df["earningsGrowth"] = df.groupby("symbol")["netIncome"].pct_change()

# Partie Valorisation
df['peRatio'] = df['stock_price'] / (df['netIncome'] / df['commonStockSharesOutstanding'])
df['price2book'] = df['marketCap'] / df['totalShareholderEquity']

# ------------------------------------ CREATION DES FILTRES
st.sidebar.header("Paramètres")

# filtre sur le secteur d'activité
industry_list = df["industry"].dropna().unique()
selected_industry = st.sidebar.selectbox("Industrie", sorted(industry_list))
df_filtered = df[df["industry"] == selected_industry]

# filtre sur l'entreprise
company_list = df_filtered["symbol"].unique()
selected_companies = st.sidebar.multiselect("Entreprises", sorted(company_list))

df_filtered = df_filtered[df_filtered["symbol"].isin(selected_companies)]

# filtre sur l'année fiscale
annee_fiscale = df_filtered['fiscal_year'].dropna().unique()
selected_fiscalyear = st.sidebar.selectbox("Année fiscale", sorted(annee_fiscale, reverse=True))
df_tableau_recap = df_filtered[df_filtered["fiscal_year"] == selected_fiscalyear]

# filtre sur le ratio à afficher dans le lineplot d'introduction
metrics_lineplot = {'totalRevenue':'Revenues',
                 'ebit':'EBIT',
                 'netIncome':'Net Income',
                 'grossMargin':'Gross Margin',
                 'Operating margin':'Operating margin',
                 'netMargin':'Net margin',
                 'ROE':'ROE',
                 'ROA':'ROA',
                 'revenueGrowth':'Revenue growth',
                 'peRatio':'P/E',
                 'price2book':'Price to book ratio',
                 'RD_ratio':'R&D ratio',
                 'SGA_ratio':'SG&A ratio',
                 'totalAssets':'Total Assets',
                 'dividendYield':'Dividend Yield'}

# Inversion : label vers colonne pour avoir les bons noms dans les filtres
label_to_column = {v: k for k, v in metrics_lineplot.items()}

# Selectbox avec les labels
selected_label = st.sidebar.selectbox("Ratio pour le lineplot", sorted(label_to_column.keys()),index=sorted(label_to_column.keys()).index('Revenues'))

# Nom de la colonne dans le DataFrame
selected_column = label_to_column[selected_label]


# Palette de couleurs affectée à chaque entreprise pour éviter les changements entre les graphes
color_map = dict(zip(selected_companies, qualitative.Plotly[:len(selected_companies)]))





st.title("📊 Financial Analysis Tool ")


# ----------------------------- DASH
if len(df_tableau_recap) == 0:
    st.warning("Aucune donnée pour les filtres sélectionnés. Pour afficher les filtres, cliquez sur >> en haut à gauche.")
else:
    df_tableau_recap = df_tableau_recap.set_index('symbol')

    if selected_companies:



        st.subheader(f"📌 Overview for {selected_fiscalyear}")


        # ------------------------ LINE PLOT
        df_lineplot = df_filtered[df_filtered["symbol"].isin(selected_companies)].copy()
        df_lineplot["fiscal_year"] = df_lineplot["fiscal_year"].astype(int)
        df_lineplot = df_lineplot.sort_values(by="fiscal_year")

        fig = px.line(
            df_lineplot,
            x="fiscal_year",
            y=selected_column,
            color="symbol",
            color_discrete_map=color_map,
            markers=True,
            labels={
                "fiscal_year": "Fiscal year",
                selected_column: selected_label,
                "symbol": "Company"
            },
            title=f"📈 {selected_label} evolution per company and per fiscal year."
        )
        fig.update_layout(
            yaxis_tickformat=",",
            xaxis_title="Fiscal year",
            yaxis_title=selected_label,
        )
        st.plotly_chart(fig, use_container_width=True)





        # ------------------------ OVERVIEW TABLE
        metrics_overview = {
            'totalRevenue': 'Revenus',
            'RD_ratio': 'R&D ratio',
            'SGA_ratio': 'SG&A ratio',
            'detteRatio': 'Debt ratio',
            'marketCap': 'Market capitalisation',
            'cashAndCashEquivalentsAtCarryingValue': 'Cash & equiv',
            'dividendYield': 'Rendements dividendes',
        }

        # Colonnes à formater en pourcentage
        percent_labels = ['R&D ratio', 'SG&A ratio','Debt ratio', 'Rendements dividendes']

        # Construction du tableau avec les bons formats
        overview_data = {}
        for col, label in metrics_overview.items():
            values = []
            for company in selected_companies:
                if company in df_tableau_recap.index:
                    val = df_tableau_recap.loc[company, col]
                    if pd.notnull(val):
                        if label in percent_labels:
                            formatted = f"{val * 100:.2f}%"  # % formatting
                        else:
                            formatted = f"{val:,.0f}"  # Numeric formatting
                    else:
                        formatted = "-"
                else:
                    formatted = "-"
                values.append(formatted)
            overview_data[label] = values

        df_overview = pd.DataFrame(overview_data, index=selected_companies).T
        st.dataframe(df_overview)



        st.subheader(f"📌 Financial and commercial performances for {selected_fiscalyear}")
        # -------------------------------------------------------------------------------------- RADAR CHART

        # selection des ratios à afficher
        radar_metrics = {
            "netMargin": "Net Margin",
            "Operating margin": "Operating Margin",
            "grossMargin": "Gross Margin",
            "ROE": "ROE",
            "ROA": "ROA",
            "revenueGrowth": "Revenue Growth"
        }
        df_radar = df_filtered[df_filtered["fiscal_year"] == selected_fiscalyear]
        df_radar = df_radar[df_radar["symbol"].isin(selected_companies)].fillna(0)

        # remplacer par 0 les valeurs négatives (cas fréquent) pour ne pas casser le graphe et le rendre illisible
        radar_data = pd.DataFrame({
            label: [df_radar.loc[df_radar["symbol"] == symbol, key].values[0] if symbol in df_radar["symbol"].values else 0 for symbol in selected_companies]
            for key, label in radar_metrics.items()
        }, index=selected_companies).T


        radar_cleaned = radar_data.clip(lower=0)

        fig_radar = go.Figure()
        for company in radar_cleaned.columns:
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_cleaned[company].values,
                theta=radar_cleaned.index,
                fill='toself',
                name=company,
                line=dict(color=color_map.get(company))
            ))

        fig_radar.update_layout(
            template="plotly_dark",
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=True,
        )
        st.plotly_chart(fig_radar, use_container_width=True)




        # ------------------------ PERFORMANCE TABLE
        metrics_performance = {
            'revenueGrowth': 'Revenues growth rate',
            'grossMargin':'Gross margin',
            'Operating margin':'Operating margin',
            'netMargin': 'Net margin',
            'ROE':'ROE',
            'ROA':'ROA',
        }
        performance_data = {
            label: [df_tableau_recap.loc[company, col] if company in df_tableau_recap.index else None for company in selected_companies]
            for col, label in metrics_performance.items()
        }
        df_performance = pd.DataFrame(performance_data, index=selected_companies).T
        df_performance = df_performance.applymap(lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else "-")
        st.dataframe(df_performance)



        st.subheader(f"📌 Valuation for {selected_fiscalyear}")
        # --------------------------------------------------------------------------------- SCATTER PLOT
        df_scatter = df_filtered[df_filtered["fiscal_year"] == selected_fiscalyear].copy()

        # selection des dimensions à intégrer
        df_scatter = df_scatter[
            df_scatter["peRatio"].notna() &
            df_scatter["netMargin"].notna() &
            df_scatter["marketCap"].notna()
        ]

        # axe x le P/E, en y le MC et la taille des points égal le MC
        fig_scatter = px.scatter(
            df_scatter,
            x="peRatio",
            y="netMargin",
            size="marketCap",
            color="symbol",
            color_discrete_map=color_map,
            hover_name="symbol",
            labels={
                "peRatio": "P/E Ratio",
                "netMargin": "Marge nette",
                "marketCap": "Capitalisation boursière"
            },
        )
        fig_scatter.update_layout(
            xaxis_title="P/E Ratio (bas = moins cher)",
            yaxis_title="Marge nette (haut = plus rentable)",
            legend_title="Entreprise",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)



        # ------------------------------------------ VALUATION TABLE
        metrics_valuation = {
            'peRatio': 'P/E',
            'price2book': 'Price to book'
        }

        valuation_data = {
            label: [df_tableau_recap.loc[company, col] if company in df_tableau_recap.index else None for company in selected_companies]
            for col, label in metrics_valuation.items()
        }
        df_valuation = pd.DataFrame(valuation_data, index=selected_companies).T
        df_valuation = df_valuation.applymap(lambda x: f"{x:.2f}" if pd.notnull(x) else "-")
        st.dataframe(df_valuation)




    else:
        st.warning("Veuillez sélectionner au moins une entreprise.")
