from notifiers import get_notifier

token = "5782231345:AAFHSrVArIm7B88w1iP0F4TFOdAiPzwm2NI"
id = "5521639964"

def send_to_tg(data):
    telegram = get_notifier('telegram')
    info = "\n".join([i for i in data])
    telegram.notify(token=token,chat_id = id,message = info)
    print("MSG HAS BEEN SENT")


