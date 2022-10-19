# vxlan
NSO service package for the MP-BGP EVPN VXLAN auto configuration for the cisco NXOSv which includes underlay, overlay and vrf-leaking

Please refer to the "./packages/data/vxlan service package.ppt" for the details.

```
NSO; 5.7.1.1

packages/data; includes the swich configuration(before/after), configuration xml files
packages/cisco-nx-cli-5.22; yang file was modified to support the "ip unnumbered interface", use the keyword "kils" for seaching the modified code 
packages/vxlanInfra; service package for vxlan infra (underlay, overlay)
packages/vxlanTenant; service package for tenant on the vxlan
packages/vxlanVrfleaking; service packages for VRF leaking between multiple tenants
```


# How to run

1. prepare 4 NX switches.
2. configure managment IP address
3. register the switches in the NSO
```
admin@ncs# show devices list
NAME        ADDRESS       DESCRIPTION  NED ID             ADMIN STATE
---------------------------------------------------------------------
n9k-bdr1    10.70.196.42  -            cisco-nx-cli-5.22  unlocked
n9k-leaf1   10.70.196.40  -            cisco-nx-cli-5.22  unlocked
n9k-leaf2   10.70.196.41  -            cisco-nx-cli-5.22  unlocked
n9k-spine1  10.70.196.38  -            cisco-nx-cli-5.22  unlocked
```
4. configure vxlan with xml files
```
admin@ncs# config
Entering configuration mode terminal

admin@ncs(config)# load merge packages/data/xml/config_vxlanInfra.xml
admin@ncs(config)# commit

admin@ncs(config)# load merge packages/data/xml/config_vxlanTenant_1.xml
admin@ncs(config)# commit

admin@ncs(config)# load merge packages/data/xml/config_vxlanTenant_2.xml
admin@ncs(config)# commit

admin@ncs(config)# load merge packages/data/xml/config_vxlanVrfleaking.xml
admin@ncs(config)# commit
```


# IP reachability test

Ping from svr1 towards  svr2(L2) / svr3(L3) / svr4(VRF leaking)

```
[root@svr1 ~]# ip r
default via 10.70.196.1 dev ens192 proto static metric 100
10.70.196.0/23 dev ens192 proto kernel scope link src 10.70.197.33 metric 100
172.16.0.0/16 via 172.16.201.1 dev ens224
172.16.201.0/24 dev ens224 proto kernel scope link src 172.16.201.101 metric 101
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1

[root@svr1 ~]# ping 172.16.201.1 -c 2
PING 172.16.201.1 (172.16.201.1) 56(84) bytes of data.
64 bytes from 172.16.201.1: icmp_seq=1 ttl=255 time=8.47 ms
64 bytes from 172.16.201.1: icmp_seq=2 ttl=255 time=42.9 ms

--- 172.16.201.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 8.476/25.699/42.923/17.224 ms

[root@svr1 ~]# ping 172.16.201.102 -c 2
PING 172.16.201.102 (172.16.201.102) 56(84) bytes of data.
64 bytes from 172.16.201.102: icmp_seq=1 ttl=64 time=34.1 ms
64 bytes from 172.16.201.102: icmp_seq=2 ttl=64 time=69.9 ms

--- 172.16.201.102 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 34.148/52.066/69.985/17.919 ms

[root@svr1 ~]# ping 172.16.202.103 -c 2
PING 172.16.202.103 (172.16.202.103) 56(84) bytes of data.
64 bytes from 172.16.202.103: icmp_seq=1 ttl=62 time=40.6 ms
64 bytes from 172.16.202.103: icmp_seq=2 ttl=62 time=34.4 ms

--- 172.16.202.103 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 34.467/37.536/40.605/3.069 ms

[root@svr1 ~]# ping 172.16.211.104 -c 2
PING 172.16.211.104 (172.16.211.104) 56(84) bytes of data.
64 bytes from 172.16.211.104: icmp_seq=1 ttl=62 time=35.7 ms
64 bytes from 172.16.211.104: icmp_seq=2 ttl=62 time=31.1 ms

--- 172.16.211.104 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 31.102/33.405/35.709/2.310 ms

```
