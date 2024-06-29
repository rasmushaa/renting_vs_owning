import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd


__base_layout = go.Layout(showlegend=False,
                    hovermode='x unified',
                    updatemenus=[
                                dict(
                                    type='buttons', 
                                    showactive=False,
                                    y=1.05,
                                    x=1.15,
                                    xanchor='right',
                                    yanchor='top',
                                    pad=dict(t=0, r=10),
                                    )
                                ],
                    xaxis=dict(autorange=True),
                    yaxis=dict(autorange=True)
                    )


def plot_balance_projection(df: pd.DataFrame):    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Balance'],
            customdata=np.stack((np.ceil((df['Month']+1)/12 - 1), df['Month'], (df['Balance'] / 1000)), axis=-1),
            mode='lines',
            name='Loan Balance', 
            line=dict(width=2, color='red'),
            fill='tonexty',
            opacity=0.8,
            hovertemplate =
                '<b>Years:</b> %{customdata[0]}<br>'+
                '<b>Months:</b> %{customdata[1]}<br>'+
                '<b>Balance:</b> $%{customdata[2]:.0f}k' +
                '<extra></extra>'
            ))
    
    layout = __base_layout
    layout.update(
        yaxis_title='Loan Balance',
        xaxis_title='Years',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [int(12 * i) for i in range(df['Year'].max())],
            ticktext = [i for i in range(df['Year'].max())]
            )
        )
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)


def plot_apartment_return(df):
    fig = go.Figure()

    y = np.full(len(df), df['Apartment'][0])
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=y,
            customdata=np.stack((np.ceil((df['Month']+1)/12 - 1), df['Month'], (y / 1000)), axis=-1),
            mode='lines',
            name='Loan Balance', 
            line=dict(width=2, color='green'),
            fill='tozeroy',
            opacity=0.8,
            hovertemplate =
                '<b>Apartment Purchase Price:</b> $%{customdata[2]:.0f}k' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Apartment'],
            customdata=np.stack((np.ceil((df['Month']+1)/12 - 1), df['Month'], ((df['Apartment'] - y) / 1000)), axis=-1),
            mode='lines',
            name='Loan Balance', 
            line=dict(width=2, color='green'),
            fill='tozeroy',
            opacity=0.4,
            hovertemplate =
                '<b>Price Increase</b> $%{customdata[2]:.0f}k' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Apartment'],
            customdata=np.stack(df['Apartment'] / 1000, axis=-1),
            mode='lines',
            name='Net Assets', 
            line=dict(width=3, color='orange', dash='dash'),
            hovertemplate =
                '<b>Curent Value:</b> $%{customdata:.0f}k' +
                '<extra></extra>'
            ))
    
    layout = __base_layout
    layout.update(
        yaxis_title='Apartment Value',
        xaxis_title='Years',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [int(12 * i) for i in range(df['Year'].max())],
            ticktext = [i for i in range(df['Year'].max())]
            )
        )
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)


def plot_apartment_net_assets(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=-df['Balance'],
            customdata=np.stack((-df['Balance'] / 1000), axis=-1),
            mode='lines',
            name='Loan Balance', 
            line=dict(width=2, color='red'),
            fill='tozeroy',
            opacity=0.8,
            hovertemplate =
                '<b>Loan Balance:</b> $%{customdata:.0f}k' +
                '<extra></extra>'
            ))
    
    y = np.full(len(df), df['Apartment'][0])
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=y,
            customdata=np.stack((np.ceil((df['Month']+1)/12 - 1), df['Month'], (y / 1000)), axis=-1),
            mode='lines',
            name='Loan Balance', 
            line=dict(width=2, color='green'),
            fill='tozeroy',
            opacity=0.8,
            hovertemplate =
                '<b>Purchase Price:</b> $%{customdata[2]:.0f}k' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Apartment'],
            customdata=np.stack((np.ceil((df['Month']+1)/12 - 1), df['Month'], ((df['Apartment'] - y) / 1000)), axis=-1),
            mode='lines',
            name='Loan Balance', 
            line=dict(width=2, color='green'),
            fill='tozeroy',
            opacity=0.4,
            hovertemplate =
                '<b>Price Increase</b> $%{customdata[2]:.0f}k' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Apartment']-df['Balance'],
            customdata=np.stack((df['Apartment']-df['Balance']) / 1000, axis=-1),
            mode='lines',
            name='Net Assets', 
            line=dict(width=3, color='orange', dash='dash'),
            hovertemplate =
                '<b>Net Assets:</b> $%{customdata:.0f}k' +
                '<extra></extra>'
            ))
    
    layout = __base_layout
    layout.update(
        yaxis_title='Values',
        xaxis_title='Years',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [int(12 * i) for i in range(df['Year'].max())],
            ticktext = [i for i in range(df['Year'].max())]
            )
        )
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)  


