#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Sudden Ionospheric Disturbance Receiver
# Author: Marcus Leech, Science Radio Laboratories, Inc
# Description: Six channel SID receiver, use with audio I/O
# Generated: Mon Jan  3 23:59:46 2011
##################################################

from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import notchfilt
import sidsuite
import wx

class audioSIDnetRcvr(grc_wxgui.top_block_gui):

	def __init__(self, f4=18.5e3, f3=22.5e3, f2=19.50e3, f1=24.0e3, f5=19.5e3, f6=14.5e3, hz=60, samp_rate=96000, integ=5.0, igain=1, audio_shift=23.0e3, audio_width=6.0e3, synoptic_length=int(100e3), cfn="/dev/null", filename="audioSIDFifo-0", synoptic_ratio=10, ohwname="hw:1,0", hwname="hw:0,0"):
		grc_wxgui.top_block_gui.__init__(self, title="Sudden Ionospheric Disturbance Receiver")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.f4 = f4
		self.f3 = f3
		self.f2 = f2
		self.f1 = f1
		self.f5 = f5
		self.f6 = f6
		self.hz = hz
		self.samp_rate = samp_rate
		self.integ = integ
		self.igain = igain
		self.audio_shift = audio_shift
		self.audio_width = audio_width
		self.synoptic_length = synoptic_length
		self.cfn = cfn
		self.filename = filename
		self.synoptic_ratio = synoptic_ratio
		self.ohwname = ohwname
		self.hwname = hwname

		##################################################
		# Variables
		##################################################
		self.msk_baud = msk_baud = 200
		self.width = width = audio_width
		self.start_freq = start_freq = audio_shift
		self.msk_width = msk_width = (msk_baud*1.5)
		self.integration = integration = integ
		self.chan6_freq = chan6_freq = f6
		self.chan5_freq = chan5_freq = f5
		self.chan4_freq = chan4_freq = f4
		self.chan3_freq = chan3_freq = f3
		self.chan2_freq = chan2_freq = f2
		self.chan1_freq = chan1_freq = f1
		self.sidvars = sidvars = sidsuite.variables(cfn,chan1_freq,chan2_freq,chan3_freq,chan4_freq,chan5_freq,chan6_freq,integration,0,0,igain,width,start_freq)
		self.converter_taps = converter_taps = gr.firdes.low_pass(1.0,samp_rate,width,width/5,gr.firdes.WIN_HAMMING)
		self.channel_taps = channel_taps = gr.firdes.low_pass(1750.0,samp_rate,300,45,gr.firdes.WIN_HAMMING)
		self.cbw = cbw = msk_width

		##################################################
		# Notebooks
		##################################################
		self.MainNotebook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.MainNotebook.AddPage(grc_wxgui.Panel(self.MainNotebook), "Main")
		self.MainNotebook.AddPage(grc_wxgui.Panel(self.MainNotebook), "Spectral")
		self.Add(self.MainNotebook)

		##################################################
		# Controls
		##################################################
		_width_sizer = wx.BoxSizer(wx.VERTICAL)
		self._width_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			sizer=_width_sizer,
			value=self.width,
			callback=self.set_width,
			label="Audio Capture Width",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._width_slider = forms.slider(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			sizer=_width_sizer,
			value=self.width,
			callback=self.set_width,
			minimum=300,
			maximum=14.3e3,
			num_steps=140,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.MainNotebook.GetPage(0).Add(_width_sizer)
		_start_freq_sizer = wx.BoxSizer(wx.VERTICAL)
		self._start_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			sizer=_start_freq_sizer,
			value=self.start_freq,
			callback=self.set_start_freq,
			label="Audio Start Freq",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._start_freq_slider = forms.slider(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			sizer=_start_freq_sizer,
			value=self.start_freq,
			callback=self.set_start_freq,
			minimum=100.0,
			maximum=45.0e3,
			num_steps=800,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.MainNotebook.GetPage(0).Add(_start_freq_sizer)
		_integration_sizer = wx.BoxSizer(wx.VERTICAL)
		self._integration_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			sizer=_integration_sizer,
			value=self.integration,
			callback=self.set_integration,
			label="Post Detector Integration",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._integration_slider = forms.slider(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			sizer=_integration_sizer,
			value=self.integration,
			callback=self.set_integration,
			minimum=1,
			maximum=101,
			num_steps=200,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.MainNotebook.GetPage(0).Add(_integration_sizer)
		self._chan6_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			value=self.chan6_freq,
			callback=self.set_chan6_freq,
			label="Channel 6 Frequency",
			converter=forms.float_converter(),
		)
		self.MainNotebook.GetPage(0).Add(self._chan6_freq_text_box)
		self._chan5_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			value=self.chan5_freq,
			callback=self.set_chan5_freq,
			label="Channel 5 Frequency",
			converter=forms.float_converter(),
		)
		self.MainNotebook.GetPage(0).Add(self._chan5_freq_text_box)
		self._chan4_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			value=self.chan4_freq,
			callback=self.set_chan4_freq,
			label="Channel 4 Frequency",
			converter=forms.float_converter(),
		)
		self.MainNotebook.GetPage(0).Add(self._chan4_freq_text_box)
		self._chan3_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			value=self.chan3_freq,
			callback=self.set_chan3_freq,
			label="Channel 3 Frequency",
			converter=forms.float_converter(),
		)
		self.MainNotebook.GetPage(0).Add(self._chan3_freq_text_box)
		self._chan2_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			value=self.chan2_freq,
			callback=self.set_chan2_freq,
			label="Channel 2 Frequency",
			converter=forms.float_converter(),
		)
		self.MainNotebook.GetPage(0).Add(self._chan2_freq_text_box)
		self._chan1_freq_text_box = forms.text_box(
			parent=self.MainNotebook.GetPage(0).GetWin(),
			value=self.chan1_freq,
			callback=self.set_chan1_freq,
			label="Channel 1 Frequency",
			converter=forms.float_converter(),
		)
		self.MainNotebook.GetPage(0).Add(self._chan1_freq_text_box)

		##################################################
		# Blocks
		##################################################
		self.MyScopeSink = scopesink2.scope_sink_f(
			self.MainNotebook.GetPage(0).GetWin(),
			title="Rx Channels RMS Power",
			sample_rate=2,
			v_scale=10,
			v_offset=250,
			t_scale=450.0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=6,
			trig_mode=gr.gr_TRIG_MODE_STRIPCHART,
			y_axis_label="Detected Power",
			size=((700,500)),
		)
		self.MainNotebook.GetPage(0).Add(self.MyScopeSink.win)
		self.audio_sink_0 = audio.sink(int(samp_rate/2), ohwname, True)
		self.audio_source_0 = audio.source(samp_rate, hwname, True)
		self.gr_agc2_xx_0 = gr.agc2_ff(1e-4, 3e-5, 0.75, 0.75, 0.75)
		self.gr_complex_to_mag_0 = gr.complex_to_mag(1)
		self.gr_complex_to_mag_0_0 = gr.complex_to_mag(1)
		self.gr_complex_to_mag_0_0_0 = gr.complex_to_mag(1)
		self.gr_complex_to_mag_0_0_0_0 = gr.complex_to_mag(1)
		self.gr_complex_to_mag_0_0_0_0_0 = gr.complex_to_mag(1)
		self.gr_complex_to_mag_0_0_0_0_0_0 = gr.complex_to_mag(1)
		self.gr_complex_to_real_0 = gr.complex_to_real(1)
		self.gr_complex_to_real_1 = gr.complex_to_real(1)
		self.gr_complex_to_real_2 = gr.complex_to_real(1)
		self.gr_fft_filter_xxx_0 = gr.fft_filter_ccc(1, (notchfilt.notch_taps(samp_rate,hz,(samp_rate/2)/hz)))
		self.gr_file_sink_1_0 = gr.file_sink(gr.sizeof_float*1, "sid_ch1.dat")
		self.gr_file_sink_1_0.set_unbuffered(True)
		self.gr_file_sink_1_0_0 = gr.file_sink(gr.sizeof_float*1, "sid_ch2.dat")
		self.gr_file_sink_1_0_0.set_unbuffered(True)
		self.gr_file_sink_1_0_0_0 = gr.file_sink(gr.sizeof_float*1, "sid_ch3.dat")
		self.gr_file_sink_1_0_0_0.set_unbuffered(True)
		self.gr_file_sink_1_0_0_0_0 = gr.file_sink(gr.sizeof_float*1, "sid_ch4.dat")
		self.gr_file_sink_1_0_0_0_0.set_unbuffered(True)
		self.gr_file_sink_1_0_0_0_0_0 = gr.file_sink(gr.sizeof_float*1, "sid_ch5.dat")
		self.gr_file_sink_1_0_0_0_0_0.set_unbuffered(True)
		self.gr_file_sink_1_0_0_0_0_0_0 = gr.file_sink(gr.sizeof_float*1, "sid_ch6.dat")
		self.gr_file_sink_1_0_0_0_0_0_0.set_unbuffered(True)
		self.gr_file_sink_4 = gr.file_sink(gr.sizeof_gr_complex*synoptic_length, "synoptic_output")
		self.gr_file_sink_4.set_unbuffered(False)
		self.gr_freq_xlating_fir_filter_xxx_0 = gr.freq_xlating_fir_filter_ccc(2, (converter_taps), -1*(start_freq), samp_rate)
		self.gr_goertzel_fc_0 = gr.goertzel_fc(samp_rate, int(samp_rate/200), chan1_freq)
		self.gr_goertzel_fc_1 = gr.goertzel_fc(samp_rate, int(samp_rate/200), chan2_freq)
		self.gr_goertzel_fc_1_0 = gr.goertzel_fc(samp_rate, int(samp_rate/200), chan3_freq)
		self.gr_goertzel_fc_1_0_0 = gr.goertzel_fc(samp_rate, int(samp_rate/200), chan4_freq)
		self.gr_goertzel_fc_1_0_0_0 = gr.goertzel_fc(samp_rate, int(samp_rate/200), chan5_freq)
		self.gr_goertzel_fc_1_0_0_0_0 = gr.goertzel_fc(samp_rate, int(samp_rate/200), chan6_freq)
		self.gr_hilbert_fc_0 = gr.hilbert_fc(32)
		self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_float*1, 20)
		self.gr_keep_one_in_n_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 20)
		self.gr_keep_one_in_n_0_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 20)
		self.gr_keep_one_in_n_0_0_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 20)
		self.gr_keep_one_in_n_0_0_0_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 20)
		self.gr_keep_one_in_n_0_0_0_0_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 20)
		self.gr_keep_one_in_n_0_0_0_0_1 = gr.keep_one_in_n(gr.sizeof_float*1, 100)
		self.gr_keep_one_in_n_0_0_0_0_1_0 = gr.keep_one_in_n(gr.sizeof_float*1, 100)
		self.gr_keep_one_in_n_0_0_0_0_1_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 100)
		self.gr_keep_one_in_n_0_0_0_0_1_0_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 100)
		self.gr_keep_one_in_n_0_0_0_0_1_0_0_0_0 = gr.keep_one_in_n(gr.sizeof_float*1, 100)
		self.gr_keep_one_in_n_0_0_0_0_1_0_0_0_1 = gr.keep_one_in_n(gr.sizeof_float*1, 100)
		self.gr_keep_one_in_n_1 = gr.keep_one_in_n(gr.sizeof_gr_complex*synoptic_length, synoptic_ratio)
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vff((igain, ))
		self.gr_multiply_const_vxx_1 = gr.multiply_const_vff((0.125, ))
		self.gr_multiply_const_vxx_2 = gr.multiply_const_vcc((100, ))
		self.gr_single_pole_iir_filter_xx_0 = gr.single_pole_iir_filter_ff(1.0/(integration*200), 1)
		self.gr_single_pole_iir_filter_xx_0_0 = gr.single_pole_iir_filter_ff(1.0/(integration*200), 1)
		self.gr_single_pole_iir_filter_xx_0_0_0 = gr.single_pole_iir_filter_ff(1.0/(integration*200), 1)
		self.gr_single_pole_iir_filter_xx_0_0_0_0 = gr.single_pole_iir_filter_ff(1.0/(integration*200), 1)
		self.gr_single_pole_iir_filter_xx_0_0_0_0_0 = gr.single_pole_iir_filter_ff(1.0/(integration*200), 1)
		self.gr_single_pole_iir_filter_xx_0_0_0_0_0_0 = gr.single_pole_iir_filter_ff(1.0/(integration*200), 1)
		self.gr_stream_to_vector_0 = gr.stream_to_vector(gr.sizeof_gr_complex*1, synoptic_length)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
			self.MainNotebook.GetPage(1).GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=50,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=2048,
			fft_rate=5,
			average=True,
			avg_alpha=0.03,
			title="Instantaneous Spectrum",
			peak_hold=False,
			size=((800,400)),
		)
		self.MainNotebook.GetPage(1).Add(self.wxgui_fftsink2_0.win)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_f(
			self.MainNotebook.GetPage(1).GetWin(),
			baseband_freq=0,
			dynamic_range=50,
			ref_level=45,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=2048,
			fft_rate=3,
			average=True,
			avg_alpha=0.03,
			title="Spectrogram",
			size=((800,400)),
		)
		self.MainNotebook.GetPage(1).Add(self.wxgui_waterfallsink2_0.win)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_stream_to_vector_0, 0), (self.gr_keep_one_in_n_1, 0))
		self.connect((self.gr_keep_one_in_n_1, 0), (self.gr_file_sink_4, 0))
		self.connect((self.gr_keep_one_in_n_0_0, 0), (self.gr_file_sink_1_0_0, 0))
		self.connect((self.gr_hilbert_fc_0, 0), (self.gr_fft_filter_xxx_0, 0))
		self.connect((self.gr_fft_filter_xxx_0, 0), (self.gr_stream_to_vector_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.gr_complex_to_real_0, 0))
		self.connect((self.gr_fft_filter_xxx_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0, 0))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_0, 0), (self.gr_file_sink_1_0_0_0_0_0, 0))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_0_0, 0), (self.gr_file_sink_1_0_0_0_0_0_0, 0))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_1, 0), (self.MyScopeSink, 0))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_1_0, 0), (self.MyScopeSink, 1))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_1_0_0, 0), (self.MyScopeSink, 2))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_1_0_0_0, 0), (self.MyScopeSink, 3))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_1_0_0_0_0, 0), (self.MyScopeSink, 4))
		self.connect((self.gr_keep_one_in_n_0_0_0_0_1_0_0_0_1, 0), (self.MyScopeSink, 5))
		self.connect((self.gr_complex_to_real_1, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.gr_complex_to_real_1, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.gr_fft_filter_xxx_0, 0), (self.gr_complex_to_real_1, 0))
		self.connect((self.audio_source_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_hilbert_fc_0, 0))
		self.connect((self.gr_complex_to_real_0, 0), (self.gr_agc2_xx_0, 0))
		self.connect((self.gr_agc2_xx_0, 0), (self.gr_multiply_const_vxx_1, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0, 0), (self.gr_keep_one_in_n_0_0_0_0_1, 0))
		self.connect((self.gr_keep_one_in_n_0_0_0_0, 0), (self.gr_file_sink_1_0_0_0_0, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.gr_file_sink_1_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0, 0), (self.gr_keep_one_in_n_0, 0))
		self.connect((self.gr_goertzel_fc_0, 0), (self.gr_complex_to_mag_0, 0))
		self.connect((self.gr_complex_to_mag_0, 0), (self.gr_single_pole_iir_filter_xx_0, 0))
		self.connect((self.gr_complex_to_real_2, 0), (self.gr_goertzel_fc_0, 0))
		self.connect((self.gr_complex_to_real_2, 0), (self.gr_goertzel_fc_1, 0))
		self.connect((self.gr_goertzel_fc_1, 0), (self.gr_complex_to_mag_0_0, 0))
		self.connect((self.gr_complex_to_mag_0_0, 0), (self.gr_single_pole_iir_filter_xx_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0, 0), (self.gr_keep_one_in_n_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_1_0, 0))
		self.connect((self.gr_complex_to_real_2, 0), (self.gr_goertzel_fc_1_0, 0))
		self.connect((self.gr_goertzel_fc_1_0, 0), (self.gr_complex_to_mag_0_0_0, 0))
		self.connect((self.gr_complex_to_mag_0_0_0, 0), (self.gr_single_pole_iir_filter_xx_0_0_0, 0))
		self.connect((self.gr_keep_one_in_n_0_0_0, 0), (self.gr_file_sink_1_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_1_0_0, 0))
		self.connect((self.gr_complex_to_real_2, 0), (self.gr_goertzel_fc_1_0_0, 0))
		self.connect((self.gr_goertzel_fc_1_0_0, 0), (self.gr_complex_to_mag_0_0_0_0, 0))
		self.connect((self.gr_complex_to_mag_0_0_0_0, 0), (self.gr_single_pole_iir_filter_xx_0_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_1_0_0_0, 0))
		self.connect((self.gr_complex_to_real_2, 0), (self.gr_goertzel_fc_1_0_0_0, 0))
		self.connect((self.gr_complex_to_real_2, 0), (self.gr_goertzel_fc_1_0_0_0_0, 0))
		self.connect((self.gr_goertzel_fc_1_0_0_0, 0), (self.gr_complex_to_mag_0_0_0_0_0, 0))
		self.connect((self.gr_goertzel_fc_1_0_0_0_0, 0), (self.gr_complex_to_mag_0_0_0_0_0_0, 0))
		self.connect((self.gr_complex_to_mag_0_0_0_0_0, 0), (self.gr_single_pole_iir_filter_xx_0_0_0_0_0, 0))
		self.connect((self.gr_complex_to_mag_0_0_0_0_0_0, 0), (self.gr_single_pole_iir_filter_xx_0_0_0_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_1_0_0_0_1, 0))
		self.connect((self.gr_fft_filter_xxx_0, 0), (self.gr_multiply_const_vxx_2, 0))
		self.connect((self.gr_multiply_const_vxx_2, 0), (self.gr_complex_to_real_2, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_0, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_0_0_0_0_0, 0), (self.gr_keep_one_in_n_0_0_0_0_1_0_0_0_0, 0))

	def set_f4(self, f4):
		self.f4 = f4
		self.set_chan4_freq(self.f4)

	def set_f3(self, f3):
		self.f3 = f3
		self.set_chan3_freq(self.f3)

	def set_f2(self, f2):
		self.f2 = f2
		self.set_chan2_freq(self.f2)

	def set_f1(self, f1):
		self.f1 = f1
		self.set_chan1_freq(self.f1)

	def set_f5(self, f5):
		self.f5 = f5
		self.set_chan5_freq(self.f5)

	def set_f6(self, f6):
		self.f6 = f6
		self.set_chan6_freq(self.f6)

	def set_hz(self, hz):
		self.hz = hz
		self.gr_fft_filter_xxx_0.set_taps((notchfilt.notch_taps(self.samp_rate,self.hz,(self.samp_rate/2)/self.hz)))

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_converter_taps(gr.firdes.low_pass(1.0,self.samp_rate,self.width,self.width/5,gr.firdes.WIN_HAMMING))
		self.set_channel_taps(gr.firdes.low_pass(1750.0,self.samp_rate,300,45,gr.firdes.WIN_HAMMING))
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
		self.gr_goertzel_fc_0.set_rate(self.samp_rate)
		self.gr_goertzel_fc_1_0.set_rate(self.samp_rate)
		self.gr_goertzel_fc_1.set_rate(self.samp_rate)
		self.gr_goertzel_fc_1_0_0_0.set_rate(self.samp_rate)
		self.gr_fft_filter_xxx_0.set_taps((notchfilt.notch_taps(self.samp_rate,self.hz,(self.samp_rate/2)/self.hz)))
		self.gr_goertzel_fc_1_0_0_0_0.set_rate(self.samp_rate)
		self.gr_goertzel_fc_1_0_0.set_rate(self.samp_rate)

	def set_integ(self, integ):
		self.integ = integ
		self.set_integration(self.integ)

	def set_igain(self, igain):
		self.igain = igain
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self.gr_multiply_const_vxx_0.set_k((self.igain, ))

	def set_audio_shift(self, audio_shift):
		self.audio_shift = audio_shift
		self.set_start_freq(self.audio_shift)

	def set_audio_width(self, audio_width):
		self.audio_width = audio_width
		self.set_width(self.audio_width)

	def set_synoptic_length(self, synoptic_length):
		self.synoptic_length = synoptic_length

	def set_cfn(self, cfn):
		self.cfn = cfn
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))

	def set_filename(self, filename):
		self.filename = filename

	def set_synoptic_ratio(self, synoptic_ratio):
		self.synoptic_ratio = synoptic_ratio
		self.gr_keep_one_in_n_1.set_n(self.synoptic_ratio)

	def set_ohwname(self, ohwname):
		self.ohwname = ohwname

	def set_hwname(self, hwname):
		self.hwname = hwname

	def set_msk_baud(self, msk_baud):
		self.msk_baud = msk_baud
		self.set_msk_width((self.msk_baud*1.5))

	def set_width(self, width):
		self.width = width
		self.set_converter_taps(gr.firdes.low_pass(1.0,self.samp_rate,self.width,self.width/5,gr.firdes.WIN_HAMMING))
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._width_slider.set_value(self.width)
		self._width_text_box.set_value(self.width)

	def set_start_freq(self, start_freq):
		self.start_freq = start_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self.gr_freq_xlating_fir_filter_xxx_0.set_center_freq(-1*(self.start_freq))
		self._start_freq_slider.set_value(self.start_freq)
		self._start_freq_text_box.set_value(self.start_freq)

	def set_msk_width(self, msk_width):
		self.msk_width = msk_width
		self.set_cbw(self.msk_width)

	def set_integration(self, integration):
		self.integration = integration
		self._integration_slider.set_value(self.integration)
		self._integration_text_box.set_value(self.integration)
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self.gr_single_pole_iir_filter_xx_0.set_taps(1.0/(self.integration*200))
		self.gr_single_pole_iir_filter_xx_0_0.set_taps(1.0/(self.integration*200))
		self.gr_single_pole_iir_filter_xx_0_0_0.set_taps(1.0/(self.integration*200))
		self.gr_single_pole_iir_filter_xx_0_0_0_0.set_taps(1.0/(self.integration*200))
		self.gr_single_pole_iir_filter_xx_0_0_0_0_0_0.set_taps(1.0/(self.integration*200))
		self.gr_single_pole_iir_filter_xx_0_0_0_0_0.set_taps(1.0/(self.integration*200))

	def set_chan6_freq(self, chan6_freq):
		self.chan6_freq = chan6_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._chan6_freq_text_box.set_value(self.chan6_freq)
		self.gr_goertzel_fc_1_0_0_0_0.set_freq(self.chan6_freq)

	def set_chan5_freq(self, chan5_freq):
		self.chan5_freq = chan5_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._chan5_freq_text_box.set_value(self.chan5_freq)
		self.gr_goertzel_fc_1_0_0_0.set_freq(self.chan5_freq)

	def set_chan4_freq(self, chan4_freq):
		self.chan4_freq = chan4_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._chan4_freq_text_box.set_value(self.chan4_freq)
		self.gr_goertzel_fc_1_0_0.set_freq(self.chan4_freq)

	def set_chan3_freq(self, chan3_freq):
		self.chan3_freq = chan3_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._chan3_freq_text_box.set_value(self.chan3_freq)
		self.gr_goertzel_fc_1_0.set_freq(self.chan3_freq)

	def set_chan2_freq(self, chan2_freq):
		self.chan2_freq = chan2_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._chan2_freq_text_box.set_value(self.chan2_freq)
		self.gr_goertzel_fc_1.set_freq(self.chan2_freq)

	def set_chan1_freq(self, chan1_freq):
		self.chan1_freq = chan1_freq
		self.set_sidvars(sidsuite.variables(self.cfn,self.chan1_freq,self.chan2_freq,self.chan3_freq,self.chan4_freq,self.chan5_freq,self.chan6_freq,self.integration,0,0,self.igain,self.width,self.start_freq))
		self._chan1_freq_text_box.set_value(self.chan1_freq)
		self.gr_goertzel_fc_0.set_freq(self.chan1_freq)

	def set_sidvars(self, sidvars):
		self.sidvars = sidvars

	def set_converter_taps(self, converter_taps):
		self.converter_taps = converter_taps
		self.gr_freq_xlating_fir_filter_xxx_0.set_taps((self.converter_taps))

	def set_channel_taps(self, channel_taps):
		self.channel_taps = channel_taps

	def set_cbw(self, cbw):
		self.cbw = cbw

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--f4", dest="f4", type="eng_float", default=eng_notation.num_to_str(18.5e3),
		help="Set f4 [default=%default]")
	parser.add_option("", "--f3", dest="f3", type="eng_float", default=eng_notation.num_to_str(22.5e3),
		help="Set f3 [default=%default]")
	parser.add_option("", "--f2", dest="f2", type="eng_float", default=eng_notation.num_to_str(19.50e3),
		help="Set f2 [default=%default]")
	parser.add_option("", "--f1", dest="f1", type="eng_float", default=eng_notation.num_to_str(24.0e3),
		help="Set f1 [default=%default]")
	parser.add_option("", "--f5", dest="f5", type="eng_float", default=eng_notation.num_to_str(19.5e3),
		help="Set f5 [default=%default]")
	parser.add_option("", "--f6", dest="f6", type="eng_float", default=eng_notation.num_to_str(14.5e3),
		help="Set f6 [default=%default]")
	parser.add_option("", "--hz", dest="hz", type="intx", default=60,
		help="Set hz [default=%default]")
	parser.add_option("", "--samp-rate", dest="samp_rate", type="intx", default=96000,
		help="Set samp_rate [default=%default]")
	parser.add_option("", "--integ", dest="integ", type="eng_float", default=eng_notation.num_to_str(5.0),
		help="Set integ [default=%default]")
	parser.add_option("", "--igain", dest="igain", type="eng_float", default=eng_notation.num_to_str(1),
		help="Set igain [default=%default]")
	parser.add_option("", "--audio-shift", dest="audio_shift", type="eng_float", default=eng_notation.num_to_str(23.0e3),
		help="Set audio_shift [default=%default]")
	parser.add_option("", "--audio-width", dest="audio_width", type="eng_float", default=eng_notation.num_to_str(6.0e3),
		help="Set audio_width [default=%default]")
	parser.add_option("", "--synoptic-length", dest="synoptic_length", type="intx", default=int(100e3),
		help="Set synoptic_length [default=%default]")
	parser.add_option("", "--cfn", dest="cfn", type="string", default="/dev/null",
		help="Set cfn [default=%default]")
	parser.add_option("", "--filename", dest="filename", type="string", default="audioSIDFifo-0",
		help="Set filename [default=%default]")
	parser.add_option("", "--synoptic-ratio", dest="synoptic_ratio", type="intx", default=10,
		help="Set synoptic_ratio [default=%default]")
	parser.add_option("", "--ohwname", dest="ohwname", type="string", default="hw:1,0",
		help="Set ohwname [default=%default]")
	parser.add_option("", "--hwname", dest="hwname", type="string", default="hw:0,0",
		help="Set hwname [default=%default]")
	(options, args) = parser.parse_args()
	tb = audioSIDnetRcvr(f4=options.f4, f3=options.f3, f2=options.f2, f1=options.f1, f5=options.f5, f6=options.f6, hz=options.hz, samp_rate=options.samp_rate, integ=options.integ, igain=options.igain, audio_shift=options.audio_shift, audio_width=options.audio_width, synoptic_length=options.synoptic_length, cfn=options.cfn, filename=options.filename, synoptic_ratio=options.synoptic_ratio, ohwname=options.ohwname, hwname=options.hwname)
	tb.Run(True)

