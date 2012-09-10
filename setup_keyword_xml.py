import pycurl, StringIO, urllib, xml.etree.ElementTree as ET

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnie&Password=the-pooh"
params+= "&EnableDoubleOptIn=true";
params+= "&ConfirmMessage=Reply Y to join our sweetest list";
params+= "&JoinMessage=The only reason for being a bee that I know of, is to make honey. And the only reason for making honey, is so as I can eat it.";
params+= "&ForwardEmail=honey@bear-alliance.co.uk";
params+= "&ForwardUrl=http://bear-alliance.co.uk/honey-donations/";
params+= "&ContactGroupIDs[]=honey";
params+= "&ContactGroupIDs[]=lovers";


curl.setopt(pycurl.POSTFIELDS, params)

curl.setopt(pycurl.URL, "https://app.eztexting.com/keywords/honey?format=xml")

contents = StringIO.StringIO()
curl.setopt(pycurl.WRITEFUNCTION, contents.write) 

curl.perform()

print contents.getvalue() + "\n==============================\n" #result of API call

responseCode = curl.getinfo(pycurl.HTTP_CODE);
print 'Response code: ' + str(responseCode);
isSuccesResponse = responseCode < 400;

def getText(x): return x.text
doc = ET.XML(contents.getvalue())

print 'Status: ' + doc.findtext('Status')
print 'Code: ' + doc.findtext('Code')
if (isSuccesResponse):
     print 'Keyword ID: ' + doc.findtext('Entry/ID')
     print 'Keyword: ' + doc.findtext('Entry/Keyword')
     print 'Is double opt-in enabled: ' + doc.findtext('Entry/EnableDoubleOptIn')
     print 'Confirm message: ' + doc.findtext('Entry/ConfirmMessage')
     print 'Join message: ' + doc.findtext('Entry/JoinMessage')
     print 'Forward email: ' + doc.findtext('Entry/ForwardEmail')
     print 'Forward url: ' + doc.findtext('Entry/ForwardUrl')
     print 'Groups: ' + ', '.join(map(getText, doc.findall('Entry/ContactGroupIDs/Group')))
else:
    print 'Errors: ' + ', '.join(map(getText, doc.findall('Errors/Error')))