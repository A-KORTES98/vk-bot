import time
import vk_api
import sys
import os
dir = os.path.dirname(__file__)
sys.path.append(dir)
from router.controller import redirectToHandler


INSTANCE_QUERRY = -1
FINISH_DIALOGUE = 0
START_DIALOGUE = 1
CONTINUE_DIALOGUE = 2

vk = vk_api.VkApi(login = '<your login>', password = '<your password')
vk.auth()
values = {'out': 0,'count': 100,'time_offset': 10}
print('Bot\'s running...')

def isMsgToBot(msg):
    if msg.find('=>bot=>') != -1:
        return -1, msg.replace('=>bot=>', '').strip(' ')
    if msg.find('=>bot') != -1:
        return 1, msg
    if msg.find('<=bot') != -1:
        return 0, msg
    return 2, msg


def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})


def addUpdateNewMsgInf(dialogues, msg, vk):
    isToBot, message = isMsgToBot(msg['body'])
    for dialogue in dialogues:
        if msg['user_id'] == dialogue['person']:
            if isToBot is CONTINUE_DIALOGUE and dialogue['bot_state'] is START_DIALOGUE:
                dialogue.update({'time': msg['date'], 'preUltMsgTime': dialogue['time']})
                return True
            elif not (isToBot is CONTINUE_DIALOGUE):
                if dialogue['bot_state'] is START_DIALOGUE and isToBot is FINISH_DIALOGUE:
                    write_msg(dialogue['person'], 'Bye-bye :-)')
                if isToBot is START_DIALOGUE and dialogue['bot_state']:
                    write_msg(dialogue['person'], 'Hi!')
                dialogue.update({'bot_state': isToBot})
                return False
    if isToBot is START_DIALOGUE:
        dialogues.append({'person': msg['user_id'],
                          'time': msg['date'],
                          'preUltMsgTime': 0,
                          'bot_state': 1})
        write_msg(msg['user_id'], 'Hi!')
    return False




dialogues = []
timeLastSelfMes = 0

while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        if item['user_id'] != 325710986 or time.time() - timeLastSelfMes > 4:
            if item['user_id'] == 325710986:
                timeLastSelfMes = time.time()
            msgType, msg = isMsgToBot(item['body'])
            if msgType is INSTANCE_QUERRY:
                print('instance querry')
                write_msg(item['user_id'], redirectToHandler(msg))
            elif addUpdateNewMsgInf(dialogues, item, vk):
                print('usual querry')
                write_msg(item['user_id'], redirectToHandler(item['body']))
            print(dialogues)
    time.sleep(1)



