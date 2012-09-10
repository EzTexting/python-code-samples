import pycurl, StringIO, urllib, xml.etree.ElementTree as ET

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

curl.setopt(pycurl.URL, "https://app.eztexting.com/sending/messages?format=xml")

contents = StringIO.StringIO()
curl.setopt(pycurl.WRITEFUNCTION, contents.write) 

curl.perform()

print contents.getvalue() + "\n==============================" #result of API call

responseCode = curl.getinfo(pycurl.HTTP_CODE);
print 'Response code: ' + str(responseCode);
isSuccesResponse = responseCode < 400;

def getText(x): return x.text

doc = ET.XML(contents.getvalue())

print 'Status: ' + doc.findtext('Status')
print 'Code: ' + doc.findtext('Code')
if (isSuccesResponse):
    print 'Message ID: ' + doc.findtext('Entry/ID')
    print 'Subject: ' + doc.findtext('Entry/Subject')
    print 'Message: ' + doc.findtext('Entry/Message')
    print 'Message Type ID: ' + doc.findtext('Entry/MessageTypeID')
    print 'Total Recipients: ' + doc.findtext('Entry/RecipientsCount')
    print 'Credits Charged: ' + doc.findtext('Entry/Credits')
    print 'Time To Send: ' + doc.findtext('Entry/StampToSend')
    print 'Phone Numbers: ' + ', '.join(map(getText, doc.findall('Entry/PhoneNumbers/PhoneNumber')))
    print 'Locally Opted Out Numbers: ' + ', '.join(map(getText, doc.findall('Entry/LocalOptOuts/PhoneNumber')))
    print 'Globally Opted Out Numbers: ' + ', '.join(map(getText, doc.findall('Entry/GlobalOptOuts/PhoneNumber')))
else:
    print 'Errors: ' + ', '.join(map(getText, doc.findall('Errors/Error')))
              