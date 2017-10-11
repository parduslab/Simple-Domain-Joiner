#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
GUI module of Simple Domain Joiner
"""

#Libraries
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sdj import*

#A global variable that holds the state of `winbind`.
#Equals to 1 if winbind is added to `/etc/nsswitch.conf`otherwise equals to 0
global WINBIND

#main function of the module
def mainDomain():
	
	#Handler class of the main window of the GUI.
	class Handler:
		def onDeleteWindow(self, *args):
			"""Delete-event handler"""
			Gtk.main_quit(*args)
		
		def onButton1Pressed(self, button1):
			"""Button-press-event handler for the `confirm` button.
			Check if `winbind` is on or off.
			If `winbind` is on check if the domain is valid.
			If the domain is valid run required methods to join the domain.
			If the domain is not valid display an error window.
			If `winbind` is off only run methods that are required to update the hostname."""
			hosts = Host()
			samba = Samba()
			nsswitch = Nsswitch()
			global WINBIND
			if (WINBIND > 0):
				nsswitch.on()
			else:
				nsswitch.off()
			entry1 = builder.get_object("entry1")
			entry2 = builder.get_object("entry2")
			host = entry1.get_text()
			realm = entry2.get_text()
			if(radio2.get_active()):
				rlist = list()
				rlist = samba.get_domain_info(realm)
				if(rlist[0] == "error"):
					builderInvIp.add_from_file("/usr/share/sdj/glades/domain_invalid_ip.glade")
					windowInvIp = builderInvIp.get_object("window1")
					windowInvIp.show_all()
					builderInvIp.connect_signals(HandlerInvIp())
				else:
					realm = rlist[0]
					workgroup = rlist[1]
					builder2.add_from_file("/usr/share/sdj/glades/domain_add.glade")
					window2 = builder2.get_object("window1")
					button_add_confirm = builder2.get_object("button1")
					entry_add_passw = builder2.get_object("entry2")
					entry_add_passw.set_activates_default(True)
					button_add_confirm.set_can_default(True)
					button_add_confirm.grab_default()
					window2.show_all()
					builder2.connect_signals(Handler2(host, realm, workgroup))
			else:
				hosts = Host()
				samba = Samba()
				current_name = hosts.get()
				current_workgroup = samba.get_workgroup()
				hosts.set(host)
				hosts.update_hostname(host)
				samba.update(host)
				builder3.add_from_file("/usr/share/sdj/glades/domain_update_host.glade")
				window3 = builder3.get_object("window1")
				label = builder3.get_object("label1")
				if not(current_workgroup == samba.get_workgroup()) and not(current_name == hosts.get()):
					label.set_text("Domain has changed to local\nHostname has updated to \""+host+"\".")
				elif not(current_name == hosts.get()) and (current_workgroup == samba.get_workgroup()):
					label.set_text("Hostname has changed to \""+host+"\".") 
				elif not(current_workgroup == samba.get_workgroup()) and (current_name == hosts.get()):
					label.set_text("Domain has changed to local.")
				else:
					label.set_text("Nothing has changed.")
				window3.show_all()
				builder3.connect_signals(Handler3())
		
		def onButton2Pressed(self, radiobutton2):
			"""Button-press-event handler for the winbind-on radio-button."""
			entry2 = builder.get_object("entry2")
			entry2.set_editable(True)
			act_win(1)
		
		def onButton3Pressed(self, radiobutton1):
			"""Button-press-event handler for the winbind-off radio-button."""
			entry2 = builder.get_object("entry2")
			entry2.set_editable(False)
			act_win(0)
		
		def onButton4Pressed(self, button4):
			"""Button-press-event handler for the `cancel` button."""
			window2 = builder.get_object("window1")
			window2.destroy()
			
		def onButton5Pressed(self, button_about):
			"""Button-press-event handler for the `about` button."""
			builderAbout.add_from_file("/usr/share/sdj/glades/about.glade")
			aboutWindow = builderAbout.get_object("window1")
			revealer = builderAbout.get_object("revealer1")
			licenseButton = builderAbout.get_object("button1")
			licenseButton.connect("clicked", reveal)
			devButton = builderAbout.get_object("button2")
			devButton.connect("clicked", reveal)
			linkButton = builderAbout.get_object("linkButton")
			linkButton.set_label("Project link")
			builderAbout.connect_signals(AboutHandler())
			aboutWindow.show_all()
		
	#Handler class of the login-window. 
	class Handler2():
		
		def __init__(self, host, realm, workgroup):
			"""constructor method that creates required objects 
			to access the necessary methods for joining the domain. """
			self.host = host
			self.realm = realm
			self.workgroup = workgroup
		
		def onDeleteWindow(self, *args):
			"""Delete-event handler"""
			Gtk.main_quit(*args)
		
		def onButton1Pressed(self, button1):
			"""Button-press-event handler for the `confirm` button.
			Call required methods to join the domain and to make 
			all the necesssary configurations.
			If succesfully joins the domain display a success message.
			otherwise display the error window related with the error."""
			hosts = Host()
			kerberos = Kerberos()
			samba = Samba()
			domain = Domain()
			entry1 = builder2.get_object("entry1")
			entry2 = builder2.get_object("entry2")
			entry3 = builder.get_object("entry2")
			domain = Domain()
			kerberos = Kerberos()
			userName = entry1.get_text()
			host = self.host
			password_host = entry2.get_text()
			realm = self.realm
			workgroup = self. workgroup
			hosts.set(host)
			hosts.add_realm(host, realm)
			samba.set(host, realm, workgroup)
			kerberos.add_realm(realm)
			kerberos.add_domain(realm)
			kerberos.set_default_realm(realm)
			hosts.add_ldapServer()
			domain.add_server()
			output = domain.add(userName, realm, password_host)
			domain.configure_pam()
			kerberos.configure()
			hosts.update_xauth(host)
			check = domain.confirm()
			print (check)
			success = list()
			success.append("Joined")
			success.append("to dns domain")
			error1 = "No credentials cache found"
			error2 = "Our netbios name can be at most 15 chars long"
			error3 = "Client's credentials have been revoked while getting initial credentials"
			error4 = "Password incorrect while getting initial credentials"
			error5 = "failed to find DC for domain"
			error6 = "Logon failure"
			error7 = "Failed to set account flags for machine account"
			
			builder_err1.add_from_file("/usr/share/sdj/glades/domain_err1.glade")
			window = builder_err1.get_object("window1")
			window.show_all()
			
			if((success[0] in check) and (success[1] in check)):
				builder_success.add_from_file("/usr/share/sdj/glades/domain_success.glade")
				window = builder_success.get_object("window1")
				ltest = list()
				buffer_text = ""
				for c in check:
					if(c == "\n"):
						ltest.append(buffer_text)
						buffer_text = ""
					else:
						buffer_text = buffer_text + c
				for line in ltest:
					if ("Joined") in line:
						text1 = line
				label = builder_success.get_object("label1")
				label.set_text(text1)
				
				builder_success.connect_signals(HandlerSuccess())
				window2 = builder2.get_object("window1")
				window2.destroy()
			elif(error1 in output):
				errorTextContent="User not found in database!"
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				builder_err1.connect_signals(HandlerError1())
			elif(error2 in output):
				errorTextContent="Computer Name too long!"
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				errorTextContent2="Computer name can not be longer than 15 characters."
				label2 = builder_err1.get_object("errorText2")
				label2.set_text(errorTextContent2)
				builder_err1.connect_signals(HandlerError2())
			elif(error3 in output):
				errorTextContent="Too many failed attempts! Account locked out.\
					Wait a few minutes to try again."
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				builder_err1.connect_signals(HandlerError3())
			elif(error4 in output):
				errorTextContent="Unauthorized user or incorrect password."
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				builder_err1.connect_signals(HandlerError4())
			elif(error5 in output):
				errorTextContent="Realm not found."
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				builder_err1.connect_signals(HandlerError5())
			elif(error6 in output):
				errorTextContent="Incorrect password."
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				builder_err1.connect_signals(HandlerError6())
			elif(error7 in output) or (error7 in check):
				errorTextContent="Failed to Join Domain!"
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				errorTextContent2="This computer name already exist in this domain."
				label2 = builder_err1.get_object("errorText2")
				label2.set_text(errorTextContent2)
				builder_err1.connect_signals(HandlerError7())
			else:
				errorTextContent="Failed to Join Domain!"
				label1 = builder_err1.get_object("errorText")
				label1.set_text(errorTextContent)
				errorTextContent2="An unknown error occured."
				label2 = builder_err1.get_object("errorText")
				label2.set_text(errorTextContent2)
				builder_err1.connect_signals(HandlerError8())
		
		def onButton2Pressed(self, button2):
			"""Button-press-event handler for the `cancel` button."""
			window2 = builder2.get_object("window1")
			window2.destroy()
			
	#Handler classes of the other windows.
	class HandlerError3:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerError6:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerError5:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerError4:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerError1:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerError2:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerSuccess:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_success.get_object("window1")
			window.destroy()
	class Handler3:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder3.get_object("window1")
			window.destroy()
	class HandlerError7:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class HandlerError8:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		def onButton1Pressed(self, button1):
			window = builder_err1.get_object("window1")
			window.destroy()
	class AboutHandler:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
			
		def onButton3Pressed(self, button3):
			aboutWindow = builderAbout.get_object("window1")
			aboutWindow.destroy()
	
		def onButton1Pressed(self, button1):
			lis = ""
			with open("license.txt", "r") as license_text:
				for line in license_text:
					lis = lis + line
			text = builderAbout.get_object("text1")
			textbuffer = text.get_buffer()
			textbuffer.set_text(lis)
	
		def onButton2Pressed(self, button2):
			text = builderAbout.get_object("text1")
			textbuffer = text.get_buffer()
			textbuffer.set_text("Emre Balcı (ebalci@gmail.com) \n \
Ali Orhun Akkirman (aoakkirman@gmail.com) ")
	
	class HandlerInvIp:
		def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)
		
		def onButton1Pressed(self, button1):
			windowInvIp = builderInvIp.get_object("window1")
			windowInvIp.destroy()
	
	def reveal(self):
		"""Activate the revealer in the `about` window."""
		revealer = builderAbout.get_object("revealer1")
		revealer.set_reveal_child(not revealer.get_reveal_child())
	
	def act_win(arg):
		global WINBIND
		WINBIND = arg
		
	global WINBIND
	
	#Create Gtk objects to build the GUI.
	builder = Gtk.Builder()
	builder2 = Gtk.Builder()
	builder_err1 = Gtk.Builder()
	builder_success = Gtk.Builder()
	builder3 = Gtk.Builder()
	builderAbout = Gtk.Builder()
	builderInvIp = Gtk.Builder()
	samba = Samba()
	host = Host()
	nsswitch = Nsswitch()
	builder.add_from_file("/usr/share/sdj/glades/domain.glade")
	window = builder.get_object("window1")
	cancel_button = builder.get_object("cancel_button")
	label = builder.get_object("label1")
	radio1 = builder.get_object("radiobutton1")
	radio2 = builder.get_object("radiobutton2")
	entry_username = builder.get_object("entry1")
	entry_realm = builder.get_object("entry2")
	computer_name = host.get()
	entry_username.set_text(computer_name)
	entry_realm.set_text(samba.get_realm().replace("\n",""))
	
	#Check if `winbind` is on or off. 
	#If it is on set the second entry editable set uneditable otherwise. 
	winbind = nsswitch.check()
	if (winbind == "removed"):
		radio1.set_active(True)
		radio2.set_active(False)
		entry2 = builder.get_object("entry2")
		entry2.set_editable(False)
		WINBIND = 0
	else:
		radio1.set_active(False)
		radio2.set_active(True)
		entry2 = builder.get_object("entry2")
		entry2.set_editable(True)
		WINBIND = 1
	button_confirm = builder.get_object("button1")
	entry_realm.set_activates_default(True)
	entry_username.set_activates_default(True)
	button_confirm.set_can_default(True)
	button_confirm.grab_default()
	window.show_all()
	builder.connect_signals(Handler())
	window.connect("destroy", Gtk.main_quit)
	Gtk.main()

#Call the main function.
def main():
	mainDomain()

if __name__ == "__main__":
    main()
