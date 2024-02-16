import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io

st.set_page_config(layout="wide")

class CovidCaseVisualizer:
    def __init__(self):
        self.df = pd.read_csv('data/owid-covid-latest.csv')
        self.all_countries = self.df['location'].unique().tolist()

    def plot_selected_countries(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='total_cases', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='none') 
        ax.barh(selected_data['location'], selected_data['total_cases'], color='royalblue')
        ax.set_xlabel('Nombre de morts')
        ax.set_ylabel('Pays')
        ax.set_title('Nombre de morts par pays')
        ax.tick_params(axis='x', labelcolor='gray')
        ax.tick_params(axis='y', labelcolor='gray')
        ax.invert_yaxis() 
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        st.image(buf)

    def plot_selected_new_cases(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='new_cases', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='none') 
        ax.bar(selected_data['location'], selected_data['new_cases'], color='darkorange')
        ax.set_xlabel('Pays')
        ax.set_ylabel('Nouveaux cas')
        ax.set_title('Nouveaux cas par pays')
        ax.tick_params(axis='x', rotation=45, labelcolor='gray')
        ax.tick_params(axis='y', labelcolor='gray')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        st.image(buf)

    def plot_cases_distribution(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        total_cases = selected_data['total_cases'].sum()
        labels = selected_data['location']
        sizes = selected_data['total_cases'] / total_cases * 100

        fig, ax = plt.subplots(figsize=(8, 8), facecolor='none') 
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title('Répartition des cas par pays')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        st.image(buf)

    def run(self):
        selected_countries = st.multiselect('Sélectionnez les pays:', self.all_countries)
        if selected_countries:
            col1, col2, col3 = st.columns(3)
            with col1:
                self.plot_selected_countries(selected_countries)
            with col2:
                self.plot_selected_new_cases(selected_countries)
            with col3:
                self.plot_cases_distribution(selected_countries)

if __name__ == '__main__':
    visualizer = CovidCaseVisualizer()
    visualizer.run()
