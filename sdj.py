#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess


PATH_NSSWITCH = "/etc/nsswitch.conf"
PATH_KERBEROS = "/etc/krb5.conf"

def get_hostname():
	return ((os.popen('hostname').read()).replace("\n",""))

def winbind_on():
	str1 = "winbind"
	list1 = list()
	with open(PATH_NSSWITCH, "r") as f:
		for line in f:
			if (("passwd" in line) and (str1 in line)):
				return ("Failed! \"winbind\" already added")
			else:
				list1.append(line)
	
	for i in range(6,9):
		list1[i] = list1[i].replace("\n", " ")
		list1[i] = list1[i] + str1 + "\n"
		
	with open(PATH_NSSWITCH, "w") as f:
		for line in list1:
			f.write(line)
	return ("\"winbind\" succesfully added.")

def winbind_off():
	str1 = "winbind"
	list1 = list()
	with open (PATH_NSSWITCH, "r") as f:
		for line in f :
			if (("passwd" in line) and not (str1 in line)):
				return ("Failed! \"winbind\" already removed")
			else:
				list1.append(line)
				
	for i in range(6,9):
		list1[i] = list1[i].replace(str1, "")
	
	with open(PATH_NSSWITCH, "w") as f:
		for line in list1:
			f.write(line)
	return ("\"winbind\" successfully removed.")

def nsswitch_check():
	with open (PATH_NSSWITCH, "r") as f:
		for line in f :
			if (("passwd") in line) and (("winbind") in line):
				return ("added")
		return ("removed")

def set_hostname(hostname):
	with open("/etc/hostname", "w") as host:
		host.write(hostname+ "\n")
	oldHostname=get_hostname()
	os.system('%s' % ("hostname "+ hostname))
	os.system('xauth add `echo $(hostname)/$(xauth list | cut -d" " -f1 | cut -d"/" -f2) $(xauth list | cut -d" " -f3,5)`')
	if not(oldHostname == hostname):
		os.system('xauth remove $(echo $(xauth list | head -1 | cut -d" " -f1))')
	
def set_hosts(hostname, realm):
	etc_hosts = list()
	with open("/etc/hosts", "r") as host:
		for line in host:
			if ("127.0.1.1") in line:
				etc_hosts.append("127.0.1.1       "+
				hostname+ "       "+
				hostname+ "."+realm.lower()+ "\n")
			else:
				etc_hosts.append(line)
	with open("/etc/hosts", "w") as host:
		for line in etc_hosts:
			host.write(line)

def update_hosts(hostname):
	etc_hosts = list()
	with open("/etc/hosts", "r") as host:
		for line in host:
			if ("127.0.1.1") in line:
				etc_hosts.append("127.0.1.1       "+
				hostname+ "\n")
			else:
				etc_hosts.append(line)
	with open("/etc/hosts", "w") as host:
		for line in etc_hosts:
			host.write(line)

def set_samba(hostname, realm, workgroup):
	with open("/etc/samba/smb.conf", "w") as samba:
		samba.write("workgroup = "+ workgroup+ "\n")
		samba.write("domain logons = yes\n")
		samba.write("netbios name = "+ hostname+ "\n")
		samba.write("server string = "+ hostname+ "\n")
		samba.write("realm = "+ realm.upper()+ "\n")
		samba.write("idmap uid= 10000-20000\n")
		samba.write("idmap gid= 10000-20000\n")
		samba.write("template shell = /bin/bash\n")
		samba.write("template homedir = /home/%D/%U\n")
		samba.write("winbind enum groups = yes\n")
		samba.write("winbind enum users = yes\n")
		samba.write("winbind use default domain = yes\n")
		samba.write("client use spnego = yes\n")
		samba.write("client ntlmv2 auth = yes\n\n")
		samba.write("socket options = TCP_NODELAY SO_RCVBUF=8192 SO_SNDBUF=8192\n\n")
		samba.write("hosts allow = all\n")
		samba.write("security = ADS\n")

def get_workgroup():
	with open("/etc/samba/smb.conf", "r") as samba:
		for line in samba:
			if ("workgroup =") in line:
				return line.replace("workgroup = ","")

