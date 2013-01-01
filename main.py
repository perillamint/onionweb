import pygtk
pygtk.require("2.0")
import gtk
import socket, fcntl, struct

class MainUI:
		#def delete_event(self, widget, event, data=None):
		#		print "Delete event occured."
		#		return False

		def destroy(self, widget, data=None):
				print "Application terminating..."
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
					gtk.main_quit()
				
				confirmBox.destroy()

		def make_button(self, title=None, event_type=None, event_func=None):
			button = gtk.Button(title)
			if event_type is not None and event_func is not None:
				button.connect(event_type, event_func, None)
			button.show()
			return button

		def startserver(self, widget, data=None):
			portnum = self.portbox.get_text()
			if portnum.isdigit() is True and portnum is not None:
				print "Server start. Port : " + portnum
			else:
				print "Wrong port number"

		def __init__(self):
				self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
				#self.window.connect("delete_event", self.delete_event)
				self.window.connect("destroy", self.destroy)
				self.window.set_border_width(10)

				#setting label ( 1st line )
				label = gtk.Label()
				label.set_markup("<b>OnionWebShare</b>")
				#label.set_justify(gtk.JUSTIFY_LEFT)
				label.show()

				#setting btnbox ( 2nd line )
				btnbox = gtk.HButtonBox()
				btnbox.set_layout(gtk.BUTTONBOX_END)
				btnbox.set_spacing(10)
				btnbox.add(self.make_button("test"))
				btnbox.add(self.make_button("test"))
				btnbox.add(self.make_button("test"))
				btnbox.add(self.make_button("Exit", "clicked", self.terminateConfirm))
				btnbox.show()

				#setting box ( 3rd line )
				linkbox = gtk.HBox()
				linkbox.set_spacing(10)

				lblport = gtk.Label("Server Port : ")
				lblport.show()
				linkbox.pack_start(lblport)

				self.portbox = gtk.Entry()
				self.portbox.show()
				linkbox.pack_start(self.portbox)

				linkbox.pack_start(self.make_button("Start", "clicked", self.startserver))

				linkbox.show()

				#selected folder listview ( 4th line )
				collist = gtk.ListStore(str, str)

				f = open("list.conf")
				datas = f.readlines()
				for data in datas:
					arr = data.split(',')
					collist.append([arr[0].strip(), arr[1].strip()])

				viewcontainer = gtk.TreeView()
				viewcontainer.set_model(collist)

				cell = gtk.CellRendererText()
				col = gtk.TreeViewColumn("Name")
				col.pack_start(cell)
				col.add_attribute(cell, 'text', 0)

				cell2 = gtk.CellRendererText()
				col2 = gtk.TreeViewColumn("real path")
				col2.pack_start(cell2)
				col2.add_attribute(cell2, 'text', 1)

				viewcontainer.append_column(col)
				viewcontainer.append_column(col2)

				viewcontainer.show()

				#boxing
				top_box = gtk.VBox(spacing = 5)
				top_box.pack_start(label) # 1st line
				top_box.pack_start(btnbox) # 2nd line
				top_box.pack_start(linkbox) # 3rd line
				top_box.pack_start(viewcontainer) # 4th line
				top_box.show()

				self.window.add(top_box)
				self.window.show()

		def main(self):
				gtk.main()

class ConfirmBox:
		def destroy(self, widget, data=None):
			self.window.destroy()

		def confirmBox(self, msgText):
				self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
				self.window.connect("destroy", self.destroy)
				self.buttonOK = gtk.Button(stock=gtk.STOCK_OK)
				self.buttonCancel = gtk.Button(stock=gtk.STOCK_CANCEL)
				self.buttonCancel.connect("clicked", self.destroy)
				self.box = gtk.VBox()
				self.label = gtk.Label(msgText)

				#Create buttonBox.
				self.buttonBox = gtk.HButtonBox()
				self.buttonBox.set_layout(gtk.BUTTONBOX_END)
				self.buttonBox.set_spacing(10)

				#Add buttons to buttonBox
				self.buttonBox.add(self.buttonOK)
				self.buttonBox.add(self.buttonCancel)

				#Pack everything in VBox
				self.box.pack_start(self.label)
				self.box.pack_start(self.buttonBox)
				
				#Show everything
				self.buttonOK.show()
				self.buttonCancel.show()
				self.buttonBox.show()
				self.label.show()
				self.window.add(self.box)
				self.box.show()
				self.window.show()

if __name__ == "__main__":
		mainUI = MainUI()
		mainUI.main()
