import matplotlib.pyplot as plt
import numpy as np
import latextable
from texttable import Texttable
import math

# parameters for the simulation
start_yr = 2022
end_yr = 2022 + (68 - 25)
tax_rate = 0.3
inflation_rate = 0.01

income = 55 * 10 ** 3
bond_interest_rate = 0.0712
bond_contrib = 10000

# ROTH IRA params
return_rate = 0.07
annual_contrib = 6000
roth_acc = [6000 * (1 + return_rate)]

# params for savings accs
savings_return = 0.005
annual_saving_add = 5500
savings_acc = [5500 * (1 + savings_return)]

# params for the s&p, conservative return rates at a fixed average
annual_stock_share = 5500
sandp_return = 0.105
stock_portfolio = [5500 * (1 + sandp_return)]

# CALCULATE MONTHLY EXP'END'ITURE 
def expenditures():
    # define dict lists of the different monthly costs and the exp'end'iture timelines
    personal_budget = [
        {'name': 'Food', 'cost': 150, 'start': start_yr, 'end': math.inf, 'period': 'monthly'},
        {'name': 'Rent', 'cost': 540, 'start': start_yr, 'end': start_yr + 3, 'period': 'monthly'},
        {'name': 'Utilities', 'cost': 140, 'start': start_yr, 'end': math.inf, 'period': 'monthly'},
        {'name': 'Life insurance', 'cost': 15, 'start': start_yr, 'end': math.inf, 'period': 'monthly'},
        {'name': 'General insurance', 'cost': 290.45, 'start': start_yr, 'end': math.inf, 'period': 'yearly'},
        {'name': 'Mortgage', 'cost': 730, 'start': start_yr + 4, 'end': math.inf, 'period': 'monthly'},
        {'name': 'Gas', 'cost': 550, 'start': start_yr + 3, 'end': math.inf, 'period': 'yearly'},
        {'name': 'Car insurance', 'cost': 950, 'start': start_yr + 3, 'end': math.inf, 'period': 'yearly'}
    ]
    
    investment_deposits = [
        {'name': 'Roth IRA contrib', 'cost': 500, 'start': start_yr, 'end': math.inf, 'period': 'monthly'},
        {'name': 'Savings account contrib', 'cost': 5500, 'start': start_yr, 'end': math.inf, 'period': 'yearly'},
        {'name': 'Bond purchases', 'cost': 11000, 'start': start_yr + 5, 'end': math.inf, 'period': 'yearly'},
        {'name': 'Stock share purchases', 'cost': 5500, 'start': start_yr, 'end': math.inf, 'period': 'yearly'}
    ]
    
    one_time_costs = [
        {'name': 'Down payment', 'cost': 4875, 'start': start_yr + 4, 'end': start_yr + 4, 'period': 'yearly'},
        {'name': 'Car purchase', 'cost': 7500, 'start': start_yr + 3, 'end': start_yr + 3, 'period': 'yearly'}
    ]
    
    monthly_expenditure_table = Texttable()
    monthly_expenditure_table.set_cols_align(['l'] + ['c'] * 4)
    monthly_expenditure_table.add_row(['\\textbf{Item}', '\\textbf{Cost}', '\\textbf{Start}', '\\textbf{End}', '\\textbf{Period}'])
    
    for item in personal_budget + investment_deposits + one_time_costs:
        monthly_expenditure_table.add_row([item['name'], item['cost'], item['start'], 'Indefinite' if item['end'] == math.inf else item['end'], item['period']])
        
    print(latextable.draw_latex(monthly_expenditure_table))
    
    # return everything
    return personal_budget + investment_deposits + one_time_costs

# RUN THE MASTER SIMULATION
def run_simulation():
    # value of accounts
    starting_salary_raw = 55000
    income = [starting_salary_raw * (1 - tax_rate)]
    bond_portfolio = [bond_contrib * (1 + bond_interest_rate)]
    
    budget = expenditures()
    
    for t in range(start_yr + 1, end_yr + 1):
        # calculate and add income (TAXED)
        income.append((1 - tax_rate) * starting_salary_raw * (1 + inflation_rate) ** (t - start_yr))
        
        # calculate roth IRA portfolio (UNTAXED)
        roth_acc.append(annual_contrib * ((1 + return_rate) ** (t - start_yr) - 1) / return_rate)
        
        # calculate bond portfolio and apply income tax deduction (TAXED)
        new_bond_amt_raw = bond_contrib * ((1 + bond_interest_rate) ** (t - start_yr) - 1) / bond_interest_rate
        prev_bond_portfolio = bond_portfolio[len(bond_portfolio) - 1]
        new_bond_amt = prev_bond_portfolio + (1 - tax_rate) * (new_bond_amt_raw - prev_bond_portfolio)
        bond_portfolio.append(new_bond_amt)
        
        # stocks and savings tracking logic
        new_stock_val_raw = annual_stock_share * ((1 + sandp_return) ** (t - start_yr) - 1) / sandp_return
        prev_stock_val = stock_portfolio[len(stock_portfolio) - 1]
        new_stock_val = prev_stock_val + (1 - tax_rate) * (new_stock_val_raw - prev_stock_val)
        stock_portfolio.append(new_stock_val)
        
        new_saving_val_raw = annual_saving_add * ((1 + savings_return) ** (t - start_yr) - 1) / savings_return
        prev_saving_val = savings_acc[len(savings_acc) - 1]
        new_saving_val = prev_saving_val + (1 - tax_rate) * (new_saving_val_raw - prev_saving_val)
        savings_acc.append(new_saving_val)
        
        # subtract the montly costs based on logic from the latest income array entry
        expenditure_curr = 0
        for item in budget:
            if t >= item['start'] and t <= item['end']:
                expenditure_curr += (1 if item['period'] == 'yearly' else 12) * item['cost']

        # print(income[len(income) - 1], expenditure_curr, income[len(income) - 1] - expenditure_curr)
        if t == start_yr + 5:
            print('Emergency fund total -> %d' % (new_stock_val + new_saving_val))
        income[len(income) - 1] -= expenditure_curr

    x_ax = np.arange(start_yr, end_yr + 1)

    plt.xlabel('Year')
    plt.ylabel('Amount')
    plt.title('Investments and Expenses over a Lifetime')

    plt.plot(x_ax, roth_acc, label='Roth IRA')
    plt.plot(x_ax, bond_portfolio, label='Series I Savings Bond')
    plt.plot(x_ax, savings_acc, label='Savings Account (Emergency Fund)')
    plt.plot(x_ax, stock_portfolio, label='S&P 500 Stock Portfolio')
    
    plt.legend()
    
    last_elem_idx = len(roth_acc)-1
    
    print('Final Worth of Assets')
    print('---------------------')
    amts = [roth_acc[last_elem_idx], bond_portfolio[last_elem_idx], stock_portfolio[last_elem_idx], savings_acc[last_elem_idx]]
    print('[Roth IRA = %d, Series I Bond = %d, Stock Portfolio = %d, Savings Account = %d | TOTAL = %d]' % (*amts, sum(amts)))
    
    plt.show()
    
if __name__ == '__main__':
    run_simulation()