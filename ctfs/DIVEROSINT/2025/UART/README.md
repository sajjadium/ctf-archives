この商品のイーサネットスイッチコントローラに直接UARTでアクセスを試みたい。どの部品の、どのピンにアクセスすればいいだろうか。
PCB上の部品番号 と、その部品の UART RX / UART TX ピン番号 を答えよ。ピン番号は部品の仕様に準拠せよ。
なお、ピンヘッダやコネクタが利用可能な場合でも、イーサネットスイッチコントローラのピン番号を答えてほしい。
Flag形式: Diver25{PCB上の部品番号_UART RXピン番号_UART TXピン番号}
（例えば、イーサネットスイッチコントローラが T21 という部品番号で、RXのピン番号が120、TXのピン番号が150であれば、Diver25{T21_120_150}となる）

I want to try to access the Ethernet switch controller of this product directly via UART. Which component and which pin should I access?
Answer the part number on the PCB and the UART RX / UART TX pin number of the component. The pin number should follow the specification of the component.
Note that even if pin headers and connectors are available, answer the pin numbers of the Ethernet switch controller. Flag Format: Diver25{Part Number on PCB_UART RX pin number_UART TX pin number}
(If the Ethernet switch controller has part number T21 on PCB, RX pin number is 120 and TX pin number is 150, the flag should be Diver25{T21_120_150}.)
