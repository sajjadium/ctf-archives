import random
from faker import Faker
from main import db,User
faker=Faker()
hexc=[]
for i in range(16):
    hexc.append(hex(i)[2:])
for i in range(50):
    random.shuffle(hexc)
passwords=[]
lucky=random.randint(100,400)
f=open('users.txt','w')
for i in range(500):
    random.shuffle(hexc)
    passwords.append("".join(hexc))
    name=faker.name()
    phone=faker.phone_number()
    if phone[0]!='+':
        phone='+'+phone
    if i == lucky:
        name='Adm1n_h3r3_UwU'
    f.write(name+'||'+passwords[i]+'||'+faker.address().replace('\n',', ')+'||'+phone+'||'+faker.email())
    f.write('\n')
f.close()

def create_db():
    f=open('users.txt','r').read()
    users=f.split('\n')
    for usr in users:
        if usr=='':
            break
        username=usr.split('||')[0]
        password=usr.split('||')[1]
        address=usr.split('||')[2]
        phone=usr.split('||')[3]
        email=usr.split('||')[4]
        user= User(name=username,
                age=random.randint(20,80),
                address=address,
                phone=phone,
                email=email,
                password=password)
        db.session.add(user)
    db.session.commit()

create_db()


