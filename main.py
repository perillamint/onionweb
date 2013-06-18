#!/usr/bin/env python
# -*- coding: utf-8
# author: KBuild, Maneulyori, sookcha
# email: qwer7995@gmail.com(KBuild), maneulyori@gmail.com(Maneulyori), lsookcha@me.com(sookcha)

import pygtk
pygtk.require("2.0")
import gtk
import os, signal
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from  server import Server
import subprocess

class MainUI:
		#def delete_event(self, widget, event, data=None):
		#		print "Delete event occured."
		#		return False

		def destroy(self, widget, data=None):
				print "Application terminating..."
				self.saveConfig()
				self.stopServerFunc()
				gtk.main_quit()

		def closeWindow(self, widget, data=None):
				closeWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
				closeWindow.set_border_width(10)
				closeWindow.show()

		def terminateConfirm(self, widget, data=None):
				confirmBox = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK_CANCEL)
				confirmBox.set_markup("This will close onionwebshare server. Are you sure?")
				userAnswer = confirmBox.run()
				if userAnswer == gtk.RESPONSE_OK:
					self.saveConfig()
					self.stopServerFunc()
					gtk.main_quit()
				
				confirmBox.destroy()

		def makeButton(self, title=None, event_type=None, event_func=None):
			button = gtk.Button(title)
			if event_type is not None and event_func is not None:
				button.connect(event_type, event_func, None)
			button.show()
			return button

		def startServer(self, widget, data=None):
			portnum = self.portbox.get_text()
			if portnum.isdigit() is True and portnum is not None and int(portnum) > 1024:
				cmd = "python server.py " + str(portnum)
				if self.p is None:
					self.p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
					print "Server start. Port : " + portnum
					self.statusLabel.set_markup("<b>Started</b>")
				else:
					print "Server is already binded"
