"""
This is a public file
"""
from qunetsim import Network


def setup_game(hacker, zardus, plays):
    network = Network.get_instance()
    network.start()
    network.delay = 0.0

    network.add_host(zardus.host)
    network.add_host(hacker.host)

    t = zardus.host.run_protocol(zardus.secret_protocol, (hacker, plays))
    t.join()

    return network


def setup_chat(zardus, adamd, plays):
    zardus.host.start()
    adamd.host.start()
    chat_network = Network.get_instance()
    chat_network.start()
    chat_network.delay = 0.0

    zardus.host.add_connection(adamd.host.host_id)
    adamd.host.add_connection(zardus.host.host_id)
    chat_network.add_host(zardus.host)
    chat_network.add_host(adamd.host)

    t1 = zardus.host.run_protocol(zardus.chat, (adamd.host.host_id, plays))
    t2 = adamd.host.run_protocol(adamd.chat, (zardus.host.host_id, plays))
    t2.join()
    t1.join()

    return chat_network


def stop(networks):
    for network in networks:
        network.stop(True)
