## InfluxDB

https://www.mikan-tech.net/entry/influxdb-grafana-install

### setup

```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt update

sudo apt install -y influxdb

sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service
```

### initialize

```
$ influx

> create database sensor
> use sensor
Using database sensor

> create user grafana with password 'grafana' with all privileges
> grant all privileges on sensor to grafana
> show users
user    admin
----    -----
grafana true

> CREATE DATABASE sensortag
> exit

> exit
```

### python から

``` sh
pip3 install influxdb
```

### grafana に表示

- https://www.mikan-tech.net/entry/raspi-sensortag-grafana


