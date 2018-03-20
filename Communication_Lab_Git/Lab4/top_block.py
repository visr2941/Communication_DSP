#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sat Feb 27 03:40:12 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from numpy import *
from optparse import OptionParser
from pam11_gnu import *
from scipy import *
import sip
import sys


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.NTd = NTd = 50
        self.N = N = NTd + 10
        self.L = L = 2
        self.dn = dn = floor(L*random.random(N))
        self.fs = fs = 32000
        self.fb = fb = 200
        self.an = an = 2*dn - (L-1)
        self.rt = rt = pam11(an, fb, fs, 'sinc', [20, 0])
        self.dly = dly = 0.5

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	fs, #samp_rate
        	"", #name
        	9 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(9):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_vector_source_x_0_4 = blocks.vector_source_f(rt[fs*3/fb:fs*6/fb], True, 1, [])
        self.blocks_vector_source_x_0_3 = blocks.vector_source_f(rt[fs*6/fb:fs*9/fb], True, 1, [])
        self.blocks_vector_source_x_0_2 = blocks.vector_source_f(rt[fs*9/fb:fs*12/fb], True, 1, [])
        self.blocks_vector_source_x_0_0_0_0_0_0 = blocks.vector_source_f(rt[fs*24/fb:fs*27/fb], True, 1, [])
        self.blocks_vector_source_x_0_0_0_0_0 = blocks.vector_source_f(rt[fs*21/fb:fs*24/fb], True, 1, [])
        self.blocks_vector_source_x_0_0_0_0 = blocks.vector_source_f(rt[fs*18/fb:fs*21/fb], True, 1, [])
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_f(rt[fs*15/fb:fs*18/fb], True, 1, [])
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f(rt[fs*12/fb:fs*15/fb], True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_f(rt[0:fs*3/fb], True, 1, [])
        self.blocks_throttle_0_4 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_3 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_2 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_0_0_0_0_0 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_0_0_0_0 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_0_0_0 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_0_0 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_float*1, fs,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, fs,True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 4))    
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_time_sink_x_0, 7))    
        self.connect((self.blocks_throttle_0_0_0, 0), (self.qtgui_time_sink_x_0, 5))    
        self.connect((self.blocks_throttle_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 6))    
        self.connect((self.blocks_throttle_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.blocks_throttle_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 2))    
        self.connect((self.blocks_throttle_0_2, 0), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.blocks_throttle_0_3, 0), (self.qtgui_time_sink_x_0, 3))    
        self.connect((self.blocks_throttle_0_4, 0), (self.qtgui_time_sink_x_0, 8))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_throttle_0_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_throttle_0_0_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.blocks_throttle_0_0_0_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0_0_0_0, 0), (self.blocks_throttle_0_0_0_0_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0_0_0_0_0, 0), (self.blocks_throttle_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_vector_source_x_0_2, 0), (self.blocks_throttle_0_2, 0))    
        self.connect((self.blocks_vector_source_x_0_3, 0), (self.blocks_throttle_0_3, 0))    
        self.connect((self.blocks_vector_source_x_0_4, 0), (self.blocks_throttle_0_4, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_NTd(self):
        return self.NTd

    def set_NTd(self, NTd):
        self.NTd = NTd
        self.set_N(self.NTd + 10)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_dn(floor(self.L*random.random(self.N)))

    def get_L(self):
        return self.L

    def set_L(self, L):
        self.L = L
        self.set_an(2*self.dn - (self.L-1))
        self.set_dn(floor(self.L*random.random(self.N)))

    def get_dn(self):
        return self.dn

    def set_dn(self, dn):
        self.dn = dn
        self.set_an(2*self.dn - (self.L-1))

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.set_rt(pam11(self.an, self.fb, self.fs, 'sinc', [20, 0]))
        self.blocks_throttle_0.set_sample_rate(self.fs)
        self.blocks_throttle_0_0.set_sample_rate(self.fs)
        self.blocks_throttle_0_0_0.set_sample_rate(self.fs)
        self.blocks_throttle_0_0_0_0.set_sample_rate(self.fs)
        self.blocks_throttle_0_0_0_0_0.set_sample_rate(self.fs)
        self.blocks_throttle_0_0_0_0_0_0.set_sample_rate(self.fs)
        self.blocks_throttle_0_2.set_sample_rate(self.fs)
        self.blocks_throttle_0_3.set_sample_rate(self.fs)
        self.blocks_throttle_0_4.set_sample_rate(self.fs)
        self.blocks_vector_source_x_0.set_data(self.rt[0:self.fs*3/self.fb], [])
        self.blocks_vector_source_x_0_0.set_data(self.rt[self.fs*12/self.fb:self.fs*15/self.fb], [])
        self.blocks_vector_source_x_0_0_0.set_data(self.rt[self.fs*15/self.fb:self.fs*18/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0.set_data(self.rt[self.fs*18/self.fb:self.fs*21/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0_0.set_data(self.rt[self.fs*21/self.fb:self.fs*24/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data(self.rt[self.fs*24/self.fb:self.fs*27/self.fb], [])
        self.blocks_vector_source_x_0_2.set_data(self.rt[self.fs*9/self.fb:self.fs*12/self.fb], [])
        self.blocks_vector_source_x_0_3.set_data(self.rt[self.fs*6/self.fb:self.fs*9/self.fb], [])
        self.blocks_vector_source_x_0_4.set_data(self.rt[self.fs*3/self.fb:self.fs*6/self.fb], [])
        self.qtgui_time_sink_x_0.set_samp_rate(self.fs)

    def get_fb(self):
        return self.fb

    def set_fb(self, fb):
        self.fb = fb
        self.set_rt(pam11(self.an, self.fb, self.fs, 'sinc', [20, 0]))
        self.blocks_vector_source_x_0.set_data(self.rt[0:self.fs*3/self.fb], [])
        self.blocks_vector_source_x_0_0.set_data(self.rt[self.fs*12/self.fb:self.fs*15/self.fb], [])
        self.blocks_vector_source_x_0_0_0.set_data(self.rt[self.fs*15/self.fb:self.fs*18/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0.set_data(self.rt[self.fs*18/self.fb:self.fs*21/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0_0.set_data(self.rt[self.fs*21/self.fb:self.fs*24/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data(self.rt[self.fs*24/self.fb:self.fs*27/self.fb], [])
        self.blocks_vector_source_x_0_2.set_data(self.rt[self.fs*9/self.fb:self.fs*12/self.fb], [])
        self.blocks_vector_source_x_0_3.set_data(self.rt[self.fs*6/self.fb:self.fs*9/self.fb], [])
        self.blocks_vector_source_x_0_4.set_data(self.rt[self.fs*3/self.fb:self.fs*6/self.fb], [])

    def get_an(self):
        return self.an

    def set_an(self, an):
        self.an = an
        self.set_rt(pam11(self.an, self.fb, self.fs, 'sinc', [20, 0]))

    def get_rt(self):
        return self.rt

    def set_rt(self, rt):
        self.rt = rt
        self.blocks_vector_source_x_0.set_data(self.rt[0:self.fs*3/self.fb], [])
        self.blocks_vector_source_x_0_0.set_data(self.rt[self.fs*12/self.fb:self.fs*15/self.fb], [])
        self.blocks_vector_source_x_0_0_0.set_data(self.rt[self.fs*15/self.fb:self.fs*18/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0.set_data(self.rt[self.fs*18/self.fb:self.fs*21/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0_0.set_data(self.rt[self.fs*21/self.fb:self.fs*24/self.fb], [])
        self.blocks_vector_source_x_0_0_0_0_0_0.set_data(self.rt[self.fs*24/self.fb:self.fs*27/self.fb], [])
        self.blocks_vector_source_x_0_2.set_data(self.rt[self.fs*9/self.fb:self.fs*12/self.fb], [])
        self.blocks_vector_source_x_0_3.set_data(self.rt[self.fs*6/self.fb:self.fs*9/self.fb], [])
        self.blocks_vector_source_x_0_4.set_data(self.rt[self.fs*3/self.fb:self.fs*6/self.fb], [])

    def get_dly(self):
        return self.dly

    def set_dly(self, dly):
        self.dly = dly


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
