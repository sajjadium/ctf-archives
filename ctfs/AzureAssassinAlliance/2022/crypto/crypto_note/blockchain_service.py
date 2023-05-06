"""
A "solo" consensus ledger endorsed during bookkeeping
"""

from json import loads, dumps
from secret import flag, alice_pub, bob_priv, bob_pub, carol_priv, carol_pub
from abc import abstractmethod
from ring_signature import serialize2json, deserialize4json, transaction_curve, OTRS, H as Hv, prng, Hp

E, G = transaction_curve()
otrs = OTRS(E, G)

class MessagePusher(object):
    @abstractmethod
    def push(self, message):
        pass

class TerminalMessagePusher(MessagePusher):
    def push(self, message):
        print(message)

class RPCListener(object):
    @abstractmethod
    def on_new_request(self, listener):
        pass

    @abstractmethod
    def listen(self):
        pass

class TerminalRPCListener(RPCListener):
    def __init__(self):
        super().__init__()
        self.listeners = []
        self.reply_hook = None

    def on_new_request(self, listener):
        self.listeners.append(listener)
    
    def do_reply(self, message):
        if self.reply_hook is not None:
            self.reply_hook(message)
            return
        print(message)

    def handle_rpc_request(self, json):
        for listener in self.listeners:
            listener(json, lambda reply: self.do_reply(reply))

    def listen(self):
        try:
            while True:
                json = ''
                while True:
                    json += input('req> ')
                    json = json.strip()
                    if json.endswith('\\'):
                        json = json[:-1]
                    else:
                        break
                self.handle_rpc_request(json)
        except KeyboardInterrupt:
            print("")
            exit()

class BCTransaction(object):
    def __init__(self, txi, sig, txo):
        self.txi = txi
        self.sig = sig
        self.txo = txo
        self.coinbase = False

    def serialize(self):
        assert not self.coinbase
        return serialize2json(self.txi, self.sig, self.txo)

    @staticmethod
    def deserialize(json):
        txi, sig, txo = deserialize4json(E, json)
        # type coerce
        txi = [int(txo_id) for txo_id in txi]
        I, c_0, r = sig
        c_0 = int(c_0)
        r = [int(r_i) for r_i in r]
        I = E(int(I.xy()[0]), int(I.xy()[1]))
        sig = (I, c_0, r)
        txo = E(int(txo.xy()[0]), int(txo.xy()[1]))
        return BCTransaction(txi, sig, txo)
    
    @staticmethod
    def generate(txi, txo, priv, state_json, ring_size=3):
        pk_owned, txos, key_images = deserialize4json(E, state_json)
        pub = priv * G
        assert pub in pk_owned and txi in pk_owned[pub]
        assert txos[txi] == pub
        txis = [txi] + prng.sample(list(range(txi)) + list(range(txi + 1, len(txos))), min(ring_size, len(txos))-1)
        prng.shuffle(txis)
        Ks = [txos[txo_id] for txo_id in txis]
        sig = otrs.signature(Ks, Hv(txis, txo), priv, txis, txi)
        return BCTransaction(txis, sig, txo)

class BCBlock(list):
    pass

class BCState(object):
    def __init__(self):
        self.txo = []
        self.key_images = set()
        self.pk_owned = dict()
    
    def verify_transaction(self, transaction:BCTransaction):
        if transaction.coinbase:
            return
        Ks = [self.txo[txo_id] for txo_id in transaction.txi]
        assert otrs.verify(Ks, Hv(transaction.txi, transaction.txo), transaction.sig, transaction.txi)
        I, _, _ = transaction.sig
        assert I not in self.key_images
    
    def apply_transaction(self, transaction:BCTransaction):
        try:
            self.verify_transaction(transaction)
            if not transaction.coinbase:
                I, _, _ = transaction.sig
                self.key_images.add(I)
            if transaction.txo not in self.pk_owned:
                self.pk_owned[transaction.txo] = []
            self.pk_owned[transaction.txo].append(len(self.txo))
            self.txo.append(transaction.txo)
        except Exception:
            pass

class BCLedger(object):
    def __init__(self, state:BCState = None, transactions:list = None) -> None:
        self.state = state if state is not None else BCState()
        self.transactions = transactions if transactions is not None else []
        self.listeners = []

    def __append_transaction(self, transaction:BCTransaction):
        self.transactions.append(transaction)
        self.state.apply_transaction(transaction)
    
    def append_block(self, block:BCBlock):
        for transaction in block:
            self.__append_transaction(transaction)
        for listener in self.listeners:
            listener(self.state)

class BCOrderService(object):
    @abstractmethod
    def insert_transaction(self, transaction:BCTransaction):
        pass

    @abstractmethod
    def mine_to(self, pub_key):
        # Theoretically, this process does not return until a token is mined.
        pass

    @abstractmethod
    def on_new_block(self, listener):
        pass

