from flask import Flask, request
import telepot
import urllib3
import re, random
import openai

from supabase import create_client, Client

url: str = "YOUR_SUPABASE_URL"
key: str = "YOUR_SUPABASE_KEY"
supabase: Client = create_client(url, key)

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "YOUR_SECRET_TOKEN"
bot = telepot.Bot('YOUR_TELEGRAM_BOT_TOKEN')
bot.setWebhook("YOUR_WEBHOOK".format(secret), max_connections=1)

openai.api_key = "YOUR_OPENAI_API_KEY"

tg_commands = {}

 # return cmd, params
def parse_cmd(cmd_string):
	text_split = cmd_string.split()
	return text_split[0], text_split[1:]

def add_command(cmd, func):
	global tg_commands
	tg_commands[cmd] = func

def remove_command(cmd):
	global tg_commands
	del tg_commands[cmd]

started = False

def start_bot(chat_id):
    add_command("/echo", cmd_echo)
    add_command("/list", list)
    add_command("/jumlah", jumlah)
    add_command("/love", love)
    add_command("/delete", delete)
    add_command("/ai", chatbot)
    add_command("/hanna", hanna)
    started = True
    bot.sendMessage(chat_id, "bot baru nyala lagi, ulang dong commandnya")


app = Flask(__name__)


@app.route('/')
def hello_world():
    add_command("/echo", cmd_echo)
    add_command("/list", list)
    add_command("/jumlah", jumlah)
    add_command("/love", love)
    add_command("/delete", delete)
    add_command("/ai", chatbot)
    add_command("/hanna", hanna)
    return 'Hello from Flask!'

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    global tg_commands
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            if text[0] == '/':
                cmd, params = parse_cmd(text)
                try:
                    tg_commands[cmd](chat_id, params)
                except KeyError:
                    if not started:
                        start_bot(chat_id)
                    else:
                        bot.sendMessage(chat_id, "Unknown command: {cmd}".format(cmd=cmd))

            else:
                try:
                    name = re.search(r"\w+", text).group()
                    descTemp = re.search(r"\bd=\w+", text)
                    desc="Empty"

                    if descTemp:
                        desc = descTemp.group()[2:]

                    priceTemp = re.search(r"\bp=\w+", text)
                    if priceTemp:
                        price = int(priceTemp.group()[2:])
                    else:
                        return "NOT OK"
                    reply = insert_data(name, desc, price)
                    bot.sendMessage(chat_id, reply)
                except:
                    bot.sendMessage(chat_id, "Gagal Banget :(")
                    return "NOT OK"

            # bot.sendMessage(chat_id, "From the web: you said '{}'".format(text))
        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"

def cmd_echo(chat_id, params):
	bot.sendMessage(chat_id, "[ECHO] {text}".format(text=" ".join(params)))

def insert_data(name, desc, price):
    name = name.lower()

    final_price = get_current_final_price()
    # OPTIONAL
    if name == "azriel":
        final_price = final_price - price
    elif name == "tiva":
        final_price = final_price + price
    else:
        return "Kamu bukan Azriel atau Tiva, Siapa Kamu??"

    try:
        data = supabase.table("buku-pengeluaran").insert(
            {
                "name": name,
                "desc": desc,
                "price": price,
                "final_price": final_price
            }
            ).execute()
        if(data.data[0].get('name') == name):
            if final_price == 0:
                return "Asikk Lunas semua :D\nJumlah akhir: 0"
            res="Rp {:,}".format(final_price)
            return "Berhasil!! jumlah akhir: " + res
        else:
            return 'Gagal :('
    except:
        return 'Gagal :('


def jumlah(chat_id, params=""):
    final_price = get_current_final_price()
    res="Rp {:,}".format(final_price)
    bot.sendMessage(chat_id, 'Jumlah akhir: ' + res)

def list(chat_id, params):
    try:
        limit = int(params[0])
        if limit <= 0:
            limit  =10
    except:
        limit = 10
    try:
        data = get_table_list(limit)
        msg = "List: \n"
        for i in reversed(data):
            msg += "{}, {}, {}, {}, {}".format(i.get('name'), i.get('desc'), i.get('price'), i.get('created_at')[:10], i.get('final_price'))
            msg += "\n"
        bot.sendMessage(chat_id, msg)
    except:
        bot.sendMessage(chat_id, 'error')

def love(chat_id, params=""):
    bot.sendMessage(chat_id, "I love you!!")
    i = random.randint(1, 2)
    if i == 0:
        bot.sendDocument(chat_id, "https://media.giphy.com/media/BXrwTdoho6hkQ/giphy.gif")
    elif i == 1:
        bot.sendDocument(chat_id, "https://media.giphy.com/media/GMUTanoEMDhUEcsnPs/giphy.gif")
    else:
        bot.sendDocument(chat_id, "https://media.giphy.com/media/Ut8FZWMUJW0bv9D4yp/giphy.gif")


def get_table_list(limit=10):
    data = supabase.table("buku-pengeluaran").select('*').order('id', desc=True).limit(limit).execute()
    return data.data

def get_current_final_price():
    data = supabase.table("buku-pengeluaran").select('*').order('id', desc=True).limit(1).execute()
    if len(data.data) == 0:
        return 0
    return int(data.data[0].get('final_price'))

def delete(chat_id, params):
    try:
        limit = int(params[0])
        if limit > 5:
            limit = 5
    except:
        limit = 1

    data = get_table_list(limit)
    for i in data:
        supabase.table("buku-pengeluaran").delete().eq('id', i.get('id')).execute()

    msg = str(limit) + " data berhasil dihapus!!\n"
    final_price = get_current_final_price()
    res="Rp {:,}".format(final_price)
    msg += "Jumlah akhir: " + res
    bot.sendMessage(chat_id, msg)


messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]

messages_lalita = [
    {"role": "system", "content": "Act like a very young cute girl named Hanna, and i am your parents."},
]


def chatbot(chat_id, params):
    input = " ".join(params)
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        bot.sendMessage(chat_id, reply)
        # return reply

def hanna(chat_id, params):
    input = " ".join(params)
    if input:
        messages_lalita.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages_lalita
        )
        reply = chat.choices[0].message.content
        messages_lalita.append({"role": "assistant", "content": reply})
        bot.sendMessage(chat_id, reply)
        # return reply
