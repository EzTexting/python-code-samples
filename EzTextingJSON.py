from EzTextingBase import EzTextingBase, Contact, Group, EzTextingError
import simplejson as json

class EzTextingJSON(EzTextingBase):
    def __init__(self, base_url, login, password):
        EzTextingBase.__init__(self, base_url, login, password)

    def _get(self,url, **params):
        params['format'] = 'json'
        return EzTextingBase._get(self,url, **params)

    def _post(self,url, **params):
        return EzTextingBase._post(self,url + (url.find('?')==-1 and '?' or '&') + 'format=json', **params)

    def _parse_contacts_result(self, content):
        pyobj = json.loads(content)
        res = []
        for entry in pyobj['Response']['Entries']:
             contact = Contact(str(entry['PhoneNumber']), str(entry['FirstName']), str(entry['LastName']), str(entry['Email']), str(entry['Note']), entry['Groups'], str(entry['Source']), str(entry['CreatedAt']), str(entry['ID']))
             res.append(contact)
        return res

    def _parse_contact_result(self, content):
        pyobj = json.loads(content)
        entry = pyobj['Response']['Entry']
        return Contact(str(entry['PhoneNumber']), str(entry['FirstName']), str(entry['LastName']), str(entry['Email']), str(entry['Note']), entry['Groups'], str(entry['Source']), str(entry['CreatedAt']), str(entry['ID']))

    def _parse_group_result(self, content):
        pyobj = json.loads(content)
        entry = pyobj['Response']['Entry']
        return self._build_group(entry)

    def _parse_groups_result(self, content):
        pyobj = json.loads(content)
        res = []
        for entry in pyobj['Response']['Entries']:
             res.append( self._build_group(entry) )
        return res

    def _build_group(self, entry):
        return Group(str(entry['Name']), str(entry['Note']), entry['ContactCount'], str(entry['ID']))


    def _parse_errors(self, errcode, content):
        pyobj = json.loads(content)
        return EzTextingError(errcode, pyobj['Response']['Errors'])