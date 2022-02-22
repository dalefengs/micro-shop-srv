# 加密字符串
import random
import string


def pbkdf2_encry(password, salt):
    from hashlib import pbkdf2_hmac
    from binascii import hexlify
    dk = pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 8000, 16)
    return hexlify(dk).decode("utf-8")


# 验证加密字符串
def pbkdf2_verify(encrypt_password, password, salt):
    dk = pbkdf2_encry(password, salt)
    if encrypt_password != dk:
        return False
    return True


# 生成随机推荐码
def create_sn(first, length):
    # 大小写字母+数字
    char = string.ascii_letters + string.digits
    str = [random.choice(char) for _ in range(length)]
    return first + ''.join(str)



