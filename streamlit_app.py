import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io
import base64

st.set_option('deprecation.showPyplotGlobalUse', False)

# hide_st_style = """
#                 <style>
#                 #MainMenu {visibility: hidden;}
#                 footer {visibility: hidden;}
#                 header {visibility: hidden;}
#                 </style>
#                 """
# st.markdown(hide_st_style, unsafe_allow_html=True)

class CovidVisualizer:
    def __init__(self):
        self.df = pd.read_csv('data/owid-covid-latest.csv')
        self.all_countries = self.df['location'].unique().tolist()
    
    def plot_selected_countries(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='total_deaths', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='none', edgecolor='none')
        
        if len(selected_data) > 8: 
            bars = ax.barh(selected_data['location'], selected_data['total_deaths'])
            ax.set_ylabel('Pays', color='white') 
            ax.set_xlabel('Nombre de morts', color='white') 
            ax.set_title('Nombre de morts par pays', color='white') 
            for bar, death_count in zip(bars, selected_data['total_deaths']):
                if pd.notna(death_count):  
                    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, str(int(death_count)), va='center', color='white') 
            ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            ax.tick_params(axis='y', colors='white')  
            ax.spines['top'].set_visible(False) 
            ax.spines['right'].set_visible(False) 
            ax.spines['left'].set_visible(False) 
        else:
            bars = ax.bar(selected_data['location'], selected_data['total_deaths'])
            ax.set_xlabel('Pays', color='white') 
            ax.set_ylabel('Nombre de morts', color='white') 
            ax.set_title('Nombre de morts par pays', color='white') 
            ax.tick_params(axis='x', rotation=45, colors='white')  
            ax.tick_params(axis='y', colors='white')  
            for bar, death_count in zip(bars, selected_data['total_deaths']):
                if pd.notna(death_count):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(death_count)), ha='center', va='bottom', color='white') 
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False) 
            ax.spines['left'].set_visible(False) 

        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        image = buf.getvalue()
        
        st.image(image, use_column_width=True)

    def run(self):
        selected_countries = st.multiselect('Sélectionnez les pays:', self.all_countries)
        if selected_countries:
            self.plot_selected_countries(selected_countries)

if __name__ == '__main__':
    visualizer = CovidVisualizer()
    visualizer.run()
