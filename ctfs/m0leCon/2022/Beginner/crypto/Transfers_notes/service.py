import interface
import utils

def validate(username: str, new=False):
    valid = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if len(username) == 0:
        print("Cancelling operation...")
        return True
    elif not (3 <= len(username) <= 64):
        print("Invalid username: length must be at least 3 and at most 64")
        return False
    elif any(c not in valid for c in username):
        print("Invalid username: only letters and digits allowed")
        return False
    elif (not new) and username not in utils.users():
        print("Username not in list")
        return False
    return True

def login():
    username = input('Insert username (only letters and digits): ').strip()
    while not validate(username):
        username = input('Insert username (only letters and digits): ').strip()
    if username == '':
        return None, None
    
    password = input('Insert password: ').strip()
    return utils.login(username, password)

def register():
    username = input('Insert username (only letters and digits): ').strip()
    while not validate(username, new=True):
        username = input('Insert username (only letters and digits): ').strip()
    if username == '':
        return None, None
    
    password = input('Insert password: ').strip()
    return utils.register(username, password)

def show_users():
    print(interface.users)
    users = utils.users()
    users.sort(key=lambda e: int(utils.Ids[e], 16))
    for user in users:
        print(f'| {utils.Ids[user]} {user:64} |')
    print(interface.users_border)

def show_transactions(username=None, password=None):
    print(interface.transactions)
    for userid, timestamp, transaction in utils.transactions(username, password):
        if len(transaction) > 128:
            t = transaction[:125] + '...'
        else:
            t = transaction
        print(f'| {userid} {int(timestamp):0>16x} | {t:128} |')
    print(interface.transactions_borders)

def show_transactions_of(user: str, username=None, password=None):
    print("Transactinos of", user)
    print(interface.transaction)
    p = 0
    if user == username:
        psw = password
    else:
        psw = None
    data = utils.Users[user].read_transactions(psw)
    for timestamp in data:
        transaction = data[timestamp]
        print(f'[{int(timestamp):0>16x}] {transaction}')
        p += 1
    if p == 0:
        print('No transaction found')

def main_menu():
    print(interface.main_menu)
    choice = input('> ').strip()
    while choice not in ('1', '2', '3', '4', '5', '6'):
        print("Invalid choice (must be one of '1', '2', '3', '4', '5', '6')")
        choice = input('> ').strip()
    
    if choice == '1':
        show_users()
    elif choice == '2':
        show_transactions()
    elif choice == '3':
        return login()
    elif choice == '4':
        return register()
    elif choice == '5':
        user = input('Insert username (only letters and digits): ').strip()
        while not validate(user):
            user = input('Insert username (only letters and digits): ').strip()
        if user != '':
            show_transactions_of(user)
    else:
        raise SystemExit()
    
    return None, None

def user_menu(username: str, password: str):
    print(f'\n[{username}] ' + interface.user_menu)
    choice = input('> ').strip()
    while choice not in ('1', '2', '3', '4', '5', '6'):
        print("Invalid choice (must be one of '1', '2', '3', '4', '5', '6')")
        choice = input('> ').strip()

    if choice == '1':
        show_users()
    elif choice == '2':
        show_transactions(username, password)
    elif choice == '3':
        show_transactions_of(username, username, password)
    elif choice == '4':
        receiver = input('Receiver: ').strip()
        while receiver not in utils.users():
            if receiver == '':
                print("Cancelling operation...")
                return username, password
            print("Receiver not in user\'s list...")
            receiver = input('Receiver: ').strip()
        amount = input('Amount: ').strip()
        while any(c not in '0123456789' for c in amount) or (len(amount) != 1 and amount[0] == '0') or len(amount) > 10:
            print("The amount must be an integer value with up to 10 digits...")
            amount = input('Amount: ').strip()
        amount = int(amount)
        description = input('Insert description: ').strip()
        utils.Users[username].new_transaction(password, amount, receiver, description)
    elif choice == '5':
        user = input('Insert username (only letters and digits): ').strip()
        while not validate(user):
            user = input('Insert username (only letters and digits): ').strip()
        if user != '':
            show_transactions_of(user, username, password)
    else:
        return None, None

    return username, password

def main():
    user = (None, None)
    print(interface.header)
    while True:
        try:
            if user == (None, None):
                user = main_menu()
            else:
                user = user_menu(*user)
        except SystemExit:
            print("Quitting...")
            utils.save_all()
            exit()
        except Exception as e:
            print("Unknown issue...", e)
            utils.save_all()
            exit()

if __name__ == "__main__":
    main()