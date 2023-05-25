https://uzimihsr.github.io/post/2020-01-15-prometheus-grafana-raspberry-pi/

こっから落としてくる
https://prometheus.io/download/#prometheus

``` sh
sudo useradd -U -s /sbin/nologin -M -d / node_exporter

# serviceファイルを作成する
sudo vim /etc/systemd/system/node_exporter.service

###################################
[Unit]
Description=Node Exporter

[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
###################################

# serviceの起動
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
systemctl status node_exporter
```


``` sh
sudo cp -a prometheus-2... /usr/local/prometheus

# service起動に必要なuser(prometheus)を追加する
sudo useradd -U -s /sbin/nologin -M -d / prometheus

# Prometheusが時系列データを保存するためのディレクトリを作成する
sudo mkdir -p /var/lib/prometheus/data
sudo chown -R prometheus:prometheus /var/lib/prometheus

# serviceファイルを作成する
sudo vim /etc/systemd/system/prometheus.service

####################################
[Unit]
Description=Prometheus Server

[Service]
User=prometheus
ExecStart=/usr/local/prometheus/prometheus \
  --config.file=/usr/local/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/data

[Install]
WantedBy=multi-user.target
######################################

# serviceの起動
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
systemctl status prometheus
```
