import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gedit', '3.0')

from gi.repository import GObject, Gtk, Gedit


class PanelTogglerWindowActivatable(GObject.Object, Gedit.WindowActivatable):

	window = GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)

		self._header_bar    = None
		self._panel_sidebar = None
		self._left_button   = None
		self._bottom_button = None

	def do_activate(self):
		self._header_bar    = find_widget(self.window, "headerbar")
		self._panel_sidebar = find_widget(self.window, "bottom_panel_sidebar")
		self._button_box    = Gtk.Box()
		self._left_button   = Gtk.Button(image=image_file("left"))
		self._bottom_button = Gtk.Button(image=image_file("bottom"))

		self._button_box.get_style_context().add_class("linked")
		self._bottom_button.connect("clicked", self.on_bottom_button_activated)
		self._left_button.connect("clicked", self.on_left_button_activated)

		self._header_bar.pack_end(self._button_box)
		self._button_box.pack_end(self._bottom_button, True, True, 0)
		self._button_box.pack_end(self._left_button, True, True, 1)

		self._button_box.show()
		self._left_button.show()
		self._bottom_button.show()
		self._panel_sidebar.hide()

	def do_deactivate(self):
		self._left_button.destroy()
		self._bottom_button.destroy()
		self._button_box.destroy()
		self._panel_sidebar.show()

	def on_left_button_activated(self, _button):
		panel = self.window.get_side_panel()
		status = not panel.get_property("visible")

		panel.set_property("visible", status)

	def on_bottom_button_activated(self, _button):
		panel = self.window.get_bottom_panel()
		status = not panel.get_property("visible")

		panel.set_property("visible", status)


def find_widget(widget, widget_id):
	if Gtk.Buildable.get_name(widget) == widget_id:
		return widget

	if not hasattr(widget, "get_children"):
		return None

	for child in widget.get_children():
		ret = find_widget(child, widget_id)

		if ret:
			return ret

	return None


def image_file(image):
	path = os.path.dirname(__file__)
	icon = "/icons/gedit-view-" + image + "-pane-symbolic.svg"

	return Gtk.Image.new_from_file(path + icon)
