#!/usr/bin/env python3
# encoding:utf-8


from keysec.parsers.top import top_parser


class ARGS:
    ALGORITHM = None
    BITS = None
    COMMENT = None
    CONVERT = None
    EDIT = None
    FORMAT = None
    GENERATE = None
    IN = None
    INFO = None
    NOPASS = None
    OUT = None
    PASSWORD = None
    PRIVATE = None
    PUBLIC = None


def parse_args():
    args = vars(top_parser.parse_args())
    ARGS.ALGORITHM = args.get('algorithm')
    ARGS.BITS = args.get('bits')
    ARGS.COMMENT = args.get('comment')
    ARGS.FORMAT = args.get('format')
    ARGS.IN = args.get('infile').read() if args.get('infile') else None
    ARGS.NOPASS = args.get('nopass')
    ARGS.OUT = args.get('outfile')
    ARGS.PASSWORD = args.get('pass')
    ARGS.CONVERT = args.get('opt') == 'conv'
    ARGS.EDIT = args.get('opt') == 'edit'
    ARGS.GENERATE = args.get('opt') == 'gen'
    ARGS.INFO = args.get('opt') == 'info'
    ARGS.PRIVATE = args.get('gen') == 'priv'
    ARGS.PUBLIC = args.get('gen') == 'pub'
    return args
