
import argparse
import sys

class SubArgumentParser:
    """
    Example usage:
    parser = SubArgumentParser()

    parser.add_subcommand('fetch', help='git fetch',
                          callable=git_func)
    # parser.fetch is an argparse.ArgumentParser for everything after subcommand.
    parser.fetch.add_argument('arg1', )
    parser.fetch.add_argument('arg2', )

    parser.add_subcommand('pull', help='git pull')
    parser.pull.add_argument('arg', )

    # Returns the subcommand (as text) and the parsed args for the rest of the args
    subcommand, args = parser.parse_args()

    # Can also directly call the callables passed with the parser.__dict__ as kwargs.
    parser.call()
    """

    def __init__(self):
        self.subcommands = {}

    def _build_subcommand_parser(self):
        usage_str = "Sub-commands:\n\n"
        for k in self.subcommands.keys():
            usage_str += "{:20s}{}\n".format(k, self.subcommands[k]['help'])
        usage_str += '\n'

        self.subcommand = argparse.ArgumentParser(usage=usage_str)
        self.subcommand.add_argument('subcommand')

    def add_subcommand(self, subcommand, help=None, callable=None):
        self.subcommands[subcommand] = {'parser': argparse.ArgumentParser(),
                                        'help': help,
                                        'callable': callable}
        self._build_subcommand_parser()

    def __getattr__(self, item):
        return self.subcommands[item]['parser']

    def parse_args(self):
        subcmd = self.subcommand.parse_args(sys.argv[1:2])
        return subcmd.subcommand, self.subcommands[subcmd.subcommand]['parser'].parse_args(sys.argv[2:])

    def call(self):
        subcmd, args = self.parse_args()
        self.subcommands[subcmd]['callable'](**args.__dict__)
