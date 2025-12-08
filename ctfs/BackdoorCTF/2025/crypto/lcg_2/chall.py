import sys
from secrets import randbelow
from Crypto.Util.number import getPrime

FLAG = "flag{REDACTED}"
MAIN_BITS = 128
INTERVAL_MODULUS = 1031

class LCG:
    """A Linear Congruential Generator class."""
    def __init__(self, a, c, m, seed=None):
        self.a = a
        self.c = c
        self.m = m
        if seed is not None:
            self.seed = seed
        else:
            self.seed = randbelow(m)

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

    def skip(self, n):
        if n == 0:
            return self.seed

        a_n = pow(self.a, n, self.m)
        try:
            inv_a_minus_1 = pow(self.a - 1, -1, self.m)
            geometric_sum = (self.c * (a_n - 1) * inv_a_minus_1) % self.m
        except ValueError:
            geometric_sum = (self.c * n) % self.m

        self.seed = (a_n * self.seed + geometric_sum) % self.m
        return self.seed

def print_banner():
    print(r"""
         *******     *******     ********  **     ** ********       
        /**////**   **/////**   **//////**/**    /**/**/////        
        /**   /**  **     //** **      // /**    /**/**             
        /*******  /**      /**/**         /**    /**/*******        
        /**///**  /**      /**/**    *****/**    /**/**////         
        /**  //** //**     ** //**  ////**/**    /**/**             
        /**   //** //*******   //******** //******* /********       
        //     //   ///////     ////////   ///////  ////////        
                                                                                                                            
              ** **     ** ****     **** *******  ******** *******  
             /**/**    /**/**/**   **/**/**////**/**///// /**////** 
             /**/**    /**/**//** ** /**/**   /**/**      /**   /** 
             /**/**    /**/** //***  /**/******* /******* /*******  
             /**/**    /**/**  //*   /**/**////  /**////  /**///**  
         **  /**/**    /**/**   /    /**/**      /**      /**  //** 
        //***** //******* /**        /**/**      /********/**   //**
         /////   ///////  //         // //       //////// //     // 
    """)
    print("[-] TARGET: Rogue Jumper")
    print("[-] STATUS: Navigation Drive Unstable")
    print("[-] INTEL:  Jump intervals controlled by aux circuit (mod 1031)")
    print("---------------------------------------------------------")

def main():
    print_banner()
    m_int = INTERVAL_MODULUS
    a_int = <redacted>
    c_int = <redacted>
    seed_int= <redacted>
    
    interval_lcg = LCG(a_int, c_int, m_int, seed_int)


    m_main = getPrime(MAIN_BITS)
    a_main = randbelow(m_main)
    c_main = randbelow(m_main)
    
    main_lcg = LCG(a_main, c_main, m_main)

    print(f"[i] Main Navigation Modulus (M): {m_main}")
    print(f"[i] Aux System Modulus (m): {m_int}")
    print("\n[SYSTEM] Tracking initiated...")

    QUERIES_ALLOWED = 20 
    
    for i in range(QUERIES_ALLOWED):
        print(f"\n--- Observation {i+1}/{QUERIES_ALLOWED} ---")
        print("1. Ping ship location (Observe)")
        print("2. Engage Tractor Beam (Predict)")
        choice = input("Select Action > ").strip()

        if choice == '1':
            jump_distance = interval_lcg.next()

            if jump_distance > 0:
                current_coord = main_lcg.skip(jump_distance - 1)
            else:
                current_coord = main_lcg.seed
            
            print(f"[+] Signal Detected. Coordinate: {current_coord}")
            print(f"[+] Jump Magnitude: UNKNOWN (Auxiliary Encrypted)")

        elif choice == '2':
            print("\n[!] TRACTOR BEAM CHARGING...")
            print("[!] To lock on, predict the next 3 coordinates.")
            
            try:
                answers = []
                for _ in range(3):
                    jump = interval_lcg.next()
                    if jump > 0:
                        val = main_lcg.skip(jump - 1)
                    else:
                        val = main_lcg.seed
                    answers.append(val)
                
                u1 = int(input("Predicted Coord 1: "))
                u2 = int(input("Predicted Coord 2: "))
                u3 = int(input("Predicted Coord 3: "))

                if u1 == answers[0] and u2 == answers[1] and u3 == answers[2]:
                    print("\n[SUCCESS] Target Locked! Beam engaged.")
                    print(f"[OUTPUT] {FLAG}")
                    sys.exit(0)
                else:
                    print("\n[FAILURE] Prediction mismatch. Target escaped into hyperspace.")
                    sys.exit(0)
            except ValueError:
                print("[ERROR] Invalid input.")
                sys.exit(0)
        
        else:
            print("[!] Invalid command.")

    print("\n[SYSTEM] Tracking sensors overheated. Connection lost.")

if __name__ == "__main__":
    main()
