## ラズパイ

### ラズパイマガジン

#### Goods
- AI アクセラレーター
  - TPU (Tens or Processing Unit)


### SunFounder Starter Kit
- [オンラインマニュアル](https://docs.sunfounder.com/projects/davinci-kit/ja/latest/)

#### install
https://taku-info.com/ubuntu-wiringpi-gpio/

```sh
$ sudo apt-get install wiringpi
$ sudo apt install python3-rpi.gpio

# このデフォルトのバージョンのままでは使えない
$ sudo gpio readall
Oops - unable to determine board type... model: 17
$ gpio -v
gpio version: 2.50
Copyright (c) 2012-2018 Gordon Henderson
This is free software with ABSOLUTELY NO WARRANTY.
For details type: gpio -warranty

Raspberry Pi Details:
  Type: Unknown17, Revision: 04, Memory: 0MB, Maker: Sony
  * Device tree is enabled.
  *--> Raspberry Pi 4 Model B Rev 1.4
  * This Raspberry Pi supports user-level GPIO access.
```

Raspberry Pi 4 Model BでWiring Pi 2.50は対応しておらず、Wiring Pi 2.52へバージョンアップする必要がある

```sh
$ wget https://project-downloads.drogon.net/wiringpi-latest.deb
$ sudo dpkg -i wiringpi-latest.deb

$ gpio -v
```


