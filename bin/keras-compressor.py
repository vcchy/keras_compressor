#!/usr/bin/env python
import argparse
import logging

import keras
from keras.models import load_model
from keras.utils.layer_utils import count_total_params

from keras_compressor.compressor import compress


def gen_argparser():
    parser = argparse.ArgumentParser(description='compress keras model')
    parser.add_argument('model', type=str, metavar='model.h5',
                        help='target model, whose loss is specified by `model.compile()`.')
    parser.add_argument('compressed', type=str, metavar='compressed.h5',
                        help='compressed model path')
    parser.add_argument('--error', type=float, default=0.1, metavar='0.1',
                        help='layer-wise acceptable error. '
                             'If this value is larger, compressed model will be '
                             'less accurate and achieve better compression rate. '
                             'Default: 0.1')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        help='log level. Default: INFO')
    return parser


def main():
    parser = gen_argparser()
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level))

    model = load_model(args.model)  # type: keras.models.Model
    total_params_before = sum(count_total_params(model.layers))
    model = compress(model, acceptable_error=args.error)
    total_params_after = sum(count_total_params(model.layers))
    model.save(args.compressed)
    print('\n'.join((
        'Compressed model',
        '    before #params {:>20,d}',
        '    after  #params {:>20,d} ({:.2%})',
    )).format(
        total_params_before, total_params_after, 1 - float(total_params_after) / total_params_before,
    ))


if __name__ == '__main__':
    main()
