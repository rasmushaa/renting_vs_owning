import streamlit as st
import numpy as np
from finance_math import *
import plotting as plots
from helpers import *


################## TITLE ######################
st.title('Is Renting an Apartment a Better Option for You? Find Out Now!')
st.markdown(f'''This application illustrates how your amortized mortgage payments will evolve over  
            time according to your specified parameters.   
            It also compares the opportunity cost of invested capital with a specified return rate.   
            For a more detailed discussion, please read the accompanying article <>.''')
st.divider()


################## SIDEBAR ######################
st.sidebar.header('Please, provide your own parameters for:')
st.sidebar.subheader('Apartment and Mortgage')
APARTMENT_PRICE = st.sidebar.number_input('Apartment purchasing price [$]', 1000, 10_000_000, 175_000, 10_000, key='1')
DOWN_PAYMENT = st.sidebar.number_input('Down Payment [$]', 1000, 10_000_000, 17_500, 1_000, key='2')
LOAN_AMOUNT = APARTMENT_PRICE - DOWN_PAYMENT
LOAN_TERM = st.sidebar.number_input('Mortgage Term [Years]', 1, 50, 25, 1, key='3')
INTEREST_RATE = st.sidebar.number_input('Interest rate [%]', 0.01, 50.00, 4.50, 0.5, key='4') / 100 # To actual percentages
APARTMENT_CONDO = st.sidebar.number_input('Condominium Fee / Maintenance [$]', 0, 10_000, 220, 100, key='8')
APARTMENT_RETURN = st.sidebar.number_input('Apartment price Return [%]', -50.00, 50.00, 0.50, 0.05, key='9') / 100
APARTMENT_TAX = st.sidebar.number_input('Apartment Gain Tax[%]', 0.00, 100.00, 0.00, 1.00, key='11') / 100

st.sidebar.subheader('Renting')
RENT = st.sidebar.number_input('Rent [$]', 100, 10_000, 850, 100, key='10')

st.sidebar.subheader('Investing and Horizont')
TIME_HORIZONT = st.sidebar.number_input('Time Horizont [Years]', 1, 100, 5, 1, key='6')
STOCK_RETURN = st.sidebar.number_input('Investments Return [%]', 0.01, 50.00, 7.00, 1.00, key='7') / 100
STOCK_TAX = st.sidebar.number_input('Capital Asset Gain Tax[%]', 0.00, 100.00, 30.00, 1.00, key='12') / 100


################# PAGES #################
df = generate_amortization_schedule(P=LOAN_AMOUNT, T=LOAN_TERM, r=INTEREST_RATE)
monthly_return = np.power(APARTMENT_RETURN + 1, 1/12)
df['Apartment'] = np.cumprod(np.full(len(df), monthly_return)) * APARTMENT_PRICE
df['Condominium'] = APARTMENT_CONDO

st.subheader('Mortgage and Apartment')
text = f'''Let's first consider the typical example of purchasing a house.\\
Suppose you plan to buy a house :house: for :red[**{money_to_string(APARTMENT_PRICE)}**].\\
You have already saved :green[**{money_to_string(DOWN_PAYMENT)}**] (which is about {DOWN_PAYMENT/APARTMENT_PRICE*100:.0f}% of the purchase price)\\
This down payment means you need to apply for a loan of :red[**{money_to_string(APARTMENT_PRICE - DOWN_PAYMENT)}**] from the bank :bank:  
which represents the :red[*Liabilities*] side of your **Balance Sheet**.\\
For you, this is a liability, which is a negative value, as it is the amount you owe to the bank.\\
Assuming that your yearly interest rate remains constant at :red[**{INTEREST_RATE*100:.1f}%**]  
and you will pay off the loan over :green[**{LOAN_TERM} years**] using *Amortized* loan payments,\\
the outstanding loan balance will change over time as demonstrated in the image below:'''
st.markdown(text)
plots.plot_balance_projection(df)


text = f'''Fortunately, you are not throwing your money out of the window :money_with_wings: when you purchase a house.\\
Instead, :green[**you gain a valuable asset**] that contributes positively to your financial portfolio.\\
This asset, which you will own despite holding debt, is recorded on the :green[**Asset side**] of your **Balance Sheet**.\\
When you purchase a house, its initial value is the price you paid for it.\\
Over time, as property values typically appreciate, the value of your house is likely to increase.\\
Assuming a modest annual appreciation rate of :green[**increase {APARTMENT_RETURN*100:.1f}% yearly**],\\
your house's value will grow, thereby increasing your total assets as follows:'''
st.markdown(text)
plots.plot_apartment_return(df)


