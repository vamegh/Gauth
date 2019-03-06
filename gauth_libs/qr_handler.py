import base64
import logging
import os
import qrcode
import random
from file_handler import FileHandler

class GenQR(object):
    def __init__(self, config_data=None):
        self.config_data = config_data
        self.handle = FileHandler

    def gen_secrets(self):
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
        self.config_data["secrets"] = {}
        self.config_data["secrets"]["key"] = secret_key
        self.config_data["secrets"]["scratch_codes"] = scratch_codes
        return secret_key, scratch_codes

    def gen_qrcode(self):
        properties = self.config_data['properties']
        qr_code_store = self.config_data['qr_config']['file_store']
        service_name = properties['name']
        service_env = properties['backend']
        user_email = self.config_data['user_details']['email']
        user_id = self.config_data['user_details']['uid']
        qr_ident = ("%s-%s(%s :: %s)" % (
            service_name, service_env, user_id, user_email))
        secret = self.config_data['secrets']['key']
        qrcode_data = ("otpauth://totp/%s?secret=%s" % (qr_ident, secret))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=40,
            border=5,
        )
        qr_image_file = os.path.join(qr_code_store, user_id, user_id+".png")
        self.handle.make_dir(path=qr_image_file)
        self.config_data['qr_config']['image_file'] = qr_image_file

        qr.add_data(qrcode_data)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(qr_image_file)

    def gen_auth_file(self):
        gen_auth_data = ("%s\n\" RATE_LIMIT 3 30\n\" TOTP_AUTH\n" % self.config_data['secrets']['key'])
        gen_auth_data += '\n'.join(self.config_data['secrets']['scratch_codes'])
        qr_code_store = self.config_data['qr_config']['file_store']
        user_id = self.config_data['user_details']['uid']
        auth_file = os.path.join(qr_code_store, user_id, ".google-authenticator")
        self.config_data['qr_config']['auth_file'] = auth_file
        self.handle.write_file(output_file=auth_file, data=gen_auth_data)

# self.config_data = {'user_details': {}}
# self.config_data['system'] = "TEST"
# self.config_data['user_details'] = {"email": "vam@gmail.com", "uid": "vam"}
# gen_secrets(self.config_data=self.config_data)
# gen_qrcode(self.config_data=self.config_data)
# gen_auth_file(self.config_data=self.config_data)
