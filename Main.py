import sms_conf, email_conf, tele_conf, bolt_conf
from boltiot import Sms, Email, Bolt
import json, time, requests

minimum_limit = 500  


mybolt = Bolt(bolt_conf.API_KEY, bolt_conf.DEVICE_ID)
sms = Sms(sms_conf.SID, sms_conf.AUTH_TOKEN, sms_conf.TO_NUMBER, sms_conf.FROM_NUMBER)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)


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
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response_tele.text)
        telegram_data = json.loads(response_tele.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False
        

while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = int(data['value']) 
        if  sensor_value > minimum_limit:
            print("Object Detected")
            print("Making request to alert on all devices")
            
            response_sms = sms.send_sms("You received a letter in your mail box at location  XYZ!!")
            print("Response received from Twilio is: " + str(response_sms))
            print("Status of SMS at Twilio is :" + str(response_sms.status))
            
            response_email = mailer.send_email ("Alert","Please check your mail box at location XYZ")
            response_text = json.loads(response_email.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
                        
            message = "Alert! You have a new MAIL in location XYZ "
            telegram_status = send_telegram_message(message)
            print("This is the Telegram status:", telegram_status)
        
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(50)
    


