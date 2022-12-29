import string
import requests
from celery import shared_task
from .models import advertising


@shared_task
def Thread(id,email):
    response = requests.get(
    'https://api.imagga.com/v2/tags?image_url=%s' % 'https://cloudhw.s3.ir-thr-at1.arvanstorage.com/' + str(id)+'.jpg',
            auth=('acc_3922ebc91e7966a', '1ea32bc773aa293ad66b048309e8588b'))
    data = response.json()
    res=data["result"]["tags"]
    category=""
    percent=0
    for i in res:
        conf=i["confidence"]
        text=i["tag"]["en"]
        if(text == "car" or text == "vehicle" or text == "motor" or text == "bus" ):
            if(conf>percent):
                percent=conf
                category=text
    if(percent>30):
        advertisment=advertising.objects.get(id=id)
        advertisment.category=category
        advertisment.state=1
        advertisment.save()
        message="Advertisment with id "+str(id)+" is accepted"
        requests.post(
		"https://api.mailgun.net/v3/sandbox9ea6c617f2fc43438587fe29f3ef7958.mailgun.org/messages",
		auth=("api", "4a8d6994a2e1e8c2095247728e8a5d84-2de3d545-ef85a533"),
		data={"from": "Excited User <mailgun@sandbox9ea6c617f2fc43438587fe29f3ef7958.mailgun.org>",
			"to": [email],
			"subject": "Advertisment APP",
			"text": message})
        
    else:
        advertisment=advertising.objects.get(id=id)
        advertisment.state=3
        advertisment.save()
        message="Advertisment with id "+str(id)+" is rejected"
        requests.post(
		"https://api.mailgun.net/v3/sandbox9ea6c617f2fc43438587fe29f3ef7958.mailgun.org/messages",
		auth=("api", "4a8d6994a2e1e8c2095247728e8a5d84-2de3d545-ef85a533"),
		data={"from": "Excited User <mailgun@sandbox9ea6c617f2fc43438587fe29f3ef7958.mailgun.org>",
			"to": [email],
			"subject": "Advertisment APP",
			"text": message})
    
    

        

        ## send advertisment to second service

        
        