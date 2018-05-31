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

### Setup
```
python3 setup.py install
```

### Run
```
sdj
```
### Manual
Enter the computer name and the domain address.
Then click 'Confirm' or press enter to join the domain or click 'Cancel' to close without making any changes.

![alt text](https://github.com/PardusGenc/projects/blob/master/sdj/sdj_main1.png)

Login with an authorized account in the new domain to continue.

![alt text](https://github.com/PardusGenc/projects/blob/master/sdj/sdj_adddomain.png)

This message will be received if the system succesfully joins to the domain.

![alt text](https://github.com/PardusGenc/projects/blob/master/sdj/sdj_sucdomain.png)

