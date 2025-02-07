


import streamlit as st
import pathlib
import yfinance as yf


# Function to load CSS from the 'assets' folder

file_path = '/Users/ninni/desktop/volatility/assets/styles.css'

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
# css_path = pathlib.Path("/Users/ninni/desktop/volatility/assets/styles.css")
# load_css(css_path)




st.set_page_config(
    page_title="Volatility",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown("""
    <style>
    /* Stile testo markdown */
    .stMarkdown p {
        font-size: 14.5px !important; /* Imposta font corpo a 14.5px */
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    
col1, col2, col3 = st.columns([0.22, 0.28, 0.5])

with col1:
    giorni = st.slider("**giorni**", 5, 252, step=1, value=10)  # Valore di default 10
    giorni = giorni * -1

    col_1a, col1_b = st.columns([0.48, 0.52])

    with col_1a:
        
        #st.button('funziono?',key='pulse')
        with st.form(key='VOLatiliTY_Calc'):
            nome_ticker = st.text_input('**VOLatiliTY**', value="SPY", placeholder='Enter the Ticker').strip()  # Default SPY
            bottone_ricerca = st.form_submit_button('press to calc')

        if bottone_ricerca:
            if nome_ticker:
                ticker = yf.Ticker(nome_ticker.upper())
                dati_storici = ticker.history(period='1y')

                if len(dati_storici) > 0:
                    dati_storici = dati_storici[giorni:]
                    dati_storici['rendimento'] = (dati_storici['Close'].pct_change()) * 100
                    volatility = dati_storici['rendimento'].std()

                    with col1:
                        st.markdown(f'Volatilità **{nome_ticker.upper()}** negli ultimi **{giorni * -1}** giorni:&nbsp;&nbsp;**{volatility:.2f}%**')


                else:
                    with col1:
                        st.markdown(f'il ticker **{nome_ticker.upper()}** non esiste o è stato delistato')
                        
                        
            else:
            
                st.markdown(f'**inserisci un Ticker**')

                
                        
                        
                        
                        
                        
                        
                        
                        
                        


