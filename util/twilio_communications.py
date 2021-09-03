# How to get first phone number
    # https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account


from twilio.rest import Client
from log         import Log
from datetime import datetime

class Twilio_Communications():
    def __init__(self, parameter_dict: dict, log_file: Log):
        self.client                   = Client(parameter_dict['twilio_account_sid'], parameter_dict['twilio_auth_token'])
        self.my_cell_number           = parameter_dict['my_cell_number']
        self.bot_phonenumber          = parameter_dict['twilio_bot_phonenumber']
        self.log_file                 = log_file
        self.sent_text                = False
    
    
    def get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")


    def print_and_log(self, message, e=False):
        if e:
            print(              f"[!] {self.get_current_time()} ERROR: {message}")
            self.log_file.write(f"[!] {self.get_current_time()} ERROR: {message}")
            self.log_file.write(f"[!] {self.get_current_time()} {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
            return
        print(              f"[*] {self.get_current_time()} {message}")
        self.log_file.write(f"[*] {self.get_current_time()} {message}")



    def send_text(self, position, margin_ratio):
        try:
            if not self.sent_text:
                body = f"WARNING, your position {position} margin ratio is {margin_ratio}."
                self.client.messages.create(
                        from_ = self.bot_phonenumber,
                        to    = self.my_cell_number,
                        body  = body)
                
                self.sent_text = True
                self.print_and_log(message=f"Sent {position} margin ratio: {margin_ratio} text")
        except Exception as e:
            self.print_and_log(message="could not sent text message", e=e)


    def send_disconnected_text(self, message):
        try:
            self.client.messages.create(
                    from_ = self.bot_phonenumber,
                    to    = self.my_cell_number,
                    body  = message)
            self.sent_text = True
            self.print_and_log(message="Sent disconnected text")
        except Exception as e:
            self.print_and_log(message="could not sent disconnected text", e=e)



    def send_phone_call(self):
        try:
            self.client.calls.create(
                    url   = "https://demo.twilio.com/docs/voice.xml",
                    from_ = self.bot_phonenumber,
                    to    = self.my_cell_number)
            self.sent_text = True
            self.print_and_log("Sent phone call")
        except Exception as e:
            self.print_and_log(message="could not send phone call", e=e)
