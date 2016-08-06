import requests
import os
import simplejson as j

detect_language_key=os.environ["DETECT_LANGUAGE"]
#txt = 'my name is vincent'
#txt = 'xj ylxp td gtynpye'
txt = 'n mfaj f wji hzu'
#txt = 'rd sfrj nx anshjsy'
r = requests.get('http://ws.detectlanguage.com/0.2/detect?q=' + txt + '&key=' + detect_language_key)
print(r.status_code)
js = r.json()
print(j.dumps(js, indent=4*' '))

if not js['data']['detections']:
    print("hit")
print(js['data']['detections'])

#print(js["data"]["detections"][0]["language"])
#print(js["data"]["detections"][0]["confidence"])
#print(js)

#print(r.text)
#txt = 'rd sfrj nx anshjsy'
#r = requests.get('http://ws.detectlanguage.com/0.2/detect?q=' + txt + '&key=' + detect_language_key)
#print(r.text)
