# Simple Domain Joiner

Simple Domain Joiner is a system administrator tool for Linux systems.
Simple Domain Joiner offers a very simple graphical user interface to change the domain of the system.
Users are only asked to enter the computer name and the domain address.
All necesssary configurations are done in background.

### Prerequisites
**Debian**: 

```
apt install libpam-krb5 libnss-winbind libpam-winbind winbind samba krb5-user
```

### Run
```
python3 simple-domain-joiner.py
```
### Manual

Enter the computer name and the domain address.

![alt text](https://github.com/PardusGenc/Simple-Domain-Joiner/blob/master/screenshots/sdj_main1.png)

![alt text](https://github.com/PardusGenc/Simple-Domain-Joiner/blob/master/screenshots/sdj_adddomain.png)

![alt text](https://github.com/PardusGenc/Simple-Domain-Joiner/blob/master/screenshots/sdj_sucdomain.png)