#				pid = os.fork()
#				if pid == 0:
#					fp = open("owsserver.pid", "w")
#					fp.write(str(os.getpid()))
#					fp.close()
#					self.serverFunc(int(portnum))
#				return
			else:
				print "Wrong port number"

		def stopServer(self, widget, data=None):
			self.stopServerFunc();
			self.statusLabel.set_markup("<b>Stopped</b>")

		def stopServerFunc(self):
			if self.p is None:
				print "Already process killed"
			else:
				pid = self.p.pid
				os.kill(pid, signal.SIGTERM)
				os.kill(pid+1, signal.SIGTERM)
				self.p = None
				print "Sever stopped"


		def serverFunc(self, portnum):
			self.server = HTTPServer(('localhost', portnum), Server)
			self.server.serve_forever()

		def removeRow(self, widget, data=None):
			if data.keyval != 65535:
				return False
			selection = self.tree.get_selection()
			selection.set_mode(gtk.SELECTION_SINGLE)
			treemodel, treeiter = selection.get_selected()
			self.collist.remove(treeiter)

		def addFile(self, widget, data=None):
			filechooser = gtk.FileChooserDialog(title="Choose file to host", action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
			filechooser.set_current_folder("~")
			filechooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
			response = filechooser.run()

			if response == gtk.RESPONSE_OK:
				sfile = filechooser.get_filename()
				print sfile, 'selected'
				if len(sfile) > 15:
					self.lblrfname.set_text(sfile[:15] + '...')
					self.rfname = sfile
			filechooser.destroy()

		def openShared(self, widget, data = None):
			self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
			self.window.set_border_width(10)

			btnbox = gtk.HButtonBox()
			btnbox.set_layout(gtk.BUTTONBOX_END)
			btnbox.set_spacing(5)

			self.lblrfname = gtk.Label("/")
			self.rfname = "/"
			self.lblrfname.show()

			btnbox.add(self.lblrfname)

			btnbox.add(self.makeButton("Select", "clicked", self.addFile))
			btnbox.add(self.makeButton("Exit", "clicked", self.terminateConfirm))
			btnbox.show()

			#setting add list box ( 4th line )
			addbox = gtk.HBox()
			addbox.set_spacing(5)

			lbltitle = gtk.Label("Title : ")
			lbltitle.show()

			self.foldername = gtk.Entry()
			self.foldername.show()

			addbox.add(lbltitle)
			addbox.add(self.foldername)
			addbox.add(self.makeButton("Add", "clicked", lambda w, d: self.collist.append([self.foldername.get_text(), self.rfname])))
			addbox.show()

			#selected folder listview ( 5th line )
			self.collist = gtk.ListStore(str, str)

			f = open("list.conf")
			datas = f.readlines()
			for data in datas:
				arr = data.split(',')
				self.collist.append([arr[0].strip(), arr[1].strip()])
			f.close()

			viewcontainer = gtk.TreeView()
			self.tree = viewcontainer
			viewcontainer.connect("key-press-event", self.removeRow)
			viewcontainer.set_model(self.collist)

			cell = gtk.CellRendererText()
			col = gtk.TreeViewColumn("Name")
			col.pack_start(cell)
			col.add_attribute(cell, 'text', 0)

			cell2 = gtk.CellRendererText()
			col2 = gtk.TreeViewColumn("Real path")
			col2.pack_start(cell2)
			col2.add_attribute(cell2, 'text', 1)

			viewcontainer.append_column(col)
			viewcontainer.append_column(col2)

			viewcontainer.show()

			settingsBox = gtk.VBox(spacing = 5)
			settingsBox.pack_start(btnbox)
			settingsBox.pack_start(addbox)
			settingsBox.pack_start(viewcontainer)
			settingsBox.show()

			self.window.add(settingsBox)
			self.window.show()

		def saveConfigFile(self, model, path, iter, confFp):
			str = model.get_value(iter, 0)
			str += ","
			str += model.get_value(iter, 1)
			str += "\n"
			confFp.write(str)
	
		def saveConfig(self):
			f = open("list.conf", "w")
			self.collist.foreach(self.saveConfigFile, f)
			f.close()

		def __init__(self):
			self.p = None
			self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
			#self.window.connect("delete_event", self.delete_event)
			self.window.connect("destroy", self.destroy)
			self.window.set_border_width(5)

			#setting label ( 1st line )
			label = gtk.Label()
			label.set_markup("<b>OnionWebShare</b>")
			#label.set_justify(gtk.JUSTIFY_LEFT)
			label.show()

			#setting box ( 2nd line )
			linkbox = gtk.HBox()
			linkbox.set_spacing(5)

			lblport = gtk.Label("Server Port : ")
			lblport.show()
			linkbox.pack_start(lblport)

			self.portbox = gtk.Entry()
			self.portbox.set_text("8800");
			self.portbox.show()
			linkbox.pack_start(self.portbox)

			linkbox.pack_start(self.makeButton("Start", "clicked", self.startServer))
			linkbox.pack_start(self.makeButton("Stop", "clicked", self.stopServer))

			linkbox.show()

			self.statusLabel = gtk.Label()
			self.statusLabel.set_markup("<b>Stopped</b>")
			self.statusLabel.show()

			#setting btnbox ( 3rd line )
			btnbox = gtk.HButtonBox()
			btnbox.add(self.makeButton("Shared directory","clicked", self.openShared))
			btnbox.show()


			#boxing
			self.top_box = gtk.VBox(spacing = 5)
			self.top_box.pack_start(label) # 1st line
			self.top_box.pack_start(linkbox) # 2nd line
			self.top_box.pack_start(self.statusLabel) # 3rd line
			self.top_box.pack_start(btnbox) # 4td line
			self.top_box.show()

			self.window.add(self.top_box)
			self.window.show()

		def main(self):
				gtk.main()

if __name__ == "__main__":
		mainUI = MainUI()
		mainUI.main()