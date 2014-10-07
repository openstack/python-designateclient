import json

from designateclient import utils
from designateclient.v1.base import CrudController
from designateclient import warlock


Blacklist = warlock.model_factory(utils.load_schema('v2', 'blacklist'))


class BlacklistsController(CrudController):
    def list(self):
        """
        Retrieve a list of blacklists

        :returns: A list of :class:`Blacklist`s
        """
        response = self.client.get('/blacklists')

        return [Blacklist(i) for i in response.json()['blacklists']]

    def get(self, blacklist_id):
        """
        Retrieve a blacklist

        :param blacklist_id: Blacklist Identifier
        :returns: :class:`Blacklist`
        """
        response = self.client.get('/blacklists/%s' % blacklist_id)

        return Blacklist(response.json())

    def create(self, blacklist):
        """
        Create a blacklist
        """
        blacklist = {"blacklist": utils.convert(blacklist)}
        response = self.client.post('/blacklists', 
                                   data=json.dumps(blacklist))
        return Blacklist(response.json())

    def update(self, blacklist):
        """
        Update a blacklist
        """
        id = blacklist['blacklist']['id']
        del blacklist['blacklist']['id']
        response = self.client.patch('/blacklists/%s' % id,
                                   data=json.dumps(blacklist))

        return Blacklist(response.json())

    def delete(self, blacklist):
        """
        Delete a blacklist

        :param blacklist: A :class:`Blacklist`, or Blacklist Identifier to delete
        """
        if isinstance(blacklist, Blacklist):
            self.client.delete('/blacklists/%s' % blacklist.id)
        else:
            self.client.delete('/blacklists/%s' % blacklist)

