#!/usr/bin/env python2
"""
=========================
PlotLatency.py

GUI application example with Matplotlib and GTK+3/Glade
=========================
"""

import gi
from gi.repository import GObject
from gi.repository import Gtk

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
# import matplotlib.pyplot as plt
# from matplotlib.axes import Subplot

import numpy as np
from numpy import arange, sin, pi

gi.require_version('Gtk', '3.0')

global builder, window
global sw_plot, box_plot_ctl
global btn_addfile, btn_rmfile
global tvSections, tvFiles, tvData
global tsSections, tsFiles, tsData
global figure, axis, canvas

class MainWindowSignals(object):

    def on_window_main_destroy(self, widget):
        Gtk.main_quit()

    def on_btn_redraw_click(self, widget):
        global figure, axis, canvas
        figure.delaxes(axis)
        axis = figure.add_subplot(111)

        N = 5
        menMeans = (20, 35, 30, 35, 27)
        womenMeans = (25, 32, 34, 20, 25)
        menStd = (2, 3, 4, 1, 2)
        womenStd = (3, 5, 2, 3, 3)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        p1 = axis.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
        p2 = axis.bar(ind, womenMeans, width,
                      bottom=menMeans, yerr=womenStd)

        axis.set_xlabel('Group')
        axis.set_ylabel('Scores')
        axis.set_title('Scores by group and gender')
        axis.set_xticks(ind, ['G1', 'G2', 'G3', 'G4', 'G5'])
        axis.set_yticks(np.arange(0, 81, 10))
        axis.legend((p1[0], p2[0]), ('Men', 'Women'))
        canvas.draw()
        pass

def main():
    global builder, window
    global sw_plot, box_plot_ctl
    global btn_addfile, btn_rmfile
    global tvSections, tvFiles, tvData
    global tsSections, tsFiles, tsData
    global figure, axis, canvas

    #### # # # # # # # # # # # # #
    ###
    ## DEFINE & INITIALIZE
    #
    builder = Gtk.Builder()
    builder.add_objects_from_file("plotlatency.glade", ("window-main", ""))
    builder.connect_signals(MainWindowSignals())

    window = builder.get_object("window-main")
    # window.connect("delete-event", Gtk.main_quit)

    sw_plot = builder.get_object("scrollw-plot")
    box_plot_ctl = builder.get_object("box-plot-matlibcontrol")

    tvSections = builder.get_object("treeview-sections")
    tvFiles = builder.get_object("treeview-files")
    tvFiles = builder.get_object("treeview-data")

    btn_addfile = builder.get_object("btn-file-add")
    btn_rmfile = builder.get_object("btn-file-remove")
    btn_redraw = builder.get_object("btn-plot-redraw")

    tsSections = Gtk.TreeStore(GObject.TYPE_STRING, GObject.TYPE_BOOLEAN)
    # tsFiles = Gtk.TreeStore(GObject.)
    # tsData = Gtk.TreeStore(GObject.)

    #### # # # # # # # # # # # # #
    ###
    ## EVENTS
    #
    # btn.connect("clicked", onBtnClick)
    # btn.connect("clicked", onBtnClick)

    #### # # # # # # # # # # # # #
    ###
    ## PLOT
    #
    figure = Figure(figsize=(8, 6), dpi=71)
    axis = figure.add_subplot(111)
    t = arange(0.0, 3.0, 0.01)
    s = sin(2*pi*t)
    axis.plot(t, s)

    axis.set_xlabel('time [s]')
    axis.set_ylabel('voltage [V]')

    canvas = FigureCanvas(figure)  # a Gtk.DrawingArea
    canvas.set_size_request(400, 270)
    sw_plot.add_with_viewport(canvas)

    # Create toolbar
    toolbar = NavigationToolbar(canvas, window)
    box_plot_ctl.add(toolbar)

    #### # # # # # # # # # # # # #
    ###
    ## TREEVIEW
    #

    # setup the text cell renderer and allows these
    # cells to be edited.
    renderer = Gtk.CellRendererText()
    renderer.set_property('editable', True)
    # renderer.connect('edited', col0_edited_cb, model)

    # The toggle cellrenderer is setup and we allow it to be
    # changed (toggled) by the user.
    renderer1 = Gtk.CellRendererToggle()
    renderer1.set_property('activatable', True)
    # renderer1.connect('toggled', col1_toggled_cb, model)

    # Connect column0 of the display with column 0 in our list model
    # The renderer will then display whatever is in column 0 of
    # our model .
    column0 = Gtk.TreeViewColumn("Name", renderer, text=0)

    # The columns active state is attached to the second column
    # in the model.  So when the model says True then the button
    # will show as active e.g on.
    column1 = Gtk.TreeViewColumn("Complete", renderer1)
    column1.add_attribute(renderer1, "active", 1)
    tvSections.append_column(column0)
    tvSections.append_column(column1)

    tvSections.set_model(tsSections)

    tsSections.append(None, ("test", None))
    tsSections.append(None, ("test", None))

    tsSections.append(None, ("test2", None))
    tsSections.append(None, ("test2", None))

    #### # # # # # # # # # # # # #
    ###
    ## DONE
    #
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
