FLAG = "byuctf{}"

class User:
    def __init__(self, username, id):
        self.username = username
        self.id = id
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
ADMIN = User('admin', 1337)

print("Welcome to onboarding! I'm Jacob from HR, and I'm here to make your experience as seamless as possible joining the company")
print("Go ahead and tell me your name:")
name = input()
print("Welcome to the company, " + name)
print("We also give you a user id, but in an attempt to make this company feel like home, we've decided to give you a choice in that, too. Go ahead and choose that now:")
id_ = input()
if not all([i in '0987654321' for i in id_]):
    print("That's not an id!")
    quit()
id_ = int(id_)
if id_ == 1337:
    print("Sorry, the admin already claimed that id, no can do")
    quit()
YOURUSER = User(name, id_)
print("Okay, you're all set! Just head into your office. The admin's is right next door, but you can just ignore that")
print("""*You realize you have freedom of choice. Choose a door*
      1) your office
      2) the admin's office
""")
choice = int(input())
if choice == 1:
    if hash(YOURUSER) == hash(YOURUSER):
        print("Man, this is a nice office")
        quit()
    else:
        print("Hey, HR, my key doesn't work yet!")
        quit()
elif choice == 2:
    if hash(YOURUSER) == hash(ADMIN):
        print(FLAG)
        quit()
    else:
        print("The HR guy tackles you to the ground for insolence")
        quit()