text = f'''Now that we have examined both the :red[*Liabilites*] and the :green[*Assets*] associated with owning a house,\\
    we can plot these together on the correct sides of the **Balance Sheet**.\\
    This will help us visualize your :orange[**Net Assets**] **(**:green[*Assets*]**-**:red[*Liabilites*]**)** and how they accumulate over time :chart_with_upwards_trend:
    '''
st.markdown(text)
plots.plot_apartment_net_assets(df)


text = f'''Owning a house involves various **Cash Flows** that contribute to both liabilities and assets.\\
    Understanding these cash flows is crucial to grasping how your :orange[**Net Assets**] increase over time.\\
    Here, we will break down the different components of the cash flow involved in owning a house.\\
    \\
    **- {money_to_string(float(APARTMENT_CONDO))} Condominium Fee**: *A fixed monthly fee charged as long as you own the house.*\\
    :green[**- Principa Payment {money_to_string(df['Principal'][0])}**]: *The sum dedicated to payoff the loan*\\
    :red[**- Loan Interest {money_to_string(df['Interest'][0])}**]: *The cumulated interst since the last payment*\\
    :red[**- Total Monthly Cost {money_to_string(APARTMENT_CONDO + df['Interest'][0] + df['Principal'][0])}**]: *The sum of the Condominium Fee, Principal Payment, and Loan Interest.*\\
    \\
    While the total mortgage payment remains constant,\\
    the distribution between :green[*Principal*] and :red[*Interest*] changes.\\
    The Principal Payment gradually increases, while the Loan Interest decreases.\\
    This change happens because as you pay off the loan, the interest is calculated on a lower remaining balance.\\
    \\
    Note, the Condominium fee is likley to increase with a relation to the house price, but it's not considered in this simplifed example.
'''
st.markdown(text)
plots.plot_payment(df)




st.subheader('Renting and Investing')
fcf_rent = APARTMENT_CONDO + df['Interest'][0] + df['Principal'][0] - RENT
df_invest = generate_investment_schedule(DOWN_PAYMENT, fcf_rent, STOCK_RETURN, LOAN_TERM)
df_invest['NetAssets'] = df_invest['Balance']
text = f'''Imagine you have the option to rent the same house you are considering to purchase for :red[**{money_to_string(RENT)}**] per month (in the reality, the rent cost is likley to increase, but it's not considered in this simplifed example).
This rental amount provides you with :green[**{money_to_string(fcf_rent)} more in Free Cash Flow**] compared to owning the same house.\\
While paying rent is typically viewed as an expense that doesn't build equity :money_with_wings:,   
strategic financial planning can turn this into a profitable scenario.  
Instead of simply pocketing the additional money under your bed each month :bed:,   
you decide to invest this surplus into the stock market :chart_with_upwards_trend:, targeting an average :green[**annual return of {STOCK_RETURN*100:.1f}%**].  
Additionally, you start with an initial investment of :green[**{money_to_string(DOWN_PAYMENT)}**], the amount you would have used for a down payment.\\
\\
By renting and investing the excess cash flow,\\
you could potentially generate a net fortune of :green[**{money_to_string(df_invest['Balance'].iloc[-1])}**] before taxes.\\
In comparison, owning the house might result in a net worth of :green[**{money_to_string(df['Apartment'].iloc[-1])}**] due to property appreciation and equity buildup.\\
\\
*This example does not consider that the house owner can also invest excess money after fully paying off the loan. 
Additionally, there are taxation procedures for realizing capital gains,
which can affect the final outcomes.
These factors are considered in the more comprehensive analysis.*
'''
st.markdown(text)
plots.plot_renting_net_assets(df_invest)



