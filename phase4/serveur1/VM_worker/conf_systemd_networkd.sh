apt update
apt upgrade
systemctl stop NetworkManager.service
systemctl disable NetworkManager.service
systemctl stop networking.service
systemctl disable networking.service