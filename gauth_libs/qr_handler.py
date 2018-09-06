import base64
import logging
import os
import qrcode
import random


def gen_secrets(config=None):
    scratch_codes = []
    scratch_random = random.SystemRandom()
    scratch_count = 0

    try:
        # python3 method - this gets random entropy from /dev/random and urandom
        seed = os.getrandom(10, flags=0)
        secret_key = base64.b32encode(seed).decode('utf_8')
    except:
        # python2 method - this only uses /dev/urandom
        seed = os.urandom(10)
        secret_key = base64.b32encode(seed)

    while scratch_count < 5:
        rand_num = scratch_random.randrange(0, 99999999)
        scratch_codes.append(str(rand_num).zfill(8))
        scratch_count += 1

    logging.debug("Secret Key: %s :: Scratch Codes: %s", secret_key, scratch_codes)
    config["secrets"] = {}
    config["secrets"]["key"] = secret_key
    config["secrets"]["scratch_codes"] = scratch_codes
    return secret_key, scratch_codes


def gen_qrcode(config=None):
    qr_ident = ("GAUTH-%s(%s :: %s)" % (config['system'], config['user_details']['email'], config['user_details']['uid']))
    secret = config['secrets']['key']
    qrcode_data = ("otpauth://totp/%s?secret=%s" % (qr_ident, secret))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=40,
        border=5,
    )

    qr.add_data(qrcode_data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("image.png")


def gen_auth_file(config=None):
    gen_auth_data = ("%s\n\" RATE_LIMIT 3 30\n\" TOTP_AUTH\n" % config['secrets']['key'])
    gen_auth_data += '\n'.join(config['secrets']['scratch_codes'])
    print(gen_auth_data)

# config = {'user_details': {}}
# config['system'] = "XRDP"
# config['user_details'] = {"email": "vam@gmail.com", "uid": "vam"}
# gen_secrets(config=config)
# gen_qrcode(config=config)
# gen_auth_file(config=config)
