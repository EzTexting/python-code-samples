import EzTextingJSON as EzTexting

ez = EzTexting.EzTextingJSON("https://app.eztexting.com", "ezdemo", "password")


try:
    print 'get_all_contacts'
    print ez.get_all_contacts(group='Honey Lovers')
    print

    contact = EzTexting.Contact('2123456796', 'Piglet', 'P.', 'piglet@small-animals-alliance.org', 'It is hard to be brave, when you are only a Very Small Animal.')
    contact = ez.create_contact(contact)
    print 'create_contact: ' + str(contact)

    contact = ez.get_contact_by_id(contact.id)
    print 'get_contact_by_id: ' + str(contact)

    contact.groups=['Friends', 'Neighbors']
    contact = ez.update_contact(contact)
    print 'update_contact: ' + str(contact)

    print 'delete.'
    ez.delete_contact(contact.id)

    print 'second delete. try to get error'
    ez.delete_contact(contact.id)

except EzTexting.EzTextingError, error:
    print str(error)
