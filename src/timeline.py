# minimap.py
#
# Copyright 2018-2021 Romain F. T.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf

class TimelineManager(Gtk.Popover):
	__gtype_name__ = 'TimelineManager'

	def __init__(self, window, **kwargs):
		super().__init__(**kwargs)
		self._window = window
		self.video = []
		self._preview_size = self._window.gsettings.get_int('preview-size')
		self.mini_pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 300, 300)
		self._mini_surface = cairo.ImageSurface(cairo.Format.ARGB32, 5, 5)

		image = self._window.get_active_image()



	def empty_frame(self):
		pass

	def generated_frame(self):
		pass

	def build_frame(self,image):

		self.row = Gtk.Frame(id=self.video)
		self.row.add(image)
		self.row.add(Gtk.Separator())

		button = Gtk.RadioButton(
			relief=Gtk.ReliefStyle.NONE, \
			draw_indicator=False, \
			valign=Gtk.Align.CENTER, \
			tooltip_text=self.label, \
			)

		self._label_widget = Gtk.Label(use_underline=True, label=self.mnemolabel)
		if self.window.gsettings.get_boolean('big-icons'):
			size = Gtk.IconSize.LARGE_TOOLBAR
		else:
			size = Gtk.IconSize.SMALL_TOOLBAR
		image = Gtk.Image().new_from_icon_name(self.icon_name, size)
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		box.add(image)
		box.add(self._label_widget)
		self.row.add(box)
		self.row.show_all()

		return self.row

	############################################################################
################################################################################