def update_samba(hostname):
	smb = list()
	with open("/etc/samba/smb.conf", "r") as samba:
		for line in samba:
			if ("netbios name = ") in line:
				smb.append("netbios name = "+ hostname+ "\n")
			elif ("server string = ") in line:
				smb.append("server string = "+ hostname+ "\n")
			elif ("workgroup = ") in line:
				smb.append("workgroup = WORKGROUP\n")
			elif ("realm = ") in line:
				smb.append("realm = WORKGROUP\n")
			else:
				smb.append(line)
	with open("/etc/samba/smb.conf", "w") as samba:
		for line in smb:
			samba.write(line)

def get_realm():
	with open("/etc/samba/smb.conf", "r") as samba:
		for line in samba:
			if(("realm = ") in line):
				return (line.replace("realm = ",""))
		return ("WORKGROUP")

def set_kerberos(realm):
	kerberos_add_realm(realm)
	kerberos_add_domain(realm)
	kerberos_set_default_realm(realm)

def kerberos_add_realm(realm):
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if( "default_domain" in line and realm in line ):
				return ("Already exists!")
	content = list()
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if( line == "[realms]\n" ):
				content.append(line)
				content.append(realm.lower()+ " = {\n")
				content.append("default_domain="+ realm+ "\n")
				content.append("}\n")
			else:
				content.append(line)
	with open(PATH_KERBEROS, "w") as kerberos:
		for line in content:
			kerberos.write(line)
	return ("realm "+ realm+ " succesfully added.")

def kerberos_add_domain(realm):
	domain = realm
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if ("."+domain.upper()) in line:
				return("Already exists!\n")
	counter1 = 0
	flag = 0
	counter2 = 0
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if( line == "[domain_realm]\n"):
				flag = 1
				counter1 += 1
			
			if(flag == 0):
				counter1 += 1
	content = list()
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if(counter2 == counter1):
				content.append("."+domain.upper()+ " = "+ realm+ "\n")
				content.append(domain.upper()+ " = "+ realm+ "\n")
				content.append(line)
				counter2 += 1
			else:
				content.append(line)
				counter2 += 1
	with open(PATH_KERBEROS, "w") as kerberos:
		for line in content:
			kerberos.write(line)
	return ("\""+ domain.upper()+ "\""+ " succesfully added to \""+ realm+ "\"")


def add_to_domain(hostname, realm, password_user):
	text = ""
	text = text + ((os.popen('echo %s|kinit %s' % (password_user,hostname+"@"+realm.upper())).read()))
	text = text + ((os.popen('klist').read()))
	text = text + ((os.popen('echo %s|%s' % (password_user, "net ads join -U "+ hostname)).read()))
	return (text)

def confirm():
	check = (os.popen('%s' % ("net ads join -k")).read())
	return check

def add_host():
	output = subprocess.check_output("net ads info", shell=True)
	tbuffer = ""
	out = list()
	for c in output:
		if(chr(c) == "\n"):
			out.append(tbuffer)
			tbuffer = ""
		else:
			tbuffer = tbuffer + chr(c)
	ip_address = out[0].replace("LDAP server: ","")
	hostname = out[1].replace("LDAP server name: ","")
	str2 = ip_address
	str3 = hostname.lower()
	
	if (fsearchBoolean(str2) or fsearchBoolean(str3)):
		return ("Failed! Either IP address or Hostname already exists")
	
	for i in range(len(str2),16):
		str2 = str2 + " "
	str1 = list()
	index = -1
	with open("/etc/hosts", "r") as f:
		for line in f:
			if (line == "# The following lines are desirable for IPv6 capable hosts\n"):
				break
			else:
				index += 1
	
	counter = 0 
	with open("/etc/hosts", "r") as f:
		for line in f:
			str1.append(line)
			counter += 1
			if(counter == index):
				str1.append(str2 + str3 + "\n")
				
	
	with open("/etc/hosts", "w") as f:
		for line in str1:
			f.write(line)
	return ("\""+str2 + str3+"\"" +" added ")

