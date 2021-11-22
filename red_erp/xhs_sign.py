import hashlib

x_sign = "X"
# api = "/fe_api/burdock/v2/user/keyInfo/${userId}"
api = "/fe_api/burdock/v2/user/keyInfo/6011212c000000000101e7f4"
m = hashlib.md5()
m.update((api + "WSUDD").encode())
sign = x_sign + m.hexdigest()
print(sign)