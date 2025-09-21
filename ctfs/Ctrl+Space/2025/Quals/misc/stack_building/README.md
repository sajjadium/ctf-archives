radio
drw0if, marcog

Welcome to our virtual satellite!

The following endpoints allows you to retrieve the 3 parts of the full flag:

Link layer at :10015
Channel coding at :10016
Modulated signal at :10017
Please read the attached file carefully to get how the communication stack is built and how to use the taps provided at different parts of the stack.


# Stack Building

Welcome to **mHACKeroni Virtual Satellite**!

This satellite follows (almost) all the specification listed in the following blue books:
- [TC space data link protocol](https://ccsds.org/Pubs/232x0b4e1c1.pdf): for the uplink data link
- [TM space data link protocol](https://ccsds.org/Pubs/132x0b3.pdf): for the downlink data link
- [TM synchronization and channel coding](https://ccsds.org/Pubs/131x0b5.pdf): for the channel coding
- BPSK as modulation

Our stack is as composed:

```

RX Antenna
    X
    |
    |    ____________       ______       _____________      _____       ______________       _____________
    |   |            |     |      |     |             |    |     |     |              |     |             |
    +---| BPSK demod | --> | Sync | --> | Descrambler | -> | FEC | --> | Frame parser | --> | Application |
        |____________|     |______|     |_____________|    |_____|     |______________|     |_____________|


                                                                                                  TX Antenna
                                                                                                       X
                                                                                                       |
     _____________       _______________       _____      ___________       ______       __________    |
    |             |     |               |     |     |    |           |     |      |     |          |   |
    | Application | --> | Frame builder | --> | FEC | -> | Scrambler | --> | Sync | --> | BPSK mod |---+
    |_____________|     |_______________|     |_____|    |___________|     |______|     |__________|

```

## Taps
In order to help with the debug in the various step we built some taps that you can use to access intermediate part of the stack.

### Link layer
Using the service at port `10015` it is possible to directly access the data link layer and exchange TC and TM frames directly:
```
                     ______________       _____________       _______________     
                    |              |     |             |     |               |    
    taps:10015 ---> | Frame parser | --> | Application | --> | Frame builder | ---> taps:10015
                    |______________|     |_____________|     |_______________| 

```

### Channel coding
Using the service at port `10016` it is possible to directly access the channel before the modulation takes place, you get a plain bitstream:
```
                    ______       _____________      _____       ______________       _____________
                   |      |     |             |    |     |     |              |     |             |
    taps:10016 --->| Sync | --> | Descrambler | -> | FEC | --> | Frame parser | --> | Application |
                   |______|     |_____________|    |_____|     |______________|     |_____________|

     _____________       _______________       _____      ___________       ______     
    |             |     |               |     |     |    |           |     |      |    
    | Application | --> | Frame builder | --> | FEC | -> | Scrambler | --> | Sync | --> taps:10016
    |_____________|     |_______________|     |_____|    |___________|     |______|     

```

### Full experience
Using the service at port `10017` it is possible to access the virtual antennas of the satellite, you get a stream of complex.
