import pycurl, StringIO, urllib, simplejson as json

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnie&Password=the-pooh"
params+= "&Keyword=honey"
params+= "&Subject=From Winnie"
params+= "&Keyword=honey"
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

curl.setopt(pycurl.URL, "https://app.eztexting.com/keywords?format=json")

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
    print 'Keyword ID: ' + str(pyobj['Response']['Entry']['ID'])
    print 'Keyword: ' + str(pyobj['Response']['Entry']['Keyword'])
    print 'Is double opt-in enabled: ' + str(pyobj['Response']['Entry']['EnableDoubleOptIn'])
    print 'Confirm message: ' + str(pyobj['Response']['Entry']['ConfirmMessage'])
    print 'Join message: ' + str(pyobj['Response']['Entry']['JoinMessage'])
    print 'Forward email: ' + str(pyobj['Response']['Entry']['ForwardEmail'])
    print 'Forward url: ' + str(pyobj['Response']['Entry']['ForwardUrl'])
    print 'Groups: ' + str(pyobj['Response']['Entry']['ContactGroupIDs'])
else:
    print 'Errors: ' + str(pyobj['Response']['Errors'])
