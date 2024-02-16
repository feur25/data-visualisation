import pandas as pd
import streamlit as st
import plotly.graph_objs as go

st.set_page_config(layout="wide")

class CovidCaseVisualizer:
    def __init__(self):
        self.df = pd.read_csv('data/owid-covid-latest.csv')
        self.all_countries = self.df['location'].unique().tolist()

    def plot_selected_countries(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='total_cases', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=selected_data['total_cases'],
            y=selected_data['location'],
            orientation='h',
            marker_color='royalblue'
        ))

        fig.update_layout(
            title='Nombre de morts par pays',
            xaxis_title='Nombre de morts',
            yaxis_title='Pays',
            template='plotly_dark'
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_selected_new_cases(self, selected_countries):
        selected_data = self.df[self.df['location'].isin(selected_countries)]
        selected_data = selected_data.sort_values(by='new_cases', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=selected_data['location'],
            y=selected_data['new_cases'],
            marker_color='darkorange'
        ))

        fig.update_layout(
            title='Nouveaux cas par pays',
            xaxis_title='Pays',
            yaxis_title='Nouveaux cas',
            template='plotly_dark'
        )

        st.plotly_chart(fig, use_container_width=True)

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
