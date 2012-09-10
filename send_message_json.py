import pycurl, StringIO, urllib, simplejson as json

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnie&Password=the-pooh"
params+= "&Subject=From Winnie"
params+= "&Message=I am a Bear of Very Little Brain, and long words bother me"
params+= "&PhoneNumbers[]=2123456785&PhoneNumbers[]=2123456786"
params+= "&MessageTypeID=1&StampToSend=1305582245"

curl.setopt(pycurl.POSTFIELDS, params)

curl.setopt(pycurl.URL, "https://app.eztexting.com/sending/messages?format=json")

contents = StringIO.StringIO()
curl.setopt(pycurl.WRITEFUNCTION, contents.write) 

curl.perform()

print contents.getvalue() + "\n==============================\n" #result of API call

responseCode = curl.getinfo(pycurl.HTTP_CODE);
print 'Response code: ' + str(responseCode);
isSuccesResponse = responseCode < 400;

pyobj = json.loads(contents.getvalue())

print 'Status: ' + str(pyobj['Response']['Status'])
print 'Code: ' + str(pyobj['Response']['Code'])
if (isSuccesResponse):
    print 'Message ID: ' + str(pyobj['Response']['Entry']['ID'])
    print 'Subject: ' + pyobj['Response']['Entry']['Subject']
    print 'Message: ' + pyobj['Response']['Entry']['Message']
    print 'Message Type ID: ' + str(pyobj['Response']['Entry']['MessageTypeID'])
    print 'Total Recipients: ' + str(pyobj['Response']['Entry']['RecipientsCount'])
    print 'Credits Charged: ' + str(pyobj['Response']['Entry']['Credits'])
    print 'Time To Send: ' + pyobj['Response']['Entry']['StampToSend']
    print 'Phone Numbers: ' + str(pyobj['Response']['Entry']['PhoneNumbers'])
    try:    
        print 'Locally Opted Out Numbers: ' + str(pyobj['Response']['Entry']['LocalOptOuts'])
    except KeyError:
        pyobj['Response']['Entry']['LocalOptOuts'] = ''
    try:
        print 'Globally Opted Out Numbers: ' + pyobj['Response']['Entry']['GlobalOptOuts']
    except KeyError:
        pyobj['Response']['Entry']['GlobalOptOuts'] = ''
else:
    print 'Errors: ' + str(pyobj['Response']['Errors'])
              