import pygtk
pygtk.require("2.0")
import gtk

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

		def remove_row(self, widget, data=None):
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

		def __init__(self):
				self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
				#self.window.connect("delete_event", self.delete_event)
				self.window.connect("destroy", self.destroy)
				self.window.set_border_width(5)

				#setting label ( 1st line )
				label = gtk.Label()
				label.set_markup("<b>OnionWebShare</b>")
				#label.set_justify(gtk.JUSTIFY_LEFT)
				label.show()

				#setting btnbox ( 2nd line )
				btnbox = gtk.HButtonBox()
				btnbox.set_layout(gtk.BUTTONBOX_END)
				btnbox.set_spacing(5)

				self.lblrfname = gtk.Label("/")
				self.lblrfname.show()

				btnbox.add(self.lblrfname)
				btnbox.add(self.make_button("Select", "clicked", self.addFile))
				btnbox.add(self.make_button("Exit", "clicked", self.terminateConfirm))
				btnbox.show()

				#setting add list box ( 3rd line )
				addbox = gtk.HBox()
				addbox.set_spacing(5)

				self.foldername = gtk.Entry()
				self.foldername.show()

				addbox.add(self.foldername)
				addbox.add(self.make_button("Add", "clicked", lambda w, d: self.collist.append([self.foldername.get_text(), self.rfname])))
				addbox.show()

				#setting box ( 4th line )
				linkbox = gtk.HBox()
				linkbox.set_spacing(5)

				lblport = gtk.Label("Server Port : ")
				lblport.show()
				linkbox.pack_start(lblport)

				self.portbox = gtk.Entry()
				self.portbox.show()
				linkbox.pack_start(self.portbox)

				linkbox.pack_start(self.make_button("Start", "clicked", self.startserver))

				linkbox.show()

				#selected folder listview ( 5th line )
				self.collist = gtk.ListStore(str, str)

				f = open("list.conf")
				datas = f.readlines()
				for data in datas:
					arr = data.split(',')
					self.collist.append([arr[0].strip(), arr[1].strip()])

				viewcontainer = gtk.TreeView()
				self.tree = viewcontainer
				viewcontainer.connect("key-press-event", self.remove_row)
				viewcontainer.set_model(self.collist)

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
				top_box.pack_start(addbox) # 3rd line
				top_box.pack_start(linkbox) # 4th line
				top_box.pack_start(viewcontainer) # 5th line
				top_box.show()

				self.window.add(top_box)
				self.window.show()

		def main(self):
				gtk.main()

if __name__ == "__main__":
		mainUI = MainUI()
		mainUI.main()
