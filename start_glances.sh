sudo service grafana-server start
sudo service influxd start
glances --export influxdb
