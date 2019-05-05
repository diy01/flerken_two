# -*- coding: utf-8 -*-

import json, requests
from ..models import BasePath

def get_token(tokenKey):
    try:
        basePath = BasePath.objects.all().first()
        if not basePath:
            return False, '未设置'
        url = "{0}/api/sso/token/{1}/".format(basePath.sso_url.rstrip("/"), tokenKey)
        response = requests.get(url, params={}, headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            return False, response.text
        userinfo = json.loads(response.text)
        return True, userinfo
    except Exception as ex:
        return False, str(ex)