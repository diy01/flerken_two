import hashlib
import socket
import time


class License():

    def __encryption(self, content):
        hl = hashlib.md5()
        content = "h#@d)*@r)06gg@u#54t=&=i!53-opisa=9s7mzgofp@+7hr&ly" + content + "gv2z4$7n&u3n@0&03+j)f&=#d!9=4moubw^rhudrt8eyys08l2"
        hl.update(content.encode())
        return hl.hexdigest()

    def check_hostname(self, hostname):
        local_hostname = socket.gethostname()
        if hostname == self.__encryption(local_hostname):
            return True, "success"
        return False, "illegal host"

    def __get_license_key(self, license):
        content = "{expiration_date}|{start_date}|{full_name}|{company}|{email}|{license_type}|{nodes}".format(
            **license)
        return self.__encryption(content)

    def check_date(self, license):
        expiration_date = license.get("expiration_date")
        start_date = license.get("start_date")
        expiration_date_time = time.mktime(time.strptime(expiration_date, "%Y年%m月%d号")) + 86400
        start_date_time = time.mktime(time.strptime(start_date, "%Y年%m月%d号"))
        if time.time() >= start_date_time and time.time() < expiration_date_time:
            return True, "success"
        return False, "license expiration"

    def check_license(self, license):
        if not license:
            return False, "illegal license"
        try:
            license_key = self.__get_license_key(license)
            if license_key == license.get("license_key"):
                res, msg = self.check_hostname(license.get("hostname"))
                if not res:
                    return res, msg
                return self.check_date(license)
        except:
            pass
        return False, "illegal license"

    def check_nodes(self, license, nodes):
        res, msg = self.check_license(license)
        if not res:
            return res, msg
        if license.get("nodes") < nodes:
            return True, "success"
        return False, "number of illegal nodes"

    def get_license(self, company, email, full_name, hostname, start_date, expiration_date, nodes, license_type):
        license = {
            "company": company,
            "email": email,
            "full_name": full_name,
            "start_date": start_date,
            "expiration_date": expiration_date,
            "nodes": nodes,
            "license_type": license_type,
            "hostname": self.__encryption(hostname),
        }
        license_key = self.__get_license_key(license)
        license['license_key'] = license_key
        return license
