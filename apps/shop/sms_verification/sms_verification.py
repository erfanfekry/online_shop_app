from sms_ir import SmsIr

class SendSms(SmsIr):
     def __init__(self):
         self.api_key = 'CUbdri4GHW2nmfbt7WqYMRZ5Gx5nz3SRy1POOJfIPCbCf2xu'
         # self.linenumber = 50003181890144
         super().__init__(api_key=self.api_key)

def notification_sms(number, message):
    sms_manager = SendSms()
    sms_manager.send_sms(number, message)

def verification_sms(number, template_id, parameters):
    sms_manager = SendSms()
    sms_manager.send_verify_code(number, template_id, parameters)


