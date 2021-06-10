from secrets import flag

assert(len(flag) > 512//8)

seed = int.from_bytes(flag, byteorder='big')

class BBSnLCG:
    def __init__(this, seed):        
        this.B = int.from_bytes(b'BSides CBR', byteorder='big')
        this.C = int.from_bytes(b'cybears', byteorder='big')
        this.D = 2020
        this.N = 133329403635104636891429937256104361307834148892567075810781974525019940196738419111061390432404940560467873684206839810286509876858329703550705859195697849826490388233366569881709667248117952214502616623921379296197606033756105490632562475495591221340492570618714533225999432158266347487875153737481576276481
        this.e = 2
        this.rng_state = seed

    def step(this):
        # Linear Congruential Generator part
        # Step the internal state of the RNG
        this.rng_state = (this.B*(this.rng_state**3) + this.C*this.rng_state + this.D) % this.N

    def get_state(this):
        #Blum-Blum-Shub part
        return pow(this.rng_state, this.e, this.N)

if __name__ == "__main__":

    print("Arming bomb...")
    rng = BBSnLCG(seed)

    print("Parameters used")
    print("B {}, C {}, D {}, N {}, e {}".format(rng.B, rng.C, rng.D, rng.N, rng.e))

    #print("{}: {}".format(0, rng.get_state() ))
    
    internal_state = [rng.rng_state]
    external_state = [rng.get_state()]

    print("Beginning countdown...")
    #Step RNG and save internal and external states
    for i in range(1,10):
        rng.step()
        internal_state.append(rng.rng_state)
        external_state.append(rng.get_state())

        #print("{},".format(rng.get_state() ))

    #print("internal_state = {}".format(internal_state))
    print("external_state = {}".format(external_state))

    with open("countdown", "w") as g:
        g.write("countdown = {}".format(external_state))