class BCSoloOrderService(BCOrderService):
    def __init__(self):
        super().__init__()
        self.listeners = []

    def insert_transaction(self, transaction:BCTransaction, mined:bool=False):
        # "solo" consensus :)
        if transaction.coinbase and not mined:
            # coinbase can only be generate by order service it self
            return
        new_block = BCBlock()
        new_block.append(transaction)
        for listener in self.listeners:
            listener(new_block)

    def mine_to(self, pub_key):
        transaction = BCTransaction(None, None, pub_key)
        transaction.coinbase = True
        self.insert_transaction(transaction, True)

    def on_new_block(self, listener):
        self.listeners.append(listener)

class BCPeerService(BCLedger):
    def __init__(self, order:BCOrderService, state:BCState = None, transactions:list = None):
        super().__init__(state, transactions)
        self.order = order
        self.order.on_new_block(lambda block:self.append_block(block))
        self.can_show_state = True

    def on_state_change(self, listener):
        self.listeners.append(listener)
    
    def get_state(self):
        if self.can_show_state:
            return serialize2json(self.state.pk_owned, self.state.txo, self.state.key_images)
        else:
            return "No permission"
    
    def disable_get_state(self):
        self.can_show_state = False

class BCClientService(object):
    def process_rpc(self, json, replier):
        try:
            rpc = loads(json)
            if rpc["type"] == "new_transaction":
                self.order.insert_transaction(BCTransaction.deserialize(rpc["transaction"]))
                replier("Submitted")
            elif rpc["type"] == "show_state":
                replier(self.peer.get_state())
            elif rpc["type"] == "disable_show_state":
                self.peer.disable_get_state()
                replier("Ok")
            else:
                replier("Unsupport request")
        except Exception:
            replier("Error during process your request")

    def __init__(self, rpc:RPCListener, order:BCOrderService, peer:BCPeerService):
        self.rpc = rpc
        self.order = order
        self.peer = peer
        rpc.on_new_request(lambda json, replier:self.process_rpc(json, replier))

class FlagService(object):
    def strictly_count(self, state:BCState, pub, priv):
        assert priv * G == pub
        cnt = 0
        for i in state.pk_owned[pub]:
            I = priv * Hp(E, G, pub, i)
            if I not in state.key_images:
                cnt += 1
        return cnt

    def check_state(self, state:BCState):
        if E(bob_pub) not in state.pk_owned or E(carol_pub) not in state.pk_owned:
            return
        if len(state.pk_owned[E(bob_pub)]) < 2 or len(state.pk_owned[E(carol_pub)]) < 2:
            return
        if self.strictly_count(state, E(bob_pub), bob_priv) < 1 or self.strictly_count(state, E(carol_pub), carol_priv) < 1:
            self.pusher.push("Your solution must be very interesting, do record it, but there are no flag here.")
        else:
            self.pusher.push("Here is your flag: %s" % flag)
        exit() # all things will be killed if the flag is pushed

    def __init__(self, peer:BCPeerService, pusher:MessagePusher):
        self.pusher = pusher
        self.peer = peer
        self.peer.on_state_change(lambda state:self.check_state(state))

if __name__ == '__main__':
    # Start a "blockchain network" :)
    pusher_1 = TerminalMessagePusher()
    rpc_1 = TerminalRPCListener()
    order_1 = BCSoloOrderService()
    peer_1 = BCPeerService(order_1)
    client_1 = BCClientService(rpc_1, order_1, peer_1)
    flag_1 = FlagService(peer_1, pusher_1)
    # At first, the miner carol get her token.
    order_1.mine_to(E(carol_pub))
    # Then, Alice borrowed 1 token from Carol through Bob.
    def submit_to_rpc_1(type_str, transaction=None):
        req = dict()
        req['type'] = type_str
        if transaction is not None:
            req['transaction'] = transaction
        json = dumps(req)
        respond = None
        def hook_impl(message):
            nonlocal respond
            respond = message
        rpc_1.reply_hook = hook_impl
        rpc_1.handle_rpc_request(json)
        rpc_1.reply_hook = None
        return respond

    def transfer_to(txo_id, priv, pub):
        # transfer txo_id, priv to pub
        transaction = BCTransaction.generate(txo_id, pub, priv, submit_to_rpc_1("show_state"))
        return submit_to_rpc_1("new_transaction", transaction.serialize())

    # So, Carol --1 token--> Bob
    transfer_to(0, carol_priv, E(bob_pub))
    # and Bob --1 token--> Alice
    transfer_to(1, bob_priv, E(alice_pub))
    # Don't let you see the state.
    submit_to_rpc_1("disable_show_state")
    # Now, it's your turn. :)
    rpc_1.listen()
