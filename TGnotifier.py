from notifiers import get_notifier

token = "XXXXX"
id = "XXXXX"

def send_to_tg(data):
    telegram = get_notifier('telegram')
    info = "\n".join([i for i in data])
    telegram.notify(token=token,chat_id = id,message = info)
    print("MSG HAS BEEN SENT")