def fsearchBoolean(str2):	
	sf = open ("/etc/hosts", "r")
	str1 = sf.readline()
	counter = 1
	while not (str1 == "# The following lines are desirable for IPv6 capable hosts\n"):
		if str2 in str1:
			str1 = str1.replace("\n", "")
			return True
		counter += 1
		str1 = sf.readline()
	return False
	sf.close()

def add_server():
	output = subprocess.check_output("net ads info", shell=True)
	tbuffer = ""
	out = list()
	for c in output:
		if(chr(c) == "\n"):
			out.append(tbuffer)
			tbuffer = ""
		else:
			tbuffer = tbuffer + chr(c)
	realm = out[2].replace("Realm: ","")
	s = out[1].replace("LDAP server name: ","")
	kerberos_add_server(realm.lower(), ("kdc"), s.lower())
	kerberos_add_server(realm.lower(), ("admin_server"), s.lower())

def kerberos_add_server(realm, server, hostname):
	counter1 = 0
	flag1 = 0
	counter2 = 0
	flag2 = 0
	counter = 0
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if(line == (realm+ " = {\n")):
				flag1 = 1
				counter1 += 1
			if(flag1 == 0):
				counter1 += 1 
			if(line == ("default_domain="+ realm+ "\n")):
				flag2 = 1
				counter2 -= 1
			if(flag2 == 0):
				counter2 += 1
	counter3 = 0
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if(counter3 >= counter1 and counter3 <= counter2):
				if((server in line) and (hostname in line)):
					return ("Already exists!")
				counter3 += 1
			else:
				counter3 += 1
	if(server == ("kdc")):
		content = list ()
		with open(PATH_KERBEROS, "r") as kerberos:
			for line in kerberos:
				if(counter == counter1):
					content.append("kdc = "+ hostname+ "\n")
					content.append(line)
					counter += 1
				else:
					content.append(line)
					counter += 1
		with open(PATH_KERBEROS, "w") as kerberos:
			for line in content:
				kerberos.write(line)
		return ("kdc \""+ hostname+ "\" successfully added to \""+ realm+ "\"")
	elif(server == ("admin_server")):
		content = list ()
		with open(PATH_KERBEROS, "r") as kerberos:
			for line in kerberos:
				if(counter == counter2):
					content.append(line)
					content.append("admin_server= "+ hostname+ "\n")
					counter += 1
				else:
					content.append(line)
					counter += 1
		with open(PATH_KERBEROS, "w") as kerberos:
			for line in content:
				kerberos.write(line)
		return ("admin server \""+ hostname+ "\" succesfully added to \""+ realm+ "\"")
	else:
		return ("Invalid server!")

def kerberos_set_default_realm(realm):
	content = list()
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if ("default_realm = " in line):
				content.append("default_realm = "+ realm.upper()+ "\n")
			else:
				content.append(line)
	with open(PATH_KERBEROS, "w") as kerberos:
		for line in content:
			kerberos.write(line)

def get_actual_realm(domain):
	rlist = list()
	try:
		output = subprocess.check_output("%s" % ("samba-tool domain info "+ domain.upper()), shell=True)
	except subprocess.CalledProcessError:
		rlist.append("error")
		return rlist
	else:
		terminal = list()
		tbuffer = ""
		for c in output:
			if(chr(c) == "\n"):
				terminal.append(tbuffer)
				tbuffer = ""
			else:
				tbuffer = tbuffer + chr(c)
		for line in terminal:
			if ("Domain           :") in line:
				realm = (line.replace("Domain           : ","")).replace("\n","")
			elif ("Netbios domain   :") in line:
				workgroup = (line.replace("Netbios domain   : ","")).replace("\n","")
			else:
				pass
		rlist.append(realm)
		rlist.append(workgroup)
		return rlist

def configure_pam():
	content = list()
	with open("/etc/pam.d/common-account", "r") as pam:
		for line in pam:
			content.append(line)
	conf = "session required pam_mkhomedir.so skel=/etc/skel umask=0022\n"
	if not (content[len(content)-1] == conf):
		content.append("session required pam_mkhomedir.so skel=/etc/skel umask=0022\n")
	with open("/etc/pam.d/common-account", "w") as pam:
		for line in content:
			pam.write(line)
	del content [:]
	with open("/etc/pam.d/common-password", "r") as pam:
		for line in pam:
			if (("password") in line) and (("pam_krb5.so") in line):
				# TODO: more stable with using awk
				content.append(line.replace("minimum_uid=1000\n", "minimum_uid=10000\n"))
			else:
				content.append(line)
	with open("/etc/pam.d/common-password", "w") as pam:
		for line in content:
			pam.write(line)

