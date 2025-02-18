


import streamlit as st
import pathlib
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import timedelta
open_time = '09:30:00'
close_time = '22:00:00'


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


    
    
    
col1, col2, col3 = st.columns([0.22, 0.38, 0.4])
with col1:
    
    
    if 'giorni' not in st.session_state:
        st.session_state['giorni'] = 10
    
    giorni = st.slider("**giorni**", 5, 252, step=1,value=st.session_state['giorni'])  # Valore di default 10
    giorni = giorni * -1
    

    col_1a, col1_b = st.columns([0.48, 0.52])

    with col_1a:
        
        #st.button('funziono?',key='pulse')
        with st.form(key='VOLatiliTY_Calc'):
            nome_ticker = st.text_input('**VOLatiliTY**', value="SPY", placeholder='Enter the Ticker').upper().strip()  # Default SPY
            # st.session_state["nome_ticker"] = nome_ticker
            bottone_ricerca = st.form_submit_button('press to calc')
            
        
        if 'ricerca_premuto' not in st.session_state:
            st.session_state['ricerca_premuto'] = False
            

        if bottone_ricerca:

            if nome_ticker:
                
                st.session_state["nome_ticker"] = nome_ticker
                ticker = yf.Ticker(nome_ticker.upper())
                dati_storici = ticker.history(period='1y')
                st.session_state['dati_storici'] = dati_storici
                
                if len(st.session_state['dati_storici'])>0:
                    st.session_state['ricerca_premuto'] = True
                     
                else:
                   with col1:
                       st.markdown(f'il ticker **{nome_ticker.upper()}** non esiste o è stato delistato')      
                
            else:
                st.markdown(f'**inserisci un Ticker**')
                st.session_state.clear()
                st.session_state['ricerca_premuto'] = False
            
            
                
                
                
    if st.session_state['ricerca_premuto'] == True:  
        
        if len(st.session_state['dati_storici']) > 0:
            
            
                    st.session_state['dati_storici']['rendimento'] = (st.session_state['dati_storici']['Close'].pct_change())*100
                    st.session_state['dati_storici']['rolling'] = st.session_state['dati_storici']['rendimento'].rolling(window=(giorni*-1)).std(ddof=0)
                    
            
                    current = datetime.today()-timedelta(hours=5) # tolgo 6 ore (New York) dall'orario della data corrente
                    current_date = datetime.today().date() # solo la data corrente
                    day = current.strftime('%A') # mi indica che giorno è attualmente (monday etc..)
                    
                    if current.strftime('%H:%M:%S') < open_time or current.strftime('%H:%M:%S') > close_time or\
                        day =="Saturday" or day=="Sunday": 
        
                        dati_custom = st.session_state['dati_storici'][giorni:].copy()
                        
                     
                    if (current.strftime('%H:%M:%S') > open_time  and current.strftime('%H:%M:%S') < close_time) and\
                        day !="Saturday" and day !="Sunday": 
                         
                        if st.session_state['dati_storici'].index[-1].date() == current_date:            
                            dati_custom = st.session_state['dati_storici'][(giorni-1):-1].copy()
                        
                        if st.session_state['dati_storici'].index[-1].date() != current_date:
                            dati_custom = st.session_state['dati_storici'][giorni:].copy()
                            
                          
                        
                        
                    #dati_custom['rendimentone'] = (dati_custom['Close'].pct_change()) * 100
                    volatility = dati_custom['rendimento'].iloc[1:].std(ddof=0)
                    # dal 1° giorno al 2° avrò il primo rendimento e così via, 
                    #devo quindi scartare il rpimo rendimento che è relativo alla differenza
                    # tra il primo elemento non presente in elenco ed il primo presente
                    st.session_state['volatility'] = volatility
                    volatility_ann = volatility*np.sqrt(252)
                    
                    
                    # dati_storici_20 = st.session_state['dati_storici'][-20:].copy()
                    # dati_storici_20['rendimento'] = (dati_storici_20['Close'].pct_change()) * 100
                    # volatility_20 = (dati_storici_20['rendimento'].std(ddof=0))*np.sqrt(252)
                    
                    
                    # dati_storici_30 = st.session_state['dati_storici'][-30:].copy()
                    # dati_storici_30['rendimento'] = (dati_storici_30['Close'].pct_change()) * 100
                    # volatility_30 = (dati_storici_30['rendimento'].std(ddof=0))*np.sqrt(252)
                    
                    
                    # dati_storici_60 = st.session_state['dati_storici'].copy()
                    # dati_storici_60['rendimento'] = (dati_storici_60['Close'].pct_change()) * 100
                    # volatility_60 = (dati_storici_60['rendimento'].std(ddof=0))*np.sqrt(252)
                    

                        
                    st.markdown('*periodo considerato:*')
                    da_ = dati_custom.index[0].date().strftime('%d-%m-%Y')
                    a_ = dati_custom.index[-1].date().strftime('%d-%m-%Y')
                    st.markdown(f" dal **{da_}** al **{a_}**")
                    # st.markdown(f" dal **{dati_custom.index[-1].date()}** al **{dati_custom.index[0].date()}**")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown(f'Volatilità giornaliera **{nome_ticker.upper()}**\
                                    a **{giorni * -1}** giorni:&nbsp;&nbsp;**{volatility:.2f}%**')
                                    
                    st.markdown(f'Volatilità a **{giorni * -1}** giorni annualizzata:&nbsp;&nbsp;**{volatility_ann:.2f}%**')
                    # st.markdown(f'Volatilità a **20** giorni annualizzata:&nbsp;&nbsp;**{volatility_20:.2f}%**')
                    # st.markdown(f'Volatilità a **30** giorni annualizzata:&nbsp;&nbsp;**{volatility_30:.2f}%**')
                    # st.markdown(f'Volatilità a **60** giorni annualizzata:&nbsp;&nbsp;**{volatility_60:.2f}%**')
                   
                    
                        
                
                        

                    
                    
                    if st.session_state["nome_ticker"] == "SPY":                
                        with col2:
                            
                            col2a,col2b,col2c,col2d = st.columns([0.10,0.25,0.25,0.40])
                            col2e,col2f = st.columns([0.10,0.9])
                            #col2g,col2h,col2i = st.columns([0.10,0.50,0.40])
                            
                            with col2b:
                                trade = st.text_input('**rischio per trade**',value='',placeholder='value in $').strip()
                                #st.session_state['ricerca_premuto'] = True 
                                
                            with col2c:
                                valore_attuale_yf = st.session_state['dati_storici']['Close'][-1]
                                valore_attuale = st.text_input('**valore attuale** (yf)',value=f'{valore_attuale_yf:.2f}',placeholder="value in $")
                                
                                st.markdown('*(puoi modificarlo)*')
                                
                                
                
                
                                
                                def is_numeric(variable):
                                    try:
                                        variable = float(variable)
                                        return True 
                                    except:
                                        return False
                                    
                                    
                                
                                valore_attuale_verifica = is_numeric(valore_attuale)
                                trade_verifica = is_numeric(trade)
                                
                                
                                if valore_attuale_verifica==True and trade_verifica ==True:
                                    
                                    valore_attuale = float(valore_attuale)
                                    trade = float(trade)
                                    n_azioni = trade/((st.session_state['volatility']/100)*valore_attuale)
                                    with col2f:
                                        st.markdown(f'azioni da acquistare:&nbsp;&nbsp;**{n_azioni:.2f}**')
                                        
                                        
                                        
                                        
                                elif (valore_attuale_verifica==False and len(valore_attuale)>0) or\
                                   (trade_verifica==False and len(trade)>0):
                                       
                                       with col2f:
                                           st.markdown('non posso calcolare il numero di azioni senza valore di trade e/o prezzo')
                                           
                                           
                        
                                           
                                           
                                       
                       
                    with col2:
                        
                        #col2g,col2h,col2i = st.columns([0.15,0.50,0.35]) 
                        if st.session_state["nome_ticker"] == "SPY": 
                            col2g,col2h,col2i = st.columns([0.15,0.50,0.35]) 
                        else: 
                            col2g,col2h,col2i = st.columns([0.23,0.50,0.27]) 
                            
                        with col2h:

                            st.session_state['visual_data']=dati_custom[['Close','rendimento']].copy()
                            st.session_state['visual_data'].reset_index(inplace=True)
                            st.session_state['visual_data']['Close'] = st.session_state['visual_data']['Close'].apply(lambda x: f'{x:.2f}')
                            st.session_state['visual_data'].rename(columns={'Close':'chiusura $'},inplace=True)
                            st.session_state['visual_data']['rendimento'] = st.session_state['visual_data']['rendimento'].apply(lambda x: f'{x:.2f}%')
                            st.session_state['visual_data'].loc[0,'rendimento'] = " - "
                            st.session_state['visual_data']['Date'] = st.session_state['visual_data']['Date'].dt.strftime('%d-%m-%Y') 
                            st.session_state['visual_data'].set_index('Date',inplace=True)
                           
                            if st.session_state["nome_ticker"] == "SPY": 
                                st.markdown("<br><br>", unsafe_allow_html=True)
                                
                            st.dataframe(st.session_state['visual_data'])
            
            
                        
            
                    with col3:
                        
                         
                            fig = plt.figure(figsize=(12,7))  
                            plt.plot(st.session_state['dati_storici'].index, st.session_state['dati_storici']['rolling'],\
                                     label=f'Volatilità Rolling ({giorni*-1} giorni)', color="#4b58ff")  
                                
                            #plt.xlabel('Data')  
                            plt.ylabel('Volatilità %')  
                            plt.title(f'{st.session_state["nome_ticker"].upper()} Andamento della Volatilità Rolling')  
                            plt.legend()  
                            plt.grid()
                            plt.xticks(rotation=45)
                            st.pyplot(fig)
               

            
              
                
 
                
 
    
                                
                              
                            
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            background-color: #e0e0e0; /* Grigio chiaro neutro */
            padding: 6px;
        }
        .footer a {
            font-size: 12px; /* Scritta più piccola */
            text-decoration: none;
            color: blue; /* Puoi cambiare il colore del link se lo desideri */
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        <a href="https://gapfound.github.io/GAP_Finder_dipendent_files/disclaimer_volatility.html" target="_blank">Data Disclaimer</a>
    </div>
""", unsafe_allow_html=True)                              
                    
                        
                        
            
                
#%%


