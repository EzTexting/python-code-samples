import pycurl, StringIO, urllib, simplejson as json

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnielkup&Password=winnielkup"

curl.setopt(pycurl.URL, "https://app.eztexting.com/sending/phone-numbers/2345678910?format=json&"+params)

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
    print 'Phone number: ' + str(pyobj['Response']['Entry']['PhoneNumber'])
    print 'CarrierName: ' + pyobj['Response']['Entry']['CarrierName']
else:
    print 'Errors: ' + str(pyobj['Response']['Errors'])