## 搭建docker

`docker build -t "ez_atm" .`


## 运行docker

`docker run -d -p "0.0.0.0:4444:8888" -p "0.0.0.0:4445:3339" -h "ez_atm" --name="ez_atm" ez_atm`


其中`pub_port`需要被替换成对选手开放的端口
