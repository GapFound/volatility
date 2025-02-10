


import streamlit as st
import pathlib
import yfinance as yf
import numpy as np


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
    
    
    
    giorni = st.slider("**giorni**", 5, 252, step=1, value=10)  # Valore di default 10
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
                #st.session_state['giorni']=1
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
                    dati_custom = st.session_state['dati_storici'][giorni:].copy()
                    dati_custom['rendimento'] = (dati_custom['Close'].pct_change()) * 100
                    volatility = dati_custom['rendimento'].std()
                    st.session_state['volatility'] = volatility
                    volatility_ann = volatility*np.sqrt(252)
                    
                    
                    dati_storici_20 = st.session_state['dati_storici'][-20:].copy()
                    dati_storici_20['rendimento'] = (dati_storici_20['Close'].pct_change()) * 100
                    volatility_20 = (dati_storici_20['rendimento'].std())*np.sqrt(252)
                    
                    
                    dati_storici_30 = st.session_state['dati_storici'][-30:].copy()
                    dati_storici_30['rendimento'] = (dati_storici_30['Close'].pct_change()) * 100
                    volatility_30 = (dati_storici_30['rendimento'].std())*np.sqrt(252)
                    
                    
                    dati_storici_60 = st.session_state['dati_storici'].copy()
                    dati_storici_60['rendimento'] = (dati_storici_60['Close'].pct_change()) * 100
                    volatility_60 = (dati_storici_60['rendimento'].std())*np.sqrt(252)
                    
                    
                    st.markdown("<br>", unsafe_allow_html=True)

                        
                    st.markdown(f'Volatilità giornaliera **{nome_ticker.upper()}**\
                                    a **{giorni * -1}** giorni:&nbsp;&nbsp;**{volatility:.2f}%**')
                                    
                    st.markdown(f'Volatilità a **{giorni * -1}** giorni annualizzata:&nbsp;&nbsp;**{volatility_ann:.2f}%**')
                    st.markdown(f'Volatilità a **20** giorni annualizzata:&nbsp;&nbsp;**{volatility_20:.2f}%**')
                    st.markdown(f'Volatilità a **30** giorni annualizzata:&nbsp;&nbsp;**{volatility_30:.2f}%**')
                    st.markdown(f'Volatilità a **60** giorni annualizzata:&nbsp;&nbsp;**{volatility_60:.2f}%**')
                   
                    
                        
                
                        
                                 
                        
                 
                
                
                
                
                                
                        
                    
if st.session_state['ricerca_premuto']==True and st.session_state["nome_ticker"] == "SPY":
                    #col1, col2, col3 = st.columns([0.10, 0.40, 0.5])
                        
        with col2:
            
            col2a,col2b,col2c,col2d = st.columns([0.10,0.25,0.25,0.40])
            col2e,col2f = st.columns([0.10,0.9])
            
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
                       
                       
                    
                    
                
              
                                
                              
                            
    
                    
                        
                        
            
                
#%%


# import streamlit as st
# import pathlib
# import yfinance as yf
# import numpy as np


# col_1,col_2 = st.columns([0.5,0.5])

# nome_ticker = "SPY"

# ticker = yf.Ticker(nome_ticker.upper())
# dati_storici = ticker.history(period='1y')
# dati_custom = dati_storici[10:].copy()
# dati_custom['rendimento'] = (dati_custom['Close'].pct_change()) * 100
# volatility = dati_custom['rendimento'].std()



# with col_1:
#     if st.button('proviamo'):
        
            

#         if nome_ticker == "SPY":
#             with col_2:
                
#                 trade = st.text_input('**rischio per trade**',placeholder='value in $').strip()
                
#                 try:
#                     trade = float(trade)
#                 except ValueError:
#                     trade =""
                        
#                 if isinstance(trade,(int,float)):
#                     valore_attuale = dati_storici['Close'][-1]
#                     n_azioni = trade/((volatility/100)*valore_attuale)
                            
#                     st.markdown(f'azioni da acquistare:&nbsp;&nbsp;**{n_azioni:.2f}**')       


#%%



# import streamlit as st
# import yfinance as yf
# import numpy as np

# # Layout: due colonne
# col_1, col_2 = st.columns([0.5, 0.5])

# with st.form(key='VOLatiliTY_Calc'):
#     nome_ticker = st.text_input('**VOLatiliTY**', value="SPY", placeholder='Enter the Ticker').upper().strip()  # Default SPY
#     bottone_ricerca = st.form_submit_button('press to calc')

# #nome_ticker = "SPY"

# # Ottieni i dati storici del ticker
# ticker = yf.Ticker(nome_ticker.upper())
# dati_storici = ticker.history(period='1y')
# dati_custom = dati_storici[10:].copy()
# dati_custom['rendimento'] = (dati_custom['Close'].pct_change()) * 100
# volatility = dati_custom['rendimento'].std()

# # Variabile per verificare se è stato premuto il bottone
# if 'proviamo_premuto' not in st.session_state:
#     st.session_state['proviamo_premuto'] = False

# # Bottone per attivare il calcolo
# with col_1:
#     if bottone_ricerca:
#         st.session_state['proviamo_premuto'] = True

# # Condizione per mostrare l'input solo dopo il bottone
# if st.session_state['proviamo_premuto'] and nome_ticker=="SPY":
#     with col_2:
#         trade = st.text_input('**rischio per trade**', placeholder='value in $').strip()

#         try:
#             trade = float(trade) if trade else None
#         except ValueError:
#             trade = None

#         if isinstance(trade, (int, float)):
#             valore_attuale = dati_storici['Close'][-1]
#             n_azioni = trade / ((volatility / 100) * valore_attuale)
#             st.markdown(f'Azioni da acquistare:&nbsp;&nbsp;**{n_azioni:.2f}**')
#         else:
#             st.markdown('⚠️ Inserisci un numero valido per il rischio per trade.')
        

#%%


        
        
        
        
        
        
        
        
        
        
        

