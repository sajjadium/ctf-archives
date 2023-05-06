from qunetsim import Network


def exchange_key(aaa, tbd, qubits_n):
    network = Network.get_instance()
    nodes = [aaa.host.host_id, tbd.host.host_id]
    network.start(nodes)
    
    network.delay = 0.0

    network.add_host(aaa.host)
    network.add_host(tbd.host)

    t1 = aaa.host.run_protocol(aaa.exchange_key, (tbd.host.host_id, qubits_n*2))
    t2 = tbd.host.run_protocol(tbd.exchange_key, (aaa.host.host_id, qubits_n*2))
    t1.join()
    t2.join()

    return network


def bet_in_casino(network, aaa, tbd, bet_times):
    t1 = aaa.host.run_protocol(aaa.bet, (tbd.host.host_id, bet_times))
    t2 = tbd.host.run_protocol(tbd.bet, (aaa.host.host_id, bet_times))
    t1.join()
    t2.join()

    return network
