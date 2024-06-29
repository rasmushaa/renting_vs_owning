import pandas as pd
import numpy as np


def __calculate_monthly_payment(P, T, r):
    '''Computes the monthly payment of Amortized loan

    Amortized loan is formed by individual monthly payments,
    that are generating monthly interest,
    meaning that the total principal P is a sum of this geometrical series,
    where initial value a = A / (1 + r)^1
    https://www.investopedia.com/terms/a/amortization.asp
    https://teachingcalculus.com/2015/02/09/amortization/

    Nominal Yearly interest rate is compounded monthly -> r/12.

    Parameters
    ----------
    P : int
        Principal of the loan
    T : int
        Maturity of the loan in years
    r : float
        Nominal annual interest rate (value that reads on the contract)
    '''
    t_months = T * 12
    r_monthly = r / 12
    A = P*r_monthly*(1 + r_monthly) ** t_months / ((1 + r_monthly) ** t_months - 1)
    return A

def generate_amortization_schedule(P, T ,r):
    yearly_payment = __calculate_monthly_payment(P, T ,r)
    schedule = []
    balance = P
    for month in range(1, T*12 + 1):
        interest_payment = balance * (r/12)
        principal_payment = yearly_payment - interest_payment
        balance -= principal_payment
        schedule.append({
                'Year' : np.ceil(month/12).astype(int),
                'Month': month,
                'Payment' : yearly_payment,
                'Principal' : principal_payment,
                'Interest' : interest_payment,
                'Balance' : balance     
            })
    return pd.DataFrame(schedule).round(0)


def generate_investment_schedule(initial_value, monthy_value, r_early, T):
    r_month = np.power(r_early + 1, 1/12)
    schedule = []
    balance = initial_value
    contributions = initial_value
    for month in range(1, T*12 + 1):
        balance = balance * r_month 
        balance = balance + monthy_value
        contributions += monthy_value
        schedule.append({
                'Year' : np.ceil(month/12).astype(int),
                'Month': month,
                'Contributions': contributions,
                'Interest': balance - contributions,
                'Balance': balance
            })
    return pd.DataFrame(schedule).round(0)