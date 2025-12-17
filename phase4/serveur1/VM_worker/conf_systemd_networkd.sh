apt update
apt upgrade
systemctl stop NetworkManager.service
systemctl disable NetworkManager.service
systemctl stop networking.service
systemctl disable networking.service
nano /etc/systemd/network/ens18-ethernet.network
systemctl enable systemd-networkd
systemctl start systemd-networkd