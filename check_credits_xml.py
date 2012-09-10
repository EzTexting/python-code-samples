import pycurl, StringIO, urllib, xml.etree.ElementTree as ET

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = "User=winnie&Password=the-pooh"

curl.setopt(pycurl.URL, "https://app.eztexting.com/billing/credits/get?format=xml&"+params)

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
    print 'Plan credits: ' + doc.findtext('Entry/PlanCredits')
    print 'Anytime credits: ' + doc.findtext('Entry/AnytimeCredits')
    print 'Total: ' + doc.findtext('Entry/TotalCredits')
else:
    print 'Errors: ' + ', '.join(map(getText, doc.findall('Errors/Error')))
