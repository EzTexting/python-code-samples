import urllib, urllib2

class EzTextingBase:
    def __init__(self, base_url, login, password):
        self.base_url = base_url
        self.login = login
        self.password = password

    def _get(self,url, **params):
        #remove empty params
        keys = params.keys()
        for k in keys: 
            if params[k] is None: del params[k]
        params['User'] = self.login
        params['Password'] = self.password
        #print params
        str_params = urllib.urlencode(params)
        try:
            resp = urllib2.urlopen(self.base_url+ url + '?' + str_params)
            return resp.read()
        except urllib2.HTTPError, error:
            raise self._parse_errors(error.code, error.read())

    def _post(self,url, **params):
        #remove empty params
        keys = params.keys()
        for k in keys: 
            if params[k] is None: del params[k]
            elif getattr(params[k], '__iter__', False):
                for i, item in enumerate(params[k]):
                    params[k+'['+str(i)+']']=item
                del params[k]
        params['User'] = self.login
        params['Password'] = self.password
        #print params
        str_params = urllib.urlencode(params)
        try:
            resp = urllib2.urlopen(self.base_url+ url, str_params)
            return resp.read()
        except urllib2.HTTPError, error:
            if error.code == 201: #actually, this is success
                return error.read()
            elif error.code == 204: #actually, this is success
                return error.read()
            else:
                raise self._parse_errors(error.code, error.read())

    def _delete(self,url, **params):
        self._post(url+'?_method=DELETE', **params)

    def get_all_contacts(self, query=None, source=None, optout=None, group=None, sortBy=None, sortDir=None, itemsPerPage=None, page=None):
        """Get a list of contacts stored in your Ez Texting contact list.

        Filters
        query (Optional) Search contacts by first name / last name / phone number
        source (Optional) Source of contacts. Available values: 'Unknown', 'Manually Added', 'Upload', 'Web Widget', 'API', 'Keyword'
        optout (Optional) Opted out / opted in contacts. Available values: true, false.
        group (Optional) Name of the group the contacts belong to
        Sorting
        sortBy (Optional) Property to sort by. Available values: PhoneNumber, FirstName, LastName, CreatedAt
        sortDir (Optional) Direction of sorting. Available values: asc, desc
        Pagination
        itemsPerPage (Optional) Number of results to retrieve. By default, 10 most recently added contacts are retrieved.
        page (Optional) Page of results to retrieve

        result - list of contact objects
        """
        res = self._get("/contacts",  query=query, source=source, optout=optout, group=group, sortBy=sortBy, sortDir=sortDir, itemsPerPage=itemsPerPage, page=page)
        return self._parse_contacts_result(res)

    def get_contact_by_id(self, id):
        """Get a single contact stored in your Ez Texting contact list.
        """
        res = self._get("/contacts/"+id)
        return self._parse_contact_result(res)

    def delete_contact(self, id):
        """Delete a contact stored in your Ez Texting contact list.
        """
        self._delete("/contacts/"+id)

    def create_contact(self, contact):
        """Create a new contact that will be stored in your Ez Texting contact list.

           contact - Contact object. PhoneNumber is required, other fields are optional.
           returns contact object
        """
        res = self._post("/contacts", PhoneNumber=contact.phone_number, FirstName=contact.first_name, LastName=contact.last_name, Email=contact.email, Groups=contact.groups, Note=contact.note)
        return self._parse_contact_result(res)

    def update_contact(self, contact):
        """Update a contact stored in your Ez Texting contact list.

           contact - Contact object. id and PhoneNumber are required, other fields are optional.
           returns contact object
        """
        res = self._post("/contacts/"+contact.id, PhoneNumber=contact.phone_number, FirstName=contact.first_name, LastName=contact.last_name, Email=contact.email, Groups=contact.groups, Note=contact.note)
        return self._parse_contact_result(res)

    def get_all_groups(self, query=None, source=None, optout=None, group=None, sortBy=None, sortDir=None, itemsPerPage=None, page=None):
        """Get a list of groups stored in your Ez Texting account.

        Sorting
        sortBy (Optional) Property to sort by. Available values: Name
        sortDir (Optional) Direction of sorting. Available values: asc, desc
        Pagination
        itemsPerPage (Optional) Number of results to retrieve. By default, first 10 groups sorted in alphabetical order are retrieved.
        page (Optional) Page of results to retrieve

        result - list of group objects
        """
        res = self._get("/groups",  sortBy=sortBy, sortDir=sortDir, itemsPerPage=itemsPerPage, page=page)
        return self._parse_groups_result(res)

    def get_group_by_id(self, id):
        """Get a single group stored in your Ez Texting group list.
        """
        res = self._get("/groups/"+id)
        return self._parse_group_result(res)

    def delete_group(self, id):
        """Delete a group stored in your Ez Texting account.
        """
        self._delete("/groups/"+id)

    def create_group(self, group):
        """Create a new group that will be stored in your Ez Texting account.

           group - group object. name is required, note is optional.
           returns group object
        """
        res = self._post("/groups", Name=group.name, Note=group.note)
        return self._parse_group_result(res)

    def update_group(self, group):
        """Update a group stored in your Ez Texting account.

           group - group object. id and name are required, note is optional.
           returns group object
        """
        res = self._post("/groups/"+group.id, Name=group.name, Note=group.note)
        return self._parse_group_result(res)



class EzTextingError:
    def __init__(self, error_code, errors):
        self.error_code = error_code
        self.errors = errors
    def __str__(self):
       return 'Error code: ' + str(self.error_code) + \
              ', Errors description: ' + str(self.errors)
    def __repr__(self):
        return self.__str__()

class Contact:
    def __init__(self, phone_number, first_name=None, last_name=None, email=None, note=None, groups=None, source=None, created_at=None, id=None):
        self.id = id
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.note = note
        self.source = source
        self.groups = groups
        self.created_at = created_at

    def __str__(self):
       return 'Contact ID: ' + self.id + \
              ', Phone Number: ' + self.phone_number + \
              ', First Name: ' + self.first_name + \
              ', Last Name: ' + self.last_name + \
              ', Email: ' + self.email + \
              ', Note: ' + self.note + \
              ', Source: ' + self.source + \
              ', Groups: ' + str(self.groups) + \
              ', CreatedAt: ' + self.created_at
    def __repr__(self):
        return self.__str__()

class Group:
    def __init__(self, name, note=None, contacts_number=None, id=None):
        self.id = id
        self.name = name
        self.note = note
        self.contacts_number = contacts_number

    def __str__(self):
       return 'Group ID: ' + self.id + \
              ', Name: ' + self.name + \
              ', Note: ' + self.note + \
              ', Number of Contacts: ' + str(self.contacts_number)
    def __repr__(self):
        return self.__str__()
