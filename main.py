import pygtk
pygtk.require("2.0")
import gtk

class Hello:
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
				confirmBox = ConfirmBox()
				confirmBox.confirmBox()

		def __init__(self):
				self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
				#self.window.connect("delete_event", self.delete_event)
				self.window.connect("destroy", self.destroy)
				self.window.set_border_width(10)
				self.button = gtk.Button("Exit")
				self.button.connect("clicked", self.terminateConfirm, None)
				self.window.add(self.button)
				self.button.show()
				self.window.show()

		def main(self):
				gtk.main()

class ConfirmBox:
		def destroy(self, widget, data=None):
			gtk.main_quit()

		def confirmBox(self):
				self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
				self.window.connect("destroy", self.destroy)
				self.buttonOK = gtk.Button(stock=gtk.STOCK_OK)
				self.buttonCancel = gtk.Button(stock=gtk.STOCK_CANCEL)
				self.box = gtk.VBox()
				self.buttonBox = gtk.HButtonBox()
				self.buttonBox.set_layout(gtk.BUTTONBOX_END)
				self.buttonBox.set_spacing(10)
				self.buttonBox.add(self.buttonOK)
				self.buttonBox.add(self.buttonCancel)
				self.box.pack_start(self.buttonBox)
				self.buttonOK.show()
				self.buttonCancel.show()
				self.buttonBox.show()
				self.window.add(self.box)
				self.box.show()
				self.window.show()

if __name__ == "__main__":
		hello = Hello()
		hello.main()
