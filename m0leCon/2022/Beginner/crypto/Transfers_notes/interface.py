header="""
|---------------------------|
| Welcome in Transfer-notes |
|---------------------------|
"""

main_menu = """
Available operations:
1) List users
2) List transactions
3) Login
4) Register
5) List transactions by user
6) Exit
"""

user_menu = """Available operations:
1) List users
2) List transactions
3) List my transactions
4) New transaction
5) List transactions by user
6) Exit
"""

#display borders
users_border = '|' + '-' * 73 + '|'
transactions_borders = '|' + '-' * 156 + '|'

# display headers
transaction = "[id] [receiver] <- [amount] | [description]"
users = users_border + "\n| userid username" + ' ' * 57 + '|\n' + users_border
transactions = transactions_borders + "\n| userid        id        |" + ' ' * 130 + '|\n' + transactions_borders
