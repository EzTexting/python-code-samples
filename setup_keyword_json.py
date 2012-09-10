import pycurl, StringIO, urllib, simplejson as json

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

curl.setopt(pycurl.URL, "https://app.eztexting.com/keywords/honey?format=json")

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