st.subheader('Longer Timehorizont with Taxes')
df = pd.DataFrame()
df_loan = generate_amortization_schedule(P=LOAN_AMOUNT, T=LOAN_TERM, r=INTEREST_RATE)
fcf = df_loan['Interest'][0]+df_loan['Principal'][0]
df_invest = generate_investment_schedule(0, fcf, STOCK_RETURN, TIME_HORIZONT)
df['Month'] = np.arange(0, len(df_loan)+len(df_invest))
df['Year'] = np.ceil(df['Month']/12).astype(int)
df['Balance'] = np.pad(df_loan['Balance'], (0, len(df_invest )), 'constant', constant_values=(0, 0))
df['Contributions'] = np.pad(df_invest['Contributions'], (len(df_loan), 0), 'constant', constant_values=(0, 0))
df['Interest'] = np.pad(df_invest['Interest'], (len(df_loan), 0), 'constant', constant_values=(0, 0))
df['Apartment'] = APARTMENT_PRICE
monthly_return = np.power(APARTMENT_RETURN + 1, 1/12)
df['ApartmentGain'] = np.cumprod(np.full(len(df), monthly_return)) * APARTMENT_PRICE - APARTMENT_PRICE
df['NetAssets'] = df['Apartment'] + df['ApartmentGain'] + df['Contributions'] + df['Interest']-df['Balance']
df.iloc[-1] = [(LOAN_TERM+TIME_HORIZONT)*12+12, 
               (LOAN_TERM+TIME_HORIZONT)+1, 
               0, # Balance
               0, # Contributions
               0, # Interest
               0, # Apartment
               0, # ApartmentGain
               df['NetAssets'].iloc[-1] - df['ApartmentGain'].iloc[-1]*APARTMENT_TAX - df['Interest'].iloc[-1]*STOCK_TAX]

text = f'''After fully paying off the mortgage,\\
a house owner can also benefit from investing the :green[**Surplus Cash Flow of {money_to_string(fcf)}**].\\
Let's consider an extended period of {LOAN_TERM+TIME_HORIZONT} years after the mortgage is paid off,\\
during which the house owner invests this additional cash flow to the stock market :chart_with_upwards_trend:\\
At the end of this period, **all assets will be sold**,\\
and **taxes on** :green[*capital gains*] :red[**{STOCK_TAX*100:.1f}%**] and on :green[*apartment gains*] :red[**{APARTMENT_TAX*100:.1f}%**] **will be realized**.\\
This will decreased the generated :orange[**Net Assets**] from :green[**{money_to_string(df['NetAssets'].iloc[-2])}**] to :green[**{money_to_string(df['NetAssets'].iloc[-1])}**]
'''
st.markdown(text)
plots.plot_apartment_net_assets_with_investing(df)



df_invest = generate_investment_schedule(DOWN_PAYMENT, fcf_rent, STOCK_RETURN, LOAN_TERM+TIME_HORIZONT)
df_invest['NetAssets'] = df_invest['Contributions'] + df_invest['Interest']
df_invest.iloc[-1] = [(LOAN_TERM+TIME_HORIZONT)+1, 
               (LOAN_TERM+TIME_HORIZONT)*12+12, 
               0, # Contributions
               0, # Interest
               0, # Balance
               df_invest['NetAssets'].iloc[-1] - df_invest['Interest'].iloc[-1]*STOCK_TAX]

text = f'''By renting and investing the excess cash of :green[**{money_to_string(fcf_rent)}**] flow over a **{(LOAN_TERM+TIME_HORIZONT)}-year period**,\\
you could potentially accumulate significant wealth :moneybag:\\
After accounting for :red[**capital gains tax**] as in the previous part,\\
the generated :orange[**Net Assets**] will decreased  from :green[**{money_to_string(df_invest['NetAssets'].iloc[-2])}**] to :green[**{money_to_string(df_invest['NetAssets'].iloc[-1])}**]
but provides still a clear picture of the financial benefits of this strategy.'''
st.markdown(text)
plots.plot_renting_net_assets(df_invest)



def str_help(own_net, rent_net):
    if own_net > rent_net:
        return f'''**Owning the apartment :house: would be more profitable**\\
            by generating :green[**{money_to_string(own_net)}**] after the taxes, compared to :red[**{money_to_string(rent_net)}**] by renting it.'''
    else:
        return f'''**Renting the apartment :house: would be more profitable**\\
              by generating :green[**{money_to_string(rent_net)}**] after the taxes, compared to :red[**{money_to_string(own_net)}**] by owning it.'''
    
st.subheader('Comparison')
text = f'''Both scenarios have their benefits.\\
    Owning a house offers stability and potential property appreciation,\\
    while renting and investing provide higher flexibility and potential for greater financial returns,\\
    particularly when excess cash flow is invested wisely.\\
    \\
    **Individual preferences, financial goals, and market conditions should guide the decision between these two strategies**, although, using your inputs:\\
    \\
    {str_help(df['NetAssets'].iloc[-1], df_invest['NetAssets'].iloc[-1])}'''
st.markdown(text)
plots.plot_summary(df, df_invest)