def plot_payment(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Condominium'],
            customdata=np.stack(df['Condominium'], axis=-1),
            mode='lines',
            line=dict(width=2, color='grey'),
            fill='tozeroy',
            opacity=0,
            hovertemplate =
                '<b>Condominium</b> $%{customdata:.0f}' +
                '<extra></extra>'
            ))

    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Condominium'] + df['Principal'],
            customdata=np.stack(df['Principal'], axis=-1),
            mode='lines',
            line=dict(width=2, color='green'),
            fill='tonexty',
            opacity=0,
            hovertemplate =
                '<b>Principal</b> $%{customdata:.0f}' +
                '<extra></extra>'
            ))
        
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Condominium'] + df['Principal'] + df['Interest'],
            customdata=np.stack(df['Interest'], axis=-1),
            mode='lines',
            name='Payment Principal', 
            line=dict(width=2, color='red'),
            fill='tonexty',
            opacity=0.99,
            hovertemplate =
                '<b>Interest</b> $%{customdata:.0f}' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Condominium'] + df['Principal'] + df['Interest'],
            customdata=np.stack(df['Condominium'] + df['Principal'] + df['Interest'], axis=-1),
            mode='lines',
            name='Payment Principal', 
            line=dict(width=3, color='orange', dash='dash'),
            #fill='tonexty',
            hovertemplate =
                '<b>Total Cost</b> $%{customdata:.0f}' +
                '<extra></extra>'
            ))
    
    layout = __base_layout
    layout.update(
        yaxis_title='Amount [$]',
        xaxis_title='Years',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [int(12 * i) for i in range(df['Year'].max())],
            ticktext = [i for i in range(df['Year'].max())]
            )
        )
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)



def plot_renting_net_assets(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Contributions'],
            customdata=np.stack(df['Contributions']/1000, axis=-1),
            mode='lines',
            line=dict(width=2, color='green'),
            fill='tozeroy',
            opacity=0.8,
            hovertemplate =
                '<b>Contributions</b> $%{customdata:.0f}k' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Contributions'] + df['Interest'],
            customdata=np.stack(df['Interest']/1000, axis=-1),
            mode='lines',
            line=dict(width=2, color='green'),
            fill='tozeroy',
            opacity=0.4,
            hovertemplate =
                '<b>Interest</b> $%{customdata:.0f}k' +
                '<extra></extra>'
            ))
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'],
            y=df['Balance'],
            customdata=np.stack(df['Balance']/1000, axis=-1),
            mode='lines',
            line=dict(width=3, color='orange', dash='dash'),
            #fill='tozeroy',
            opacity=1.0,
            hovertemplate =
                '<b>Net Assets</b> $%{customdata:.0f}k' +
                '<extra></extra>'
            ))
    
    layout = __base_layout
    layout.update(
        yaxis_title='Amount [$]',
        xaxis_title='Years',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [int(12 * i) for i in range(df['Year'].max())],
            ticktext = [i for i in range(df['Year'].max())]
            )
        )
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)

