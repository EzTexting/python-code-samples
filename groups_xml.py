import EzTextingXML as EzTexting

ez = EzTexting.EzTextingXML("https://app.eztexting.com", "ezdemo", "password")


try:
    print 'get_all_groups'
    print ez.get_all_groups(sortBy='Name', sortDir='asc', itemsPerPage=10)
    print

    group = EzTexting.Group('Tubby Bears', 'A bear, however hard he tries, grows tubby without exercise')
    group = ez.create_group(group)
    print 'create_group: ' + str(group)

    group = ez.get_group_by_id(group.id)
    print 'get_group_by_id: ' + str(group)

    group = ez.update_group(group)
    print 'update_group: ' + str(group)

    print 'delete.'
    ez.delete_group(group.id)

    print 'second delete. try to get error'
    ez.delete_group(group.id)

except EzTexting.EzTextingError, error:
    print str(error)
