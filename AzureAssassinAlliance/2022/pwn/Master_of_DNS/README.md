# readme

- run command
    
    ```python
    ./start.sh
    ```
    
- test
    
    ```python
    dig @127.0.0.1 -p 9999 baidu.com
    
    ; <<>> DiG 9.16.1-Ubuntu <<>> @127.0.0.1 -p 9999 baidu.com
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 339
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1
    
    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; MBZ: 0x0005, udp: 4096
    ; COOKIE: cf2958cf5b8f520740e4d5a8625d4a26824b1325aed43d79 (good)
    ;; QUESTION SECTION:
    ;baidu.com.                     IN      A
    
    ;; ANSWER SECTION:
    baidu.com.              5       IN      A       220.181.38.251
    baidu.com.              5       IN      A       220.181.38.148
    
    ;; Query time: 31 msec
    ;; SERVER: 127.0.0.1#9999(127.0.0.1)
    ;; WHEN: Mon Apr 18 19:23:18 CST 2022
    ;; MSG SIZE  rcvd: 98
    ```