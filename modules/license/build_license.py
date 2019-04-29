from license import License
import json

company = "shfanxi"
email = "Jackson@shfanxi.com"
full_name = "Jackson"
hostname = "DESKTOP-E062GCK"
start_date = "2019年4月20号"
expiration_date = "2032年4月19号"
nodes = 20
license_type = "Normal"
lic = License().get_license(company, email, full_name, hostname, start_date, expiration_date, nodes, license_type)
with open("LICENSE.txt", "w") as fp:
    json_str = json.dumps(lic, sort_keys=True, indent=4, separators=(',', ':')).encode('utf-8').decode('unicode_escape')
    print(json_str)
    fp.write(json.dumps(lic, sort_keys=True, indent=4, separators=(',', ':')).encode('utf-8').decode('unicode_escape'))
