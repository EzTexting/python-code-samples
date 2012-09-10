import pycurl, StringIO, urllib, xml.etree.ElementTree as ET

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnie&Password=the-pooh"
params+= "&NumberOfCredits=1000"
params+= "&CouponCode=honey2011"
params+= "&FirstName=Winnie"
params+= "&LastName=The Pooh"
params+= "&Street=Hollow tree, under the name of Mr. Sanders"
params+= "&City=Hundred Acre Woods"
params+= "&State=New York"
params+= "&Zip=12345"
params+= "&Country=US"
params+= "&CreditCardTypeID=Visa"
params+= "&Number=4111111111111111"
params+= "&SecurityCode=123"
params+= "&ExpirationMonth=10"
params+= "&ExpirationYear=2017"


curl.setopt(pycurl.POSTFIELDS, params)

curl.setopt(pycurl.URL, "https://app.eztexting.com/billing/credits?format=xml")

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
    print 'Credits purchased: ' + doc.findtext('Entry/BoughtCredits')
    print 'Amount charged, $: ' + doc.findtext('Entry/Amount')
    print 'Discount, $: ' + doc.findtext('Entry/Discount')
    print 'Plan credits: ' + doc.findtext('Entry/PlanCredits')
    print 'Anytime credits: ' + doc.findtext('Entry/AnytimeCredits')
    print 'Total: ' + doc.findtext('Entry/TotalCredits')
else:
    print 'Errors: ' + ', '.join(map(getText, doc.findall('Errors/Error')))
                    