from optparse import OptionParser
from optparse import OptionGroup

def main():

    usage = 'usage: %prog [options] arg1 arg2'
    parser = OptionParser(usage=usage)
    # -file text.txt などと使いたい場合
    parser.add_option('-f', '--file', action='store', type='string',
            dest='filename', help='File name')
    parser.add_option('-n', '--num', action='store', type='int', dest='num')
    # parser.add_option('-v', action='store_true', dest='verbose', default=False)
    parser.set_defaults(verbose=True)
    parser.add_option('-v', action='store_true', dest='verbose')
    parser.add_option('-q', action='store_false', dest='verbose')

    parser.add_option('-r', action='store_const', const='root', dest='user_name')

    parser.add_option('-e', dest='env')

    def is_release(option, opt_str, value, parser):
        if parser.values.env == 'prd':  # production
            raise parser.error("Can't release")
        setattr(parser.values, option.dest, True)

    # python opt_parse.py -e prd --release
    # python opt_parse.py -e dev --release
    parser.add_option('--release', action='callback', callback=is_release, dest='release')


    # python opt_parse.py --help
    group = OptionGroup(parser, 'Dangerous options')
    group.add_option('-g', action='store_true', help='Group option')
    parser.add_option_group(group)

    options, args = parser.parse_args()
    print(options)
    print(options.filename)
    print(args)


if __name__ == '__main__':
    # python opt_parse.py arg1 arg2
    # python opt_parse.py --help
    # python opt_parse.py -f hoge.txt
    # python opt_parse.py hoge pien -f hoge.txt

    # python opt_parse.py hoge pien -f hoge.txt -n 100
    main()
