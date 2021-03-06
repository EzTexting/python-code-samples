import EzTextingJSON as EzTexting

sms = EzTexting.EzTextingJSON("https://app.eztexting.com", "centerft", "texting121212")


try:
    print 'get_all_messages'
    messages = sms.get_all_messages(sortBy='Name', sortDir='asc', itemsPerPage=10)
    print messages
    print
    
    message_id = messages[0].id

    print 'move messages to folder: '
    sms.move_message_to_folder(message_id, 77)


    message = sms.get_message_by_id(message_id)
    print 'get_message_by_id: ' + str(message)

    print 'delete.'
    sms.delete_message(message_id)

    print 'second delete. try to get error'
    sms.delete_message(message_id)

except EzTexting.EzTextingError, error:
    print str(error)