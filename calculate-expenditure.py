import matplotlib.pyplot as plt
import numpy as np

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
annual_contrib = lambda yr: 6000 if yr < 2022 + 50 else 7000
roth_acc = [6000 * (1 + return_rate)]

# value of accounts
starting_salary_raw = 55000
income = [starting_salary_raw * (1 - tax_rate)]
bond_portfolio = [bond_contrib * (1 + bond_interest_rate)]

for t in range(start_yr + 1, end_yr + 1):
    # calculate and add income
    income.append((1 - tax_rate) * starting_salary_raw * (1 + inflation_rate) ** (t - start_yr))
    # calculate roth IRA portfolio
    roth_acc.append(annual_contrib(t) * ((1 + return_rate) ** (t - start_yr) - 1) / return_rate)
    # calculate bond portfolio and apply income tax deduction
    new_bond_amt_raw = bond_contrib * ((1 + bond_interest_rate) ** (t - start_yr) - 1) / bond_interest_rate
    prev_bond_portfolio = bond_portfolio[len(bond_portfolio) - 1]
    new_bond_amt = prev_bond_portfolio + (1 - tax_rate) * (new_bond_amt_raw - prev_bond_portfolio)
    # add to portfolio
    bond_portfolio.append(new_bond_amt)

x_ax = np.arange(start_yr, end_yr + 1)

print('Final -> [Income: %d, Roth IRA: %d, Investments: %d]' % (income[len(income) - 1], roth_acc[len(roth_acc) - 1], bond_portfolio[len(bond_portfolio) - 1]))

plt.xlabel('Year')
plt.ylabel('Returns')
plt.title('Investments and Expenses over a Lifetime')

plt.plot(x_ax, roth_acc)
plt.plot(x_ax, bond_portfolio)
plt.show()

print(income)