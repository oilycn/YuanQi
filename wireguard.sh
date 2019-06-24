#!/bin/bash

WG_PORT='52147'
IPAddr=`wget --no-check-certificate -qO- http://moeclub.org/address`
POOL='https://deb.debian.org/debian/pool/main/w/wireguard/'

[ `dpkg -s libc6 |grep '^Version' |grep -o '[0-9\.]\{4\}' |head -n1 |cut -d'.' -f2` -ge "14" ] || exit 0

apt-get update
apt-get install -y libmnl-dev libelf-dev linux-headers-$(uname -r) build-essential pkg-config dkms resolvconf dnsmasq qrencode

arch=`dpkg --print-architecture`
Version=`wget --no-check-certificate -qO- "${POOL}" |grep -o 'wireguard_[0-9\_\.\-]\{1,\}_' |head -n1 |cut -d'_' -f2`
[ -n "$Version" ] || exit 1

wget --no-check-certificate -qO "/tmp/wireguard_${Version}_all.deb" "${POOL}wireguard_${Version}_all.deb"
wget --no-check-certificate -qO "/tmp/wireguard-dkms_${Version}_all.deb" "${POOL}wireguard-dkms_${Version}_all.deb"
wget --no-check-certificate -qO "/tmp/wireguard-tools_${Version}_${arch}.deb" "${POOL}wireguard-tools_${Version}_${arch}.deb"

dpkg -i "/tmp/wireguard-tools_${Version}_${arch}.deb"
dpkg -i "/tmp/wireguard-dkms_${Version}_all.deb"
dpkg -i "/tmp/wireguard_${Version}_all.deb"

[ -d /etc/wireguard ] && {
command -v wg >/dev/null 2>&1
[ $? == 0 ] || exit 1
sed -i '/#\?net.ipv4.ip_forward/d' /etc/sysctl.conf
sed -i '$a\net.ipv4.ip_forward=1' /etc/sysctl.conf
sysctl -p

cat >/etc/dnsmasq.conf<<EOF
except-interface=eth0
dhcp-range=192.168.8.2,192.168.8.254,255.255.255.0,24h
dhcp-option-force=option:router,192.168.8.1
dhcp-option-force=option:dns-server,192.168.8.1
dhcp-option-force=option:netbios-ns,192.168.8.1
listen-address=127.0.0.1,192.168.8.1
no-resolv
bogus-priv
no-negcache
clear-on-reload
cache-size=81920
server=208.67.220.220#5353
EOF

cd /etc/wireguard
wg genkey |tee privatekey |wg pubkey > publickey
wg genpsk > presharedkey

wg genkey |tee privatekey.client |wg pubkey > publickey.client

ServerKey=`cat privatekey`
ServerPub=`cat publickey`
ServerPsk=`cat presharedkey`
ClientKey=`cat privatekey.client`
ClientPub=`cat publickey.client`

cat >simple.conf<<EOF
[Interface]
PrivateKey = $ServerKey
Address = 192.168.8.1/24
#ListenPort = $WG_PORT
DNS = 192.168.8.1
#PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE;
#PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE;

[Peer]
#Endpoint = ${IPAddr}:${WG_PORT}
PublicKey = $ClientPub
AllowedIPs = 192.168.8.1/24
PresharedKey = $ServerPsk

EOF

cp -rf /etc/wireguard/simple.conf /etc/wireguard/wg0.conf
cp -rf /etc/wireguard/simple.conf /etc/wireguard/wg0-client.conf

# Server
sed -i 's/#ListenPort/ListenPort/' /etc/wireguard/wg0.conf
sed -i 's/#PostUp/PostUp/' /etc/wireguard/wg0.conf
sed -i 's/#PostDown/PostDown/' /etc/wireguard/wg0.conf
sed -i "/^#/d" /etc/wireguard/wg0.conf

# Client
sed -i 's/#Endpoint/Endpoint/' /etc/wireguard/wg0-client.conf
sed -i "s|PrivateKey =.*|PrivateKey = $ClientKey|" /etc/wireguard/wg0-client.conf
sed -i "s|PublicKey =.*|PublicKey = $ServerPub|" /etc/wireguard/wg0-client.conf
sed -i "s|Address =.*|Address = 192.168.8.2/24|" /etc/wireguard/wg0-client.conf
sed -i "s|AllowedIPs =.*|AllowedIPs = 0.0.0.0/0|" /etc/wireguard/wg0-client.conf
sed -i "/^#/d" /etc/wireguard/wg0-client.conf

# Print QR code for client config.
cat /etc/wireguard/wg0-client.conf |qrencode -o - -t UTF8

# Add to start up
sed -i '/wg-quick/d' /etc/crontab
echo -e "@reboot root wg-quick down wg0 2>/dev/null; wg-quick up wg0\n\n" >>/etc/crontab

# Try it!
wg-quick down wg0 2>/dev/null; wg-quick up wg0
}
