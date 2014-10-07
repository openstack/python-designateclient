
import logging

from designateclient.cli import base
from designateclient.v2.blacklists import Blacklist


LOG = logging.getLogger(__name__)


class ListBlacklistsCommand(base.ListCommand):
    """List Blacklists"""

    columns = ['id', 'pattern']

    def execute(self, parsed_args):
        return self.client.blacklists.list()


class GetBlacklistCommand(base.GetCommand):
    """Get Blacklist"""

    def get_parser(self, prog_name):
        parser = super(GetBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Blacklist ID")

        return parser

    def execute(self, parsed_args):
        return self.client.blacklists.get(parsed_args.id)


class CreateBlacklistCommand(base.CreateCommand):
    """Create Blacklist"""

    def get_parser(self, prog_name):
        parser = super(CreateBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('--pattern', help="Blacklist Pattern", required=True)

        return parser

    def execute(self, parsed_args):
        blacklist = Blacklist(
            pattern=parsed_args.pattern,
        )

        return self.client.blacklists.create(blacklist)


class UpdateBlacklistCommand(base.UpdateCommand):
    """Update Blacklist"""

    def get_parser(self, prog_name):
        parser = super(UpdateBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Blacklist ID")
        parser.add_argument('--pattern', help="Blacklist Pattern")

        return parser

    def execute(self, parsed_args):

        newBL = {'id': parsed_args.id}

        if parsed_args.pattern:
            newBL['pattern'] = parsed_args.pattern

#        if parsed_args.description:
#            newBL['description'] = parsed_args.description

        blacklist = {'blacklist': newBL}
        return self.client.blacklists.update(blacklist)


class DeleteBlacklistCommand(base.DeleteCommand):
    """Delete Blacklist"""

    def get_parser(self, prog_name):
        parser = super(DeleteBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Blacklist ID")

        return parser

    def execute(self, parsed_args):
        return self.client.blacklists.delete(parsed_args.id)
