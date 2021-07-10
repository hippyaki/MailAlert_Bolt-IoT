import sms_conf, email_conf, tele_conf, bolt_conf
from boltiot import Sms, Email, Bolt
import json, time, requests

HIGH = "HIGH"
LOW ="LOW"

mybolt = Bolt(bolt_conf.API_KEY, bolt_conf.DEVICE_ID)
sms = Sms(sms_conf.SID, sms_conf.AUTH_TOKEN, sms_conf.TO_NUMBER, sms_conf.FROM_NUMBER)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)

print(".")
print ("********* MailBox Alert System ACTIVE *********")
print(".")
print(".")
mybolt.digitalWrite(3,"LOW")
mybolt.digitalWrite(2,"LOW")
def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + tele_conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": tele_conf.telegram_chat_id,
        "text": message
    }
    try:
        response_tele = requests.request(
            "POST",
            url,
            params=data
        )
      #  print("This is the Telegram URL")
      #  print(url)
      #  print("This is the Telegram response")
      #  print(response_tele.text)
        telegram_data = json.loads(response_tele.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False
        
        

while True: 
#    print ("Reading sensor value")
    response = mybolt.digitalRead('0') 
    data = json.loads(response)     
#    print("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = str(data['value']) 
        mybolt.digitalWrite(2,"HIGH")
        if  sensor_value == "1":
            mybolt.digitalWrite(2,"LOW")
            mybolt.digitalWrite(3,"HIGH")
            print("Mail Recieved !")
            print(".")
            print(".")
            print("Making request to alert on all devices")
            print(".")
            print(".")
            
            response_sms = sms.send_sms("You received a letter in your mail box!")
          # print("Response received from Twilio is: " + str(response_sms))
            print("Status of SMS at Twilio is :" + str(response_sms.status))
            print(".")
            print(".")
            response_email = mailer.send_email ("Physical MAIL","You received a mail in your MAILBOX")
            response_text = json.loads(response_email.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
            print(".")
            print(".")         
            message = "You received a letter in your mail box !!"
            telegram_status = send_telegram_message(message)
            print("This is the Telegram status:", telegram_status)
            print(".")
            print(".")
            print(".")
            print(".")
            input("Press any button once you have received the mail. Do you want to reset the system?")
            print(".")
            print("System RESET complete")
            mybolt.digitalWrite(3,"LOW")
            print(".")
            print(".")
            print ("********* MailBox Alert System ACTIVE *********")
            print(".")
            print(".")
        
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(0)
    


