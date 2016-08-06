import logging
import random

import requests
import os
import simplejson as j

from caesar import CaesarCipher

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:",
            "> `<@" + bot_uid + "> decrypt [message] (key)` - I'll decrypt your message with a Caesar Cipher!",
            "> `<@" + bot_uid + "> encrypt [message] [key]` - I'll encrypt your message with a Caesar Cipher!")

        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)

    def encrypt_caesar(self, channel_id, msg_txt):
        bot_uid = self.clients.bot_user_id()
        txt = "Encrypting!"
        c = CaesarCipher()
        mode = 'encrypt'
        message = msg_txt[21:-2]

        msg_txt = msg_txt.strip().replace('  ', ' ') # remove double spacing

        if len(msg_txt) < 22:
            txt = '@caesar encrypt [message] [key]'
            self.send_message(channel_id, txt)
            return
        if msg_txt[-1:].isdigit():
            key = int(msg_txt[-1:])
        else:
            txt = 'Missing key'
            self.send_message(channel_id, txt)
            return

        
        txt = c.getTranslatedMessage(mode, message, key)

        self.send_message(channel_id, txt)

    def decrypt_caesar(self, channel_id, msg_txt):
        #add NLP
        bot_uid = self.clients.bot_user_id()
        c = CaesarCipher()
        mode = 'decrypt'

        msg_txt = msg_txt.strip().replace('  ', ' ') # remove double spacing
        key = 0

        if len(msg_txt) < 20:
            txt = '@caesar decrypt [message] (key)'
            self.send_message(channel_id, txt)
            return
        if msg_txt[-1:].isdigit():
            key = int(msg_txt[-1:])
            message = msg_txt[21:-2]
            txt = c.getTranslatedMessage(mode, message, key)
        else:
            message = msg_txt[21:]
            detect_language_key=os.environ["DETECT_LANGUAGE"]
            current_best = 0.0
            txt = 'Original message: ' + message + '\n'
            #txt = 'No Decryption Found'
            for i in range(0, 25):
                tmp_msg = c.getTranslatedMessage(mode, message, i)
                txt = txt + '\n' + tmp_msg
                #txt = txt + ', tmpmsg: ' + tmp_msg

                #r = requests.get('http://ws.detectlanguage.com/0.2/detect?q=' + tmp_msg + '&key=' + detect_language_key)
                #js = r.json()
                #if js['data']['detections'] and js['data']['detections'][0]['language'] is 'en':
                #    if js['data']['detections'][0]['confidence'] > current_best:
                #        current_best = js['data']['detections'][0]['confidence']
                #        txt = txt + ', ' + tmp_msg

        self.send_message(channel_id, txt)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
