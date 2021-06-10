#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulator
# GNU Radio version: 3.8.2.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time


class modulator(gr.top_block):

    def __init__(self, am_symbols='0,0,0,0,1,1,1,1', freq=7040100, wspr_symbols='0,1,2,3,0,1,2,3'):
        gr.top_block.__init__(self, "Modulator")

        ##################################################
        # Parameters
        ##################################################
        self.am_symbols = am_symbols
        self.freq = freq
        self.wspr_symbols = wspr_symbols

        ##################################################
        # Variables
        ##################################################
        self.tone_spacing = tone_spacing = 12000/8192
        self.symbol_duration = symbol_duration = 8192/12000
        self.samp_rate = samp_rate = 25e3
        self.pi = pi = 3.14159265358979323846
        self.dev_samp_rate = dev_samp_rate = 2.5e6

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_0_0 = filter.interp_fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                1/symbol_duration,
                0.35,
                int(samp_rate/symbol_duration/3)))
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                1/symbol_duration,
                0.35,
                int(samp_rate/symbol_duration/3)))
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(dev_samp_rate),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(dev_samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(1e3, 0)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f([0.7+0.3*int(x) for x in am_symbols.split(',')], False, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_f([float(x) for x in wspr_symbols.split(',')], False, 1, [])
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_float*1, int(symbol_duration*samp_rate))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, int(symbol_duration*samp_rate))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*pi*tone_spacing/samp_rate)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))


    def get_am_symbols(self):
        return self.am_symbols

    def set_am_symbols(self, am_symbols):
        self.am_symbols = am_symbols

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_wspr_symbols(self):
        return self.wspr_symbols

    def set_wspr_symbols(self, wspr_symbols):
        self.wspr_symbols = wspr_symbols

    def get_tone_spacing(self):
        return self.tone_spacing

    def set_tone_spacing(self, tone_spacing):
        self.tone_spacing = tone_spacing
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*self.pi*self.tone_spacing/self.samp_rate)

    def get_symbol_duration(self):
        return self.symbol_duration

    def set_symbol_duration(self, symbol_duration):
        self.symbol_duration = symbol_duration
        self.blocks_repeat_0.set_interpolation(int(self.symbol_duration*self.samp_rate))
        self.blocks_repeat_0_0.set_interpolation(int(self.symbol_duration*self.samp_rate))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 1/self.symbol_duration, 0.35, int(self.samp_rate/self.symbol_duration/3)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 1/self.symbol_duration, 0.35, int(self.samp_rate/self.symbol_duration/3)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*self.pi*self.tone_spacing/self.samp_rate)
        self.blocks_repeat_0.set_interpolation(int(self.symbol_duration*self.samp_rate))
        self.blocks_repeat_0_0.set_interpolation(int(self.symbol_duration*self.samp_rate))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 1/self.symbol_duration, 0.35, int(self.samp_rate/self.symbol_duration/3)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 1/self.symbol_duration, 0.35, int(self.samp_rate/self.symbol_duration/3)))

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*self.pi*self.tone_spacing/self.samp_rate)

    def get_dev_samp_rate(self):
        return self.dev_samp_rate

    def set_dev_samp_rate(self, dev_samp_rate):
        self.dev_samp_rate = dev_samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.dev_samp_rate)




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--am-symbols", dest="am_symbols", type=str, default='0,0,0,0,1,1,1,1',
        help="Set 0,0,0,0,1,1,1,1 [default=%(default)r]")
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default="7.0401M",
        help="Set freq [default=%(default)r]")
    parser.add_argument(
        "--wspr-symbols", dest="wspr_symbols", type=str, default='0,1,2,3,0,1,2,3',
        help="Set 0,1,2,3,0,1,2,3 [default=%(default)r]")
    return parser


def main(top_block_cls=modulator, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(am_symbols=options.am_symbols, freq=options.freq, wspr_symbols=options.wspr_symbols)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
