import streamlit as st
import numpy as np
from finance_math import *
import plotting as plots
from helpers import *


################## TITLE ######################
st.title('Is Renting an Apartment a Better Option for You? Find Out Now!')
st.markdown(f'''This application illustrates how your amortized mortgage payments will evolve over time according to your specified parameters. 
            It also compares the opportunity cost of invested capital with a specified return rate. For a more detailed discussion, 
            please read the accompanying article here <>.''')
st.divider()


################## SIDEBAR ######################
st.sidebar.header('Please, provide your own parameters for:')
st.sidebar.subheader('Apartment and Mortgage')
APARTMENT_PRICE = st.sidebar.number_input('Apartment purchasing price [$]', 1000, 10_000_000, 200_000, 10_000, key='1')
DOWN_PAYMENT = st.sidebar.number_input('Down Payment [$]', 1000, 10_000_000, 20_000, 10_000, key='2')
LOAN_AMOUNT = APARTMENT_PRICE - DOWN_PAYMENT
LOAN_TERM = st.sidebar.number_input('Mortgage Term [Years]', 1, 50, 20, 1, key='3')
INTEREST_RATE = st.sidebar.number_input('Interest rate [%]', 0.01, 50.00, 3.00, 0.5, key='4') / 100 # To actual percentages
APARTMENT_CONDO = st.sidebar.number_input('Condominium Fee / Maintenance [$]', 0, 10_000, 250, 100, key='8')
APARTMENT_RETURN = st.sidebar.number_input('Apartment price Return [%]', -50.00, 50.00, 0.50, 0.05, key='9') / 100

st.sidebar.subheader('Renting')
RENT = st.sidebar.number_input('Rent [$]', 100, 10_000, 1_000, 100, key='10')

st.sidebar.subheader('Investing and Horizont')
TIME_HORIZONT = st.sidebar.number_input('Time Horizont [Years]', 1, 100, 30, 1, key='6')
STOCK_RETURN = st.sidebar.number_input('Investments Return [%]', 0.01, 50.00, 7.00, 1.00, key='7') / 100


#@st.cache_data
def load_data():
    df = generate_amortization_schedule(P=LOAN_AMOUNT, T=LOAN_TERM, r=INTEREST_RATE)
    monthly_return = np.power(APARTMENT_RETURN + 1, 1/12)
    df['Apartment'] = np.cumprod(np.full(len(df), monthly_return)) * APARTMENT_PRICE
    df['Condominium'] = APARTMENT_CONDO
    return df


################# PAGES #################
df = load_data()

st.subheader('Mortgage and Apartment')
text = f'''Let's first consider the typical example of purchasing a house.  
If you are going to spend :red[**{money_to_string(APARTMENT_PRICE)}**] to a house :house:  
and you have already saved :green[**{money_to_string(DOWN_PAYMENT)}**] (which is about {APARTMENT_PRICE/DOWN_PAYMENT:.0f}%),  
you must appy for a loan of :red[**{money_to_string(APARTMENT_PRICE - DOWN_PAYMENT)}**] from the bank :bank:  
This is the *"Liabilites"* side on your *Balance Sheet* (so, for you it's actually negative),  
and assuming that your yearly interst rate is always a constant :red[**{INTEREST_RATE*100:.1f}%**]  
you will payoff the loan in :green[**{LOAN_TERM} years**] using Amortized loan payments,  
the liabilites will change as demonstrated in the image below'''
st.markdown(text)
plots.plot_balance_projection(df)


text = f'''Fortunetally, you are not throwing your money out of the window :money_with_wings:  
and you will also gain something when you purchase a house.  
:green[**The house has some positive value**] (that you will own despite of holding debt),   
which is the *"Asset"* side of the *Balance Sheet*.  
Assuming that the price will :green[**increase {APARTMENT_RETURN*100:.1f}% yearly**],  
your assets will increase as follows'''
st.markdown(text)
plots.plot_apartment_return(df)


text = f'''Now, when the :red[*Liabilites*] and the :green[*Assets*] are plotted together,  
on the correct sides of the Balance Sheet,  
you can see your :orange[**Net Assets**] and how those are cumulating :chart_with_upwards_trend: '''
st.markdown(text)
plots.plot_apartment_net_assets(df)


def p_vs_i():
    index = df.loc[df['Principal'] > df['Interest']].index.min()
    if index > 0:
        return f'\\\n(and actually the :green[*Principal*] is greater than the :red[*Interest*] only after {index} months),\\'
    else:
        return '\\'
    
text = f'''The :orange[**Net Assets**] are increasing due to the rising housing market and   
mandated negative cash flow towards the loan, which is formed by the  
:grey[**{money_to_string(float(APARTMENT_CONDO))} Condominium Fee**] (charged as long as you own the house),  
the :green[**Principa Payment**] :green[**{money_to_string(df['Principal'][0])}**], and the :red[**Loan Interest**] :red[**{money_to_string(df['Interest'][0])}**] in the beginning.  
The Interest and Principal values are changing during the time,{p_vs_i()}
but the sum is always a constant and it will cost :red[**{money_to_string(APARTMENT_CONDO + df['Interest'][0] + df['Principal'][0])} in total every month.**]  
'''
st.markdown(text)
plots.plot_payment(df)


st.subheader('Renting and Investing')
df_invest = generate_investment_schedule(DOWN_PAYMENT, APARTMENT_CONDO + df['Interest'][0] + df['Principal'][0] - RENT, STOCK_RETURN, LOAN_TERM)
text = f'''Imagine you have the option to rent the same house you are considering to purchase for :red[**{money_to_string(RENT)}**] per month.
This rental amount provides you with :green[**{money_to_string((APARTMENT_CONDO + df['Interest'][0] + df['Principal'][0]) - RENT)} more in Free Cash Flow**]  
compared to owning the same house.  
While paying rent is typically viewed as an expense that doesn't build equity :money_with_wings:,   
strategic financial planning can turn this into a profitable scenario.  
Instead of simply pocketing the additional money under your bed :bed: each month,   
you decide to invest this surplus into the stock market :chart_with_upwards_trend:, targeting an average annual return of :green[**{STOCK_RETURN*100:.1f}%**].  
And you don't have to even start from nothing since you will still have the inital :green[**{money_to_string(DOWN_PAYMENT)}!**]  
\\
Doing this, will generate you a net fortuen of :green[**{money_to_string(df_invest['Balance'].iloc[-1])}**] before taxes,  
compared to :green[**{money_to_string(df['Apartment'].iloc[-1])}**] from owning the house.

However, this example does not consider that also the house owner can invest the excess money after fully paying of the loan,  
and there are taxation procedures for realizifing capital gains. Let's also consdider these parameters in the next demonstration.
'''
st.markdown(text)
plots.plot_renting_net_assets(df_invest)