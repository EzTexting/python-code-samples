import EzTextingJSON as EzTexting

sms = EzTexting.EzTextingJSON("https://app.eztexting.com", "centerft", "texting121212")


try:
    print 'get_all_folders'
    print sms.get_all_folders()
    print

    folder = EzTexting.Group('Customers')
    folder = sms.create_folder(folder)
    print 'create_folder: ' + str(folder)

    folder_id = folder.id

    folder = sms.get_folder_by_id(folder_id)
    print 'get_folder_by_id: ' + str(folder)

    print 'update_folder.'
    folder.id = folder_id
    folder.name = 'Customers2'
    sms.update_folder(folder)

    folder = sms.get_folder_by_id(folder_id)
    print 'get_folder_by_id: ' + str(folder)

    print 'delete.'
    sms.delete_folder(folder_id)

    print 'second delete. try to get error'
    sms.delete_folder(folder_id)

except EzTexting.EzTextingError, error:
    print str(error)