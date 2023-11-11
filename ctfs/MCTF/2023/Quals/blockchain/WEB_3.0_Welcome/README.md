katok

kat.ok@disroot.org
Web 3 WELCOME | RU

Задание висит по адресу:

nc mctf-game.online 53131

Данный таск создан для ознакомления с категорией и платформой, которая предоставляет уязвимые контракты.
Как решить
1. Получить тикет

Пройдите в профиль вашей команды, скопируйте тикет. В будущем он понадобиться для получения своей копии задания.

**!!! ВАЖНО - НИКОМУ НЕ ПЕРЕДАВАЙТЕ СВОЙ ТИКЕТ!!!

Последствия необратимы, пощады не будет.**
2. Скачать и проанализировать файлы

В прикрепленных файлах вы имеете два файла. Что они делают:

    Setup.sol - контракт-деплоер, демонстрирует каким именно образом будет создан уязвимый контракт и по какому правилу он будет считаться решённым.
    Chal.sol - уязвимый контракт, название будет не обязательно именно таким. Именно его вам предстоит ломать.

Ваша задача добиться от уязвимого контракта такого состояния,при котором он будет считаться как решённый контрактом-деплоером.

В данном случае всё просто - надо вызвать функцию solve() контракта Chal
3. Создать свою копию задания

Пройдите по ncat порту, указанному в описании задания

Там вас встретит простой интерфейс с тремя пунктами:

    Создать копию
    Уничтожить копию
    Получить флаг

Каждое из действий запрашивает тикет, который вы получили на платформе.

После создания копии задания вы получаете информацию о созданной копии, которая пригодится для дальнейшего решения:

$ nc mctf-game.online 53131
1 - launch new instance
2 - kill instance
3 - get flag
action? 1
ticket please: ticket


your private blockchain has been deployed
it will automatically terminate in 30 minutes
here's some useful information
uuid:           12341234-12341234-12341234
rpc endpoint:   http://51.250.18.216:58545/12341234-12341234-12341234")
private key:    0xabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd
setup contract: 0x1234123412341234123412341234123412341234

    UUID - идентификатор вашей копии задания
    Адрес JSON-RPC клиента, по которому вы можете взаимодействовать с своим инстансом задания и с блокчейном.
    Приватный ключ от вашего аккаунта
    Адрес вашего аккаунта
    Адрес контракта-деплоера - в данном случае адрес контракта Setup

Рекомендую поместить все эти значения в переменные окружения вашего терминала т.к. они вам ещё понадобятся.
4. Получить флаг

После успешного выполнения задания Setup.sol контракт будет отдавать вам true в функции isSolved(). Теперь вам достаточно вернуться к сервису на ncat порту из третьего пункта и там выбрать получение флага.

Если всё сделали правильно - получите флаг, который сможете сдать в карточке таска в форме ниже.
Web 3 WELCOME | EN

The task hangs at:

nc mctf-game.online 53131.

This task is created to familiarize you with the category and platform that provides vulnerable contracts.
How to solve
1. Get a ticket

Go to your team profile, copy the ticket. You will need it to get your own copy of the task in the future.

**!!! IMPORTANT - DO NOT GIVE YOUR TICKET TO ANYONE!!!

The consequences are irreversible, there will be no mercy.
2. Download and analyze the files

In the attachments you have two files. What they do:

    Setup.sol - contract-deployer, demonstrates exactly how the vulnerable contract will be created and by what rule it will be considered as solved.
    Chal.sol - vulnerable contract, the name will not necessarily be the same. It is the one you will have to pwn.

Your task is to make contract-deployer ( Setup.sol ) mark vulnerable contract as a solved.

In this case everything is simple - you need to call the solve() function of the Chal contract.
3. Create your own copy of the task

Go to the ncat port specified in the task description

There you will be greeted by a simple interface with three items:

    Launch new instance
    Destroy instance
    Retrieve a flag

Each of the actions requests a ticket that you have received in above steps.

When you create an instance, useful information is displayed. This will come in handy for further solution:

$ nc mctf-game.online 53131
1 - launch new instance
2 - kill instance
3 - get flag
action? 1
ticket please: ticket


your private blockchain has been deployed
it will automatically terminate in 30 minutes
here's some useful information
uuid: 12341234-12341234-12341234
rpc endpoint: http://51.250.18.216:58545/12341234-12341234-12341234")
private key: 0xabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd
setup contract: 0x1234123412341234123412341234123412341234123412341234123412343434

    UUID is the identifier of your copy of the task
    The JSON-RPC client address where you can communicate with your job instance and the blockchain.
    The private key of your account
    The address of your account
    The address of the contract-deployer - the address of the Setup contract

I recommend that you put all these values in the environment variables of your terminal because you will need to reuse them.
4. Get the flag

After successful completion of the Setup.sol task, the contract will give you true in the isSolved() function. Now all you have to do is go back to the service on the ncat port from the third item and there select receive flag.

If you have done everything correctly - you will get a flag, which you can hand in in the task card in the form below.
