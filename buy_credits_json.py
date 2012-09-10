import pycurl, StringIO, urllib, simplejson as json

curl = pycurl.Curl()
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(pycurl.CAINFO, "cacert.pem")

params = ""
params+= "User=demo&Password=password"
params+= "&NumberOfCredits=1000"
params+= "&CouponCode=honey2011"
params+= "&StoredCreditCard=1111"


curl.setopt(pycurl.POSTFIELDS, params)

curl.setopt(pycurl.URL, "https://app.eztexting.com/billing/credits?format=json")

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
    print 'Credits purchased: ' + str(pyobj['Response']['Entry']['BoughtCredits'])
    print 'Amount charged, $: ' + str(pyobj['Response']['Entry']['Amount'])
    print 'Discount, $: ' + str(pyobj['Response']['Entry']['Discount'])
    print 'Plan credits: ' + str(pyobj['Response']['Entry']['PlanCredits'])
    print 'Anytime credits: ' + str(pyobj['Response']['Entry']['AnytimeCredits'])
    print 'Total: ' + str(pyobj['Response']['Entry']['TotalCredits'])
else:
    print 'Errors: ' + str(pyobj['Response']['Errors'])