def configure_kerberos():
	flag_libdefaults = 0
	flag_realms = 0
	flag_appdefault = 0
	flag_clock_skew = 0
	flag_ticket_lifetime = 0
	counter = 0
	content = list()
	content_libdefaults = list()
	counter_clock_skew = 0
	content2 = list()
	counter_ticket_lifetime = 0
	content3 = list()
	with open(PATH_KERBEROS, "r") as kerberos:
		for line in kerberos:
			if("default_realm =") in line:
				flag_libdefaults = 1
				counter += 1
				if ("appdefault") in line:
					flag_appdefault = 1
				content.append(line)
			elif(flag_libdefaults == 1 and flag_realms == 0):
				if(line == "[realms]\n"):
					flag_realms = 1
					if ("appdefault") in line:
						flag_appdefault = 1
					content.append(line)
				else:
					content_libdefaults.append(line)
					if ("appdefault") in line:
						flag_appdefault = 1
					content.append(line)
			elif(flag_libdefaults == 0):
				counter += 1
				if ("appdefault") in line:
					flag_appdefault = 1
				content.append(line)
			else:
				if ("appdefault") in line:
					flag_appdefault = 1
				content.append(line)
	for line in content_libdefaults:
		if ("clock_skew") in line:
			flag_clock_skew = 1
		elif ("ticket_lifetime") in line:
			flag_ticket_lifetime = 1
		else:
			pass
	if not (flag_clock_skew):
		for line in content:
			if(counter == counter_clock_skew):
				content2.append("clock_skew = 300\n")
				content2.append(line)
				counter_clock_skew += 1
			else:
				content2.append(line)
				counter_clock_skew += 1
		counter += 1
	if not (flag_ticket_lifetime):
		for line in content2:
			if(counter == counter_ticket_lifetime):
				content3.append("ticket_lifetime = 24000\n")
				content3.append(line)
				counter_ticket_lifetime += 1
			else:
				content3.append(line)
				counter_ticket_lifetime += 1
		del content[:]
		content = content3
	if not (flag_appdefault):
		content.append("\n[appdefaults]\n")
		content.append("pam = {\n")
		content.append("debug = false\n")
		content.append("ticket_lifetime = 36000\n")
		content.append("renew_lifetime = 36000\n")
		content.append("forwardable = true\n")
		content.append("krb4_convert = false\n")
		content.append("}\n")
	with open(PATH_KERBEROS, "w") as kerberos:
		for line in content:
			kerberos.write(line)
						
if(len(sys.argv)>1):
	cmd = sys.argv[1]
	if(cmd == "get_hostname"):
		get_hostname()
	elif(cmd == "winbind_on"):
		winbind_on()
	elif(cmd == "winbind_off"):
		winbind_off()
	elif(cmd == "set_hostname"):
		hostname = sys.argv[2]
		set_hostname(hostname)
	elif(cmd == "set_hosts"):
		hostname = sys.argv[2]
		realm = sys.argv[3]
		set_hosts(hostname, realm)
	elif(cmd == "update_hosts"):
		hostname = sys.argv[2]
		update_hosts(hostname)
	elif(cmd == "set_samba"):
		hostname = sys.argv[2]
		realm = sys.argv[3]
		set_samba(hostname, realm)
	elif(cmd == "update_samba"):
		hostname = sys.argv[2]
		update_samba(hostname)
	elif(cmd == "set_kerberos"):
		realm = sys.argv[2]
		set_kerberos(realm)
	elif(cmd == "add_to_domain"):
		hostname = sys.argv[2]
		realm = sys.argv[3]
		password_user = sys.argv[4]
		add_to_domain(hostname, realm, password_user)
	elif(cmd == "confirm"):
		confirm()
	elif(cmd == "get_realm"):
		get_realm()
	else:
		print ("Invalid Command!")
