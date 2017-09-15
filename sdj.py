#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module that contains the backend methods of the 
Simple Domain Joiner Project. All necessary configurations 
are done using this module.
"""

# Libraries
import os
import sys
import subprocess

# Absolute paths of required files
PATH_HOST = "/etc/hosts"
PATH_NSSWITCH = "/etc/nsswitch.conf"
PATH_KERBEROS = "/etc/krb5.conf"
PATH_SAMBA = "/etc/samba/smb.conf"

class Nsswitch:
	
	def on(self):
		"""Add `winbind` keyword to all necessary lines 
		in the file `/etc/nsswitch.conf`."""
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
	
	def off(self):
		"""Remove `winbind` keyword from all necessary lines
		in the file `etc/nsswitch.conf`."""
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
	
	def check(self):
		"""Check if the keyword `winbind` added or removed."""
		with open (PATH_NSSWITCH, "r") as f:
			for line in f :
				if (("passwd") in line) and (("winbind") in line):
					return ("added")
			return ("removed")

class Host:
	
	def get(self):
		"""Return the output of the terminal command `hostname`."""
		return ((os.popen('hostname').read()).replace("\n",""))
	
	def read(self):
		"""Return the content of the file `/etc/hosts`."""
		rf = open(PATH_HOST, "r")
		list1 = list()
		str1 = rf.readline()
		while not (str1 == "# The following lines are desirable for IPv6 capable hosts\n"):
			str1.replace("\n","")
			list1.append(str1)
			str1 = rf.readline()
		rf.close()	
		list1.pop()
		return list1
	
	def search(self, str2):
		"""Search if an entry exists in the file `/etc/hosts`
		Return the index of the line exists otherwise return `not found`."""
		sf = open (PATH_HOST, "r")
		str1 = sf.readline()
		counter = 0
		flag = 0
		list1 = list()
		while not (str1 == "# The following lines are desirable for IPv6 capable hosts\n"):
			if str2 in str1:
				str3 = str1.replace("\n", "")
				print ("found at line "+ str(counter+1)+ " as \""+ str3 +"\"")
				str4 = ('found at line '+str(counter+1)+" as \""+ str3 +"\"")
				list1.append(str4)
				flag = 1
			str1 = sf.readline()
			counter += 1
		if(flag == 0):
			print ("not found")
			str4 = ("not found")
			list1.append(str4)
		sf.close()
	
	def check(self, str2):
		"""Check is an entry exists in the file `/etc/hosts` 
		if exists return True otherwise return False."""
		sf = open (PATH_HOST, "r")
		str1 = sf.readline()
		counter = 1
		while not (str1 == "# The following lines are desirable for IPv6 capable hosts\n"):
			if str2 in str1:
				str1 = str1.replace("\n", "")
				sf.close()
				return True
			counter += 1
			str1 = sf.readline()
		sf.close()
		return False
	
	def add(self, str2, str3):
		"""Add a new entry after the last entry.
		Do not add if the entry already exists."""
		if (self.check(str2) or self.check(str3)):
			print ("Failed! Either IP address or Hostname already exists")
			return
		for i in range(len(str2),16):
			str2 = str2 + " "
		str1 = list()
		index = -1
		with open(PATH_HOST, "r") as f:
			for line in f:
				if (line == "# The following lines are desirable for IPv6 capable hosts\n"):
					break
				else:
					index += 1
		counter = 0 
		with open(PATH_HOST, "r") as f:
			for line in f:
				str1.append(line)
				counter += 1
				if(counter == index):
					str1.append(str2 + str3 + "\n")
		with open(PATH_HOST, "w") as f:
			for line in str1:
				f.write(line)
		print ("\""+str2 + str3+"\"" +" added ")
	
	def remove(self, str3):
		"""Remove the line at given index.
		Return a notification if index is out of bounds."""
		list1 = list()
		index = (int(str3) - 1)
		counter = 0
		flag = 0
		with open(PATH_HOST, "r") as f:
			for line in f:
				list1.append(line)
				if (line ==  "# The following lines are desirable for IPv6 capable hosts\n"):
					flag = 1
			
				if (flag == 0):
					counter += 1
		if(index >= counter):
			print ("Failed! Index is out of bounds")
			return
		str4 = list1.pop(index)
		str4 = str4.replace("\n", "")
		rmf = open(PATH_HOST, "w+")
		for line in list1:
			rmf.write(line)
		rmf.close()
		print ("\""+str4+"\""+" removed ")
	
	def edit(self, str4, str2, str3):
		"""Update the content of the line at given index.
		Return a notification if index is out of bounds."""
		index = int(str4) -1
		counter = 0
		str1 = list()
		for i in range(len(str2),16):
			str2 = str2 + " "
		flag=0
		with open(PATH_HOST, "r") as f:
			for line in f:
				if (line ==  "# The following lines are desirable for IPv6 capable hosts\n"):
					flag = 1
				if (flag == 0):
					counter += 1
		if(index >= counter):
			print ("Failed! Index is out of bounds")
			return
		counter = 0
		with open(PATH_HOST, "r") as f:
			for line in f:
				if (counter == index):
					str1.append(str2+str3+"\n")
					counter +=1
					continue
				str1.append(line)
				counter += 1
		with open(PATH_HOST, "w") as f:
			for line in str1:
				f.write(line)
		print ("line "+ str(index+1)+ " changed to "+ "\""+ str2+ str3+ "\""+ "\n\n")
	
	def add_ldapServer(self):
		"""Get the IP address and the name of the LDAP server from
		the output of the terminal command `net ads info` and
		add this as a new entry to the file `/etc/hosts`."""
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
		self.add(ip_address, hostname.lower())
	
	def update_hostname(self, hostname):
		"""Update the hostname of the entry 
		with the IP address `127.0.1.1`."""
		etc_hosts = list()
		with open(PATH_HOST, "r") as host:
			for line in host:
				if ("127.0.1.1") in line:
					etc_hosts.append("127.0.1.1       "+
					hostname+ "\n")
				else:
					etc_hosts.append(line)
		with open(PATH_HOST, "w") as host:
			for line in etc_hosts:
				host.write(line)
	
	def add_realm(self, hostname, realm):
		"""Update the hostname of the entry 
		with the IP address `127.0.1.1` and
		add the given realm to the entry."""
		etc_hosts = list()
		with open(PATH_HOST, "r") as host:
			for line in host:
				if ("127.0.1.1") in line:
					etc_hosts.append("127.0.1.1       "+
					hostname+ "       "+
					hostname+ "."+realm.lower()+ "\n")
				else:
					etc_hosts.append(line)
		with open(PATH_HOST, "w") as host:
			for line in etc_hosts:
				host.write(line)
	
	def set(self, hostname):
		"""Update the content of the file `/etc/hostname`."""
		with open("/etc/hostname", "w") as host:
			host.write(hostname+ "\n")
	
	def update_xauth(self, hostname):
		"""Make necessary display reconfigurations."""
		oldHostname = self.get()
		os.system('%s' % ("hostname "+ hostname))
		os.system('xauth add `echo $(hostname)/$(xauth list | cut -d" " -f1 | cut -d"/" -f2) $(xauth list | cut -d" " -f3,5)`')
		if not(oldHostname == hostname):
			os.system('xauth remove $(echo $(xauth list | head -1 | cut -d" " -f1))')
	
class Kerberos:
	
	def create(self, default_realm):
		"""Create `/etc/krb5.conf` file with a fixed format 
		and set the given realm as default realm."""
		kerberos = open(LOCATION, "w")
		kerberos.write("[logging]\n")
		kerberos.write("default=FILE:/var/log/krb5.log\n")
		kerberos.write("\n")
		kerberos.write("[libdefaults]\n")
		kerberos.write("default_realm = "+ default_realm.upper()+ "\n")
		kerberos.write("clock_skew = 300\n")
		kerberos.write("ticket_lifetime = 24000\n")
		kerberos.write("\n")
		kerberos.write("[realms]\n")
		kerberos.write("\n")
		kerberos.write("[domain_realm]\n")
		kerberos.write("\n")
		kerberos.write("[login]\n")
		kerberos.write("krb4_convert = true\n")
		kerberos.write("krb4_get_tickets = false\n")
		kerberos.write("\n")
		kerberos.write("[appdefaults]\n")
		kerberos.write("pam = {\n")
		kerberos.write("debug = false\n")
		kerberos.write("ticket_lifetime = 36000\n")
		kerberos.write("renew_lifetime = 36000\n")
		kerberos.write("forwardable = true\n")
		kerberos.write("krb4_convert = false\n")
		kerberos.write("}\n")
		kerberos.close()
		print ("kerberos.txt succesfully created.")
		self.add_realm(default_realm)
	
	def read(self):
		"""Return the content of `/etc/krb5.conf`."""
		content = list()
		with open(PATH_KERBEROS, "r") as kerberos:
			for line in kerberos:
				content.append(line)
		return content
	
	def set_default_realm(self, realm):
		"""Update the default realm of `/etc/krb5.conf`."""
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
	
	def add_domain(self, realm):
		"""Add a new domain entry to `/etc/krb5.conf`. 
		Return a notification if already exists in the file."""
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
	
	def add_realm(self, realm):
		"""Add a new realm entry to `/etc/krb5.conf`. 
		Return a notification if already exists in the file."""
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
	
	def add_server(self, realm, server, hostname):
		"""Take the server and the server type as argument
		add it as a server entry to the given realm.
		Return a notification if the server entry 
		already exists in the given realm."""
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
	
	def configure(self):
		"""Check some kerberos configurations.
		Make necessary configurations if they are not set."""
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
	
class Samba:
	
	def set(self, hostname, realm, workgroup):
		with open(PATH_SAMBA, "w") as samba:
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
	
	def read(self):
		content = list()
		with open(PATH_SAMBA, "r") as samba:
			for line in samba:
				content.append(line)
		return content
	
	def update(self, hostname):
		smb = list()
		with open(PATH_SAMBA, "r") as samba:
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
		with open(PATH_SAMBA, "w") as samba:
			for line in smb:
				samba.write(line)
	
	def get_realm(self):
		with open(PATH_SAMBA, "r") as samba:
			for line in samba:
				if(("realm = ") in line):
					return (line.replace("realm = ",""))
			return ("WORKGROUP")
	
	def get_workgroup(self):
		with open(PATH_SAMBA, "r") as samba:
			for line in samba:
				if ("workgroup =") in line:
					return line.replace("workgroup = ","")
	
	def get_domain_info(self, domain):
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
	
class Domain:
	
	def add(self, hostname, realm, password_user):
		text = ""
		text = text + ((os.popen('echo %s|kinit %s' % (password_user,hostname+"@"+realm.upper())).read()))
		text = text + ((os.popen('klist').read()))
		text = text + ((os.popen('echo %s|%s' % (password_user, "net ads join -U "+ hostname)).read()))
		return (text)
	
	def confirm(self):
		check = ""
		check = (os.popen('%s' % ("net ads join -k")).read())
		return (check)
	
	def configure_pam(self):
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
	
	def add_server(self):
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
		kerberos = Kerberos()
		kerberos.add_server(realm.lower(), ("kdc"), s.lower())
		kerberos.add_server(realm.lower(), ("admin_server"), s.lower())
