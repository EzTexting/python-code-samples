import pycurl, StringIO, urllib, xml.etree.ElementTree as ET

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnie&Password=the-pooh"


curl.setopt(pycurl.POSTFIELDS, params)

curl.setopt(pycurl.URL, "https://app.eztexting.com/keywords/honey?format=xml&_method=DELETE")

contents = StringIO.StringIO()
curl.setopt(pycurl.WRITEFUNCTION, contents.write) 

curl.perform()

print contents.getvalue() + "\n==============================\n" #result of API call

responseCode = curl.getinfo(pycurl.HTTP_CODE);
print 'Response code: ' + str(responseCode);
isSuccesResponse = responseCode < 400;

def getText(x): return x.text

if (not isSuccesResponse):
    doc = ET.XML(contents.getvalue())
    print 'Status: ' + doc.findtext('Status')
    print 'Code: ' + doc.findtext('Code')
    print 'Errors: ' + ', '.join(map(getText, doc.findall('Errors/Error')))