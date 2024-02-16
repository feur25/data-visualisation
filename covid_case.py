import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

class CovidCaseVisualizer:
    def __init__(self):
        self.df = pd.read_csv('data/owid-covid-latest.csv')
        self.all_countries = self.df['location'].unique().tolist()

    def plot_selected_countries(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='total_cases', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(selected_data['location'], selected_data['total_cases'], color='royalblue')
        ax.set_xlabel('Nombre de morts')
        ax.set_ylabel('Pays')
        ax.set_title('Nombre de morts par pays')
        ax.tick_params(axis='x', labelcolor='gray')
        ax.tick_params(axis='y', labelcolor='gray')
        ax.invert_yaxis() 
        st.pyplot(fig)

    def plot_selected_new_cases(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='new_cases', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(selected_data['location'], selected_data['new_cases'], color='darkorange')
        ax.set_xlabel('Pays')
        ax.set_ylabel('Nouveaux cas')
        ax.set_title('Nouveaux cas par pays')
        ax.tick_params(axis='x', rotation=45, labelcolor='gray')
        ax.tick_params(axis='y', labelcolor='gray')
        st.pyplot(fig)

    def run(self):
        selected_countries = st.multiselect('Sélectionnez les pays:', self.all_countries)
        if selected_countries:
            col1, col2 = st.columns(2)
            with col1:
                self.plot_selected_countries(selected_countries)
            with col2:
                self.plot_selected_new_cases(selected_countries)

if __name__ == '__main__':
    visualizer = CovidCaseVisualizer()
    visualizer.run()
