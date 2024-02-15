#streamlit_app.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Visualisation des données COVID-19", page_icon=":microbe:", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

class CovidVisualizer:
    """
    A class for visualizing COVID-19 data including total deaths and new cases by country.

    Attributes:
        df (pandas.DataFrame): A DataFrame containing COVID-19 data.
        all_countries (list): A list of unique countries present in the DataFrame.

    Methods:
        plot_selected_countries(selected_countries): 
            Plot total deaths for the selected countries.
        plot_selected_new_cases(selected_countries): 
            Plot new cases for the selected countries.
        run(): 
            Run the Streamlit application for data visualization.
    """
    def __init__(self):
        """
        Initializes the CovidVisualizer class by loading COVID-19 data and getting unique countries.
        """
        self.df = pd.read_csv('data/owid-covid-latest.csv')
        self.all_countries = self.df['location'].unique().tolist()

    def plot_selected_countries(self, selected_countries):
        """
        Plot total deaths for the selected countries.

        Args:
            selected_countries (list): A list of selected countries to visualize.
        """
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='total_deaths', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='none', edgecolor='none')
        if len(selected_data) > 8: 
            bars = ax.barh(selected_data['location'], selected_data['total_deaths'], color='royalblue')
            ax.set_ylabel('Pays', color='gray') 
            ax.set_xlabel('Nombre de morts', color='gray') 
            ax.set_title('Nombre de morts par pays', color='gray') 
            for bar, death_count in zip(bars, selected_data['total_deaths']):
                if pd.notna(death_count):  
                    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, str(int(death_count)), va='center', color='gray') 
            ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            ax.tick_params(axis='y', colors='gray')  
        else:
            bars = ax.bar(selected_data['location'], selected_data['total_deaths'], color='royalblue')
            ax.set_xlabel('Pays', color='gray') 
            ax.set_ylabel('Nombre de morts', color='gray') 
            ax.set_title('Nombre de morts par pays', color='gray') 
            ax.tick_params(axis='x', rotation=45, colors='gray')  
            ax.tick_params(axis='y', colors='gray')  
            for bar, death_count in zip(bars, selected_data['total_deaths']):
                if pd.notna(death_count):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(death_count)), ha='center', va='bottom', color='gray') 
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        image = buf.getvalue()
        
        st.image(image, use_column_width='auto')

    def plot_selected_new_cases(self, selected_countries):
        """
        Plot new cases for the selected countries.

        Args:
            selected_countries (list): A list of selected countries to visualize.
        """
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='new_cases', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='none', edgecolor='none')
        if len(selected_data) > 8: 
            bars = ax.barh(selected_data['location'], selected_data['new_cases'], color='darkorange')
            ax.set_ylabel('Pays', color='gray') 
            ax.set_xlabel('Nouveaux cas', color='gray') 
            ax.set_title('Nouveaux cas par pays', color='gray') 
            for bar, case_count in zip(bars, selected_data['new_cases']):
                if pd.notna(case_count):  
                    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, str(int(case_count)), va='center', color='gray') 
            ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            ax.tick_params(axis='y', colors='gray')  
        else:
            bars = ax.bar(selected_data['location'], selected_data['new_cases'], color='darkorange')
            ax.set_xlabel('Pays', color='gray') 
            ax.set_ylabel('Nouveaux cas', color='gray') 
            ax.set_title('Nouveaux cas par pays', color='gray') 
            ax.tick_params(axis='x', rotation=45, colors='gray')  
            ax.tick_params(axis='y', colors='gray')  
            for bar, case_count in zip(bars, selected_data['new_cases']):
                if pd.notna(case_count):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(case_count)), ha='center', va='bottom', color='gray') 
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        image = buf.getvalue()
        
        st.image(image, use_column_width='auto')

    def run(self):
        """
        Run the Streamlit application for data visualization.
        """
        selected_countries = st.multiselect('Sélectionnez les pays:', self.all_countries)
        if selected_countries:
            col1, col2 = st.columns(2)
            with col1:
                self.plot_selected_countries(selected_countries)
            with col2:
                self.plot_selected_new_cases(selected_countries)

if __name__ == '__main__':
    visualizer = CovidVisualizer()
    visualizer.run()
