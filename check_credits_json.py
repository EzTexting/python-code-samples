import pycurl, StringIO, urllib, simplejson as json

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=winnie&Password=the-pooh"

curl.setopt(pycurl.URL, "https://app.eztexting.com/billing/credits/get?format=json&"+params)

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
    print 'Plan credits: ' + str(pyobj['Response']['Entry']['PlanCredits'])
    print 'Anytime credits: ' + str(pyobj['Response']['Entry']['AnytimeCredits'])
    print 'Total: ' + str(pyobj['Response']['Entry']['TotalCredits'])
else:
    print 'Errors: ' + str(pyobj['Response']['Errors'])

