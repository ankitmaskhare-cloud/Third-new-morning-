import os
import json
import logging
import re
import random
import threading
import subprocess
import html
from datetime import datetime
from flask import Flask
from telebot import TeleBot, types
from telebot.types import MessageEntity

BOT_TOKEN = "8874395177:AAE0x-pdE9IMYSB-aQDwnKDNYKzGKlRuqD8"
ADMIN_IDS = [8498419947, 6862525056]

# 📁 RENDER SAFE PATH
DATA_FILE = os.path.join(os.getcwd(), "data.json")
WELCOME_DIR = os.path.join(os.getcwd(), "welcome_files")
os.makedirs(WELCOME_DIR, exist_ok=True)

# 💎 PREMIUM EMOJI MAPPING
PREMIUM_EMOJI_MAP = {
    "✅": ["6113743365826677162"],
    "📢": ["5931641120458018914"],
    "🧠": ["6271505894089952985"],
    "🔄": ["6242148104699648157"],
    "🥳": ["6242018680155152197"],
    "🦸‍♂": ["6242014252043868089"],
    "😄": ["6240160909231135849"],
    "🥏": ["6242113113601089103"],
    "❤️‍🔥": ["6242105356890151132"],
    "🔗": ["6116012762121377264"],
    "📎": ["6118262478875922552"],
    "🔺": ["5823288729191584314"],
    "📌": ["6068848489293422081"],
    "☄️": ["6068866888933317376"],
    "💁‍♀": ["6068998173198655021"],
    "💸": ["6332581398485931268"],
    "🔴": ["4992743110430687913"],
    "😉": ["6242158090498610126"],
    "😌": ["6242183396445918139"],
    "😍": ["6242440158180808121"],
    "🥰": ["6242062076504709224"],
    "📥": ["6330021121236145815"],
    "🔥": ["6332589971240655050"],
    "🚨": ["6334665239308537561"],
    "🚀": ["6332241232781121574"],
    "🔮": ["5042302287087666158"],
    "👑": ["5816539591812845173"],
    "🔛": ["5990026957419453239"],
    "👀": ["6053362469311617342"],
    "🤡": ["5323588426971227340"],
    "😀": ["6105039966788655018"],
    "🔼": ["6105002832501414007"],
    "🆘": ["5294057271226017876"],
    "🆑": ["5294125024335112026"],
    "🅾️": ["5292250898175633031"],
    "🅱️": ["5294194388056941995"],
    "🆎": ["5294467530797098107"],
    "🌹": ["6278173680493137560"],
    "💎": ["6204123844400124499"],
    "😂": ["6246887506621507085"],
    "📈": ["6093561301617875302"],
    "🎁": ["6093372095423585554"],
    "👆": ["6084832734071493634"],
    "💘": ["6266818250818983044"],
    "🎥": ["6264778055454036969"],
    "⭐": ["6138574830917655563"],
    "🍓": ["6242379654976509431"],
    "🍒": ["6242014252043868089"],
    "🍎": ["6242347743369500459"],
    "🍅": ["5900140601948507995"],
    "🌶️": ["5785281906459283269"],
    "🍉": ["6014898614814382254"],
    "🍑": ["6267225207560214192"],
    "🍊": ["6267291337171670780"],
    "🥕": ["6266787022111773140"],
    "🥭": ["6265037836550936046"],
    "🍍": ["6266955436369385728"],
    "🍌": ["6266973397922616654"],
    "🌽": ["6264720734820505831"],
    "🍋": ["6267128480601741166"],
    "🍋‍🟩": ["6267097569722111582"],
    "🍈": ["6267019543051244106"],
    "🍐": ["6267264360482084046"],
    "🥬": ["5244837092042750681"],
    "🫑": ["5246762912428603768"],
    "🍏": ["5224607267797606837"],
    "🥝": ["5276032951342088188"],
    "🥑": ["6111778259374971023"],
    "🫒": ["5949775417274536507"],
    "🥦": ["6246589483135802654"],
    "🥒": ["6244267675355193452"],
    "🫐": ["6246859052463170661"],
    "🍆": ["6246994769134756588"],
    "🍠": ["6242198351522045253"],
    "🫜": ["6242126625568200803"],
    "🥥": ["6030520420187246063"],
    "🥔": ["6030366192206614299"],
    "🍄‍🟫": ["6030433717682442920"],
    "🧅": ["6028145874503208169"],
    "🫚": ["6028220478085140634"],
    "🧄": ["6030617915944866144"],
    "🫘": ["6035277294036061660"],
    "🌰": ["6267152480878990865"],
    "🥜": ["6266818688905648040"],
    "🍞": ["6267264360482084046"],
    "🫓": ["6282702779341346176"],
    "🥐": ["5990107500941155180"],
    "🥖": ["5989930621303004669"],
    "🥯": ["5990238269810415926"],
    "🧇": ["5990350016269523841"],
    "🥞": ["6332180738166755902"],
    "🍳": ["6332256157792474083"],
    "🥚": ["6332473066525824816"],
    "🧀": ["6332189220727165527"],
    "🥓": ["6332297784615506761"],
    "🥩": ["6334316251740902076"],
    "🍗": ["6332595717906895459"],
    "🍖": ["6334586168960619847"],
    "🍔": ["6332546471811880304"],
    "🌭": ["6332159589747790307"],
    "🥪": ["6332240524111517402"],
    "🥨": ["6075586403922613321"],
    "🏳": ["6339025777870246403"],
    "🏴": ["6339262095560807956"],
    "🏁": ["6339005123372531098"],
    "🚩": ["6053143898425923591"],
    "🏳‍🌈": ["6053102331732432506"],
    "🇺🇳": ["6339065871389955418"],
    "🇦🇫": ["6052857209358914564"],
    "🇦🇽": ["6339066575764592250"],
    "🇦🇱": ["6339262924489496713"],
    "🇩🇿": ["6237985246302703400"],
    "🇦🇸": ["6240082457358503826"],
    "🇨🇨": ["6285188903980767740"],
    "🇨🇴": ["6284987710532754549"],
    "🇰🇲": ["6287052181052856661"],
    "🇨🇬": ["6287104253236355155"],
    "🇨🇩": ["6287267320259681921"],
    "🇨🇰": ["6285263550512373440"],
    "🇨🇷": ["6287385861357051284"],
    "🇹🇷": ["5354992008068876024"],
    "🇹🇹": ["5355007482836043677"],
    "🇹🇻": ["5377341072257074555"],
    "🇹🇼": ["5375458772774828569"],
    "🇹🇿": ["5375418116614404422"],
    "🇺🇦": ["5375173015715725713"],
    "🇺🇬": ["6222270837139968654"],
    "🇺🇲": ["6221943109660447566"],
    "🇺🇳": ["6221953348862481057"],
    "🇺🇸": ["6222199261509980700"],
    "🇺🇾": ["6221901877974406204"],
    "🇺🇿": ["5346146797800672155"],
    "🇻🇦": ["6224489303712472312"],
    "🇻🇨": ["6093456762113888541"],
    "🇻🇪": ["5809816842713174497"],
    "✔️": ["5330165881622244007"],
    "☑️": ["5332315315185396200"],
    "⬆️": ["5330515320161446557"],
    "↗️": ["5332355889741442089"],
    "➡️": ["5332554068122414227"],
    "↘️": ["5332617728127674636"],
    "⬇️": ["5330533062671346265"],
    "↙️": ["5332732390869578276"],
    "⬅️": ["5332651666959249030"],
    "↖️": ["5330417699849776583"],
    "↕️": ["5330394730364677082"],
    "↔️": ["6111742817304841054"],
    "↩️": ["6269048584386122161"],
    "↪️": ["6269400956387987689"],
    "⤴️": ["6269232765468676321"],
    "⤵️": ["6149904924579731857"],
    "🔃": ["6269377265348383859"],
    "🔄": ["6269458311381258421"],
    "🔙": ["6156513311585211842"],
    "🔛": ["6319056439096644016"],
    "🔝": ["6147942648511469492"],
    "🔚": ["6149683785303595272"],
    "🔜": ["5323442290708985472"],
    "🆕": ["5397782960512444700"],
    "🆓": ["6244574039667383201"],
    "🆙": ["6246891007019850969"],
    "🤷‍♀": ["6247042980142652905"],
    "🆗": ["6246515983360465678"],
    "🆒": ["6246999343274925978"],
    "🆖": ["6241993399977647842"],
    "ℹ️": ["6035277294036061660"],
    "🅿️": ["5785281906459283269"],
    "🈁": ["6014898614814382254"],
    "🈂️": ["6266787717896476444"],
    "🈳": ["6264695922794435129"],
    "🔣": ["6264989131621798851"],
    "🔤": ["6332410244039184167"],
    "🔠": ["6334811650448692061"],
    "🔡": ["6332480157516829285"],
    "🔢": ["6332254542884770988"],
    "#️⃣": ["6332445342511927824"],
    "*️⃣": ["6332502731864937801"],
    "0️⃣": ["6334677754843239333"],
    "1️⃣": ["6332592616940508489"],
    "2️⃣": ["6075586403922613321"],
    "3️⃣": ["6199705590067892461"],
    "4️⃣": ["5203924002380212799"],
    "5️⃣": ["5204354538491899693"],
    "6️⃣": ["5201729420120847803"],
    "7️⃣": ["5204439853722269655"]
}

COLOR_MAP = {"blue": "primary", "green": "success", "red": "danger"}

DEFAULT_CAPTIONS = {
    "video": "✅NEW HACK How To Activate Hack✅\n  Pls Video Ko Pura Dekhna\n        ✅ Setup Video ✅\n\n✅ FULL NUMBER WORKING  ✅",
    "document": "📥 📌 🎥\n\n👆 DOWNLOAD & USE FAST 💸\n\n💎 MINIMUM DEPOSIT 300+ 💎\n\n🔥 FULL NUMBER WORKING 🔥",
    "photo": "✅✅✅✅✅✅✅✅\n\n✅ DOWNLOAD & USE FAST ✅\n\n✅ MINIMUM DEPOSIT 300+ ✅\n\n✅ FULL NUMBER WORKING  ✅",
    "voice": "✅ Voice Message ✅",
    "audio": "✅ Audio File ✅"
}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = TeleBot(BOT_TOKEN, threaded=True)

DEFAULT_DATA = {
    "welcome_contents": [],
    "users": [],
    "stats": {"approved": 0, "channels": {}},
    "pinned_content": None,
    "join_enabled": True
}

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                loaded = json.load(f)
                for item in loaded.get("welcome_contents", []):
                    if "caption_entities" in item and item["caption_entities"]:
                        entities = []
                        for e_dict in item["caption_entities"]:
                            entities.append(MessageEntity(type=e_dict.get("type", "custom_emoji"), offset=e_dict.get("offset", 0), length=e_dict.get("length", 1), custom_emoji_id=e_dict.get("custom_emoji_id", "")))
                        item["caption_entities"] = entities
                for key in DEFAULT_DATA:
                    if key not in loaded: 
                        loaded[key] = DEFAULT_DATA[key]
                return loaded
    except Exception as e: 
        logger.error(f"Load: {e}")
    return DEFAULT_DATA.copy()

def save_data(d):
    def conv(obj):
        if isinstance(obj, MessageEntity): 
            return {"type": obj.type, "offset": obj.offset, "length": obj.length, "custom_emoji_id": obj.custom_emoji_id}
        if isinstance(obj, dict): 
            return {k: conv(v) for k, v in obj.items()}
        if isinstance(obj, list): 
            return [conv(i) for i in obj]
        return obj
    with open(DATA_FILE, 'w') as f: 
        json.dump(conv(d), f, indent=4)

data = load_data()
for key in DEFAULT_DATA:
    if key not in data: 
        data[key] = DEFAULT_DATA[key]
save_data(data)

user_states = {}

def is_admin(uid): 
    return uid in ADMIN_IDS

def format_quotes(text):
    if not text: 
        return ""
    return re.sub(r'"([^"]*)"', r'<blockquote>\1</blockquote>', text)

def convert_premium_emojis(text):
    if not text: 
        return text, []
    entities = []
    for plan_emoji, emoji_ids in PREMIUM_EMOJI_MAP.items():
        start = 0
        while True:
            pos = text.find(plan_emoji, start)
            if pos == -1: 
                break
            utf16_offset = len(text[:pos].encode('utf-16-le')) // 2
            utf16_length = len(plan_emoji.encode('utf-16-le')) // 2
            selected_id = random.choice(emoji_ids)
            entities.append(MessageEntity(type="custom_emoji", offset=utf16_offset, length=utf16_length, custom_emoji_id=selected_id))
            start = pos + len(plan_emoji)
    entities.sort(key=lambda x: x.offset)
    return text, entities

def extract_button_icon(text):
    for plan_emoji, emoji_ids in PREMIUM_EMOJI_MAP.items():
        if plan_emoji in text:
            icon_id = random.choice(emoji_ids)
            clean_text = text.replace(plan_emoji, "").strip()
            return clean_text, icon_id
    return text, None

def colored_btn(text, url=None, callback=None, color="primary", icon_emoji_id=None):
    if url:
        return types.InlineKeyboardButton(text, url=url, style=color, icon_custom_emoji_id=icon_emoji_id)
    return types.InlineKeyboardButton(text, callback_data=callback, style=color, icon_custom_emoji_id=icon_emoji_id)

def build_keyboard_with_rows(buttons_list):
    mrk = types.InlineKeyboardMarkup(row_width=2)
    buttons_by_row = {}
    for b in buttons_list:
        row = b.get("row", 0)
        if row not in buttons_by_row:
            buttons_by_row[row] = []
        icon_id = b.get("icon_emoji_id", None)
        buttons_by_row[row].append(colored_btn(b['text'], url=b["url"], color=b.get("color", "primary"), icon_emoji_id=icon_id))
    for row_num in sorted(buttons_by_row.keys()):
        row_buttons = buttons_by_row[row_num]
        if len(row_buttons) == 1:
            mrk.add(row_buttons[0])
        else:
            mrk.add(*row_buttons)
    return mrk

def send(chat_id, text, reply_markup=None, **kwargs):
    if isinstance(text, str):
        clean_txt, emoji_entities = convert_premium_emojis(text)
        if emoji_entities:
            return bot.send_message(chat_id, clean_txt, entities=emoji_entities, reply_markup=reply_markup, **kwargs)
        return bot.send_message(chat_id, clean_txt, reply_markup=reply_markup, parse_mode="HTML", **kwargs)
    return bot.send_message(chat_id, text, reply_markup=reply_markup, **kwargs)

def send_html(chat_id, text, reply_markup=None):
    clean_txt, emoji_entities = convert_premium_emojis(text)
    if emoji_entities:
        return bot.send_message(chat_id, clean_txt, entities=emoji_entities, reply_markup=reply_markup, disable_web_page_preview=True)
    return bot.send_message(chat_id, clean_txt, reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)

def send_media_with_caption(func, chat_id, file_id, caption="", reply_markup=None, **kwargs):
    if 'filename' in kwargs:
        kwargs['visible_file_name'] = kwargs.pop('filename')
    if caption:
        clean_cap, cap_entities = convert_premium_emojis(caption)
        if cap_entities:
            return func(chat_id, file_id, caption=clean_cap, caption_entities=cap_entities, reply_markup=reply_markup, **kwargs)
        return func(chat_id, file_id, caption=clean_cap, reply_markup=reply_markup, **kwargs)
    return func(chat_id, file_id, reply_markup=reply_markup, **kwargs)

def send_pinned_content(chat_id, user_name="User", channel_name="Channel"):
    pinned_idx = data.get("pinned_content")
    if pinned_idx is not None:
        contents = data.get("welcome_contents", [])
        if 0 <= pinned_idx < len(contents):
            item = contents[pinned_idx]
            try:
                safe_name = html.escape(user_name) if user_name else "User"
                safe_channel = html.escape(channel_name) if channel_name else "Channel"
                markup = build_keyboard_with_rows(item["buttons"]) if item.get("buttons") else None
                
                if item["type"] == "text":
                    txt = item["content"].replace("{name}", safe_name).replace("{channel}", safe_channel)
                    txt = format_quotes(txt)
                    send(chat_id, f"📌 PINNED\n━━━━━━━━━━━━━\n{txt}", reply_markup=markup)
                    return True
                elif item["type"] in ["video", "photo", "document", "voice", "audio"]:
                    cap = item.get("caption", "").replace("{name}", safe_name).replace("{channel}", safe_channel)
                    cap = format_quotes(cap)
                    
                    if item.get("is_file_id", False):
                        file_source = item.get("content")
                    else:
                        file_path = item.get("content", "")
                        if not os.path.exists(file_path): 
                            return False
                        file_source = open(file_path, 'rb')

                    try:
                        if item["type"] == "video":
                            send_media_with_caption(bot.send_video, chat_id, file_source, cap, reply_markup=markup, supports_streaming=True)
                        elif item["type"] == "photo":
                            send_media_with_caption(bot.send_photo, chat_id, file_source, cap, reply_markup=markup)
                        elif item["type"] == "document":
                            send_media_with_caption(bot.send_document, chat_id, file_source, cap, reply_markup=markup, visible_file_name=item.get("filename", "file"))
                        elif item["type"] == "voice":
                            send_media_with_caption(bot.send_voice, chat_id, file_source, cap)
                        elif item["type"] == "audio":
                            send_media_with_caption(bot.send_audio, chat_id, file_source, cap)
                    finally:
                        if not item.get("is_file_id", False) and hasattr(file_source, 'close'):
                            file_source.close()
                    return True
            except Exception as e: 
                logger.error(f"Pin: {e}")
    return False

def send_welcome_contents(chat_id, user_name="User", channel_name="Channel"):
    pin_sent = send_pinned_content(chat_id, user_name, channel_name)
    contents = data.get("welcome_contents", [])
    sent = False
    if contents:
        for item in contents:
            try:
                markup = build_keyboard_with_rows(item["buttons"]) if item.get("buttons") else None
                safe_name = html.escape(user_name) if user_name else "User"
                safe_channel = html.escape(channel_name) if channel_name else "Channel"
                
                if item["type"] == "text":
                    txt = item["content"].replace("{name}", safe_name).replace("{channel}", safe_channel)
                    txt = format_quotes(txt)
                    if not pin_sent: 
                        send(chat_id, txt, reply_markup=markup)
                    sent = True
                elif item["type"] in ["video", "photo", "document", "voice", "audio"]:
                    cap = item.get("caption", "").replace("{name}", safe_name).replace("{channel}", safe_channel)
                    cap = format_quotes(cap)
                    
                    if item.get("is_file_id", False):
                        file_source = item.get("content")
                    else:
                        file_path = item.get("content", "")
                        if not os.path.exists(file_path): 
                            continue
                        file_source = open(file_path, 'rb')

                    try:
                        if item["type"] == "video":
                            send_media_with_caption(bot.send_video, chat_id, file_source, cap, reply_markup=markup, supports_streaming=True)
                        elif item["type"] == "photo":
                            send_media_with_caption(bot.send_photo, chat_id, file_source, cap, reply_markup=markup)
                        elif item["type"] == "document":
                            send_media_with_caption(bot.send_document, chat_id, file_source, cap, reply_markup=markup, visible_file_name=item.get("filename", "file"))
                        elif item["type"] == "voice":
                            send_media_with_caption(bot.send_voice, chat_id, file_source, cap)
                        elif item["type"] == "audio":
                            send_media_with_caption(bot.send_audio, chat_id, file_source, cap)
                    finally:
                        if not item.get("is_file_id", False) and hasattr(file_source, 'close'):
                            file_source.close()
                    sent = True
            except Exception as e: 
                logger.error(f"Welcome: {e}")
    return sent or pin_sent

# 🌐 JOIN HANDLER (FIXED)
@bot.chat_join_request_handler()
def handle_join(update: types.ChatJoinRequest):
    user = update.from_user
    chat = update.chat
    uid, name, chat_id, channel = user.id, user.first_name, chat.id, chat.title
    ckey = str(chat_id)
    
    if "channels" not in data["stats"]: 
        data["stats"]["channels"] = {}
    if ckey not in data["stats"]["channels"]: 
        data["stats"]["channels"][ckey] = {"name": channel, "approved": 0}
    
    try:
        if data.get("join_enabled", True):
            bot.approve_chat_join_request(chat_id, uid)
            data["stats"]["approved"] += 1
            data["stats"]["channels"][ckey]["approved"] += 1
        
        if uid not in data["users"]: 
            data["users"].append(uid)
        save_data(data)
        
        safe_name = html.escape(name)
        send(uid, f"HELLO {safe_name} 🌹")
        
        sent = send_welcome_contents(uid, name, channel)
        if not sent: 
            send(uid, f"")
    except Exception as e:
        logger.error(f"Join: {e}")

# ⚙️ COMMANDS
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    user = message.from_user
    if user.id not in data["users"]: 
        data["users"].append(user.id)
        save_data(data)
    
    if is_admin(user.id):
        join_status = "🟢 ON" if data.get("join_enabled", True) else "🔴 OFF"
        text = f"""╔══════════════════════╗\n║  🏆 <b>ALL-IN-ONE BOT</b>  ║\n╚══════════════════════╝\n👑 <b>Admin:</b> {user.first_name}\n📋 /welcome | /stats | /pin | /help\n\n📥 <b>Join Accept:</b> {join_status}\n\n<i>💡 Admin = Normal | Forward = Forward Tag</i>\n<i>💎 Premium Emojis Loaded!</i>"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            colored_btn("START ✅", callback="join_on", color="success"),
            colored_btn("OFF 🔴", callback="join_off", color="danger")
        )
        markup.add(colored_btn("Welcome", callback="welcome_menu", color="primary"), colored_btn("Stats", callback="stats", color="success"))
        send_html(message.chat.id, text, reply_markup=markup)
    else:
        user_name = html.escape(user.first_name)
        send(message.chat.id, f"HELLO {user_name} 🌹")
        
        sent = send_welcome_contents(message.chat.id, user.first_name, "Channel")
        if not sent: 
            send(message.chat.id, "")

@bot.message_handler(commands=['pin'])
def pin_cmd(message: types.Message):
    if not is_admin(message.from_user.id): 
        send(message.chat.id, "❌ Admin only!")
        return
    contents = data.get("welcome_contents", [])
    if not contents: 
        send(message.chat.id, "⚠️ Pehle /welcome से content add karo!")
        return
    t = "📌 <b>PIN CONTENT</b>\n\n"
    for i, item in enumerate(contents, 1):
        prev = item.get("content", item.get("filename", ""))[:30] if item["type"] == "text" else item.get("filename", item["type"].upper())
        t += f"  {i}. {'📝' if item['type']=='text' else '📁'} {prev}\n"
    t += "\n✏️ Number (0=unpin):"
    user_states[message.from_user.id] = "pin_select"
    send_html(message.chat.id, t)

@bot.message_handler(commands=['unpin'])
def unpin_cmd(message: types.Message):
    if not is_admin(message.from_user.id): 
        send(message.chat.id, "❌ Admin only!")
        return
    data["pinned_content"] = None
    save_data(data)
    send(message.chat.id, "✅ Pin removed!")

@bot.message_handler(commands=['welcome'])
def welcome_cmd(message: types.Message):
    if not is_admin(message.from_user.id): 
        send(message.chat.id, "❌ Admin only!")
        return
    contents = data.get("welcome_contents", [])
    pinned = data.get("pinned_content")
    text = f"🎨 <b>WELCOME BUILDER</b>\n\n📝 Contents: {len(contents)}\n"
    if pinned is not None: 
        text += f"📌 <b>PINNED:</b> #{pinned+1}\n"
    text += "\n"
    if contents:
        text += "<b>Current:</b>\n"
        for i, item in enumerate(contents, 1):
            t = item["type"]
            prev = item["content"][:30] if t == "text" else item.get("filename", t.upper())
            text += f"  {i}. {'📝' if t=='text' else '📁'} {prev} [{len(item.get('buttons',[]))}🔘] {'📌' if pinned==i-1 else ''}\n"
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(colored_btn("Add Text", callback="add_text", color="primary"), colored_btn("Add File", callback="add_file", color="success"))
    markup.add(colored_btn("Add Button", callback="btn_add", color="danger"), colored_btn("Pin Content", callback="pin_menu", color="primary"))
    markup.add(colored_btn("Edit", callback="edit_menu", color="danger"), colored_btn("Delete", callback="delete_menu", color="danger"))
    markup.add(colored_btn("Preview", callback="preview", color="success"), colored_btn("Clear All", callback="clear", color="danger"))
    send_html(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['stats'])
def stats_cmd(message: types.Message):
    ch = data.get("stats", {}).get("channels", {})
    pinned = data.get("pinned_content")
    join_status = "🟢 ON" if data.get("join_enabled", True) else "🔴 OFF"
    text = f"📊 <b>STATS</b>\n\n✅ Approved: {data['stats']['approved']}\n📢 Channels: {len(ch)}\n📝 Contents: {len(data.get('welcome_contents',[]))}\n👥 Users: {len(data.get('users',[]))}\n💎 Emojis: {len(PREMIUM_EMOJI_MAP)}\n📥 Join: {join_status}"
    if pinned is not None: 
        text += f"\n📌 Pinned: #{pinned+1}"
    send_html(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_cmd(message: types.Message):
    text = "📋 <b>COMMANDS ✅</b>\n\n/welcome | /stats | /pin | /unpin | /help\n\n📥 <b>START/OFF Buttons</b> se join on/off karo!\n\n💡 <b>Button Format:</b>\n<code>Text ✅ | URL/color/row:1</code>"
    send_html(message.chat.id, text)

# 🎛️ CALLBACKS
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call: types.CallbackQuery):
    uid = call.from_user.id
    if not is_admin(uid): 
        bot.answer_callback_query(call.id, "❌ Admin only!", show_alert=True)
        return
    cmd = call.data
    contents = data.get("welcome_contents", [])
    bot.answer_callback_query(call.id)
    
    if cmd == "join_on":
        data["join_enabled"] = True
        save_data(data)
        send(call.message.chat.id, "🟢 <b>Join Accept ON!</b>")
        return
    elif cmd == "join_off":
        data["join_enabled"] = False
        save_data(data)
        send(call.message.chat.id, "🔴 <b>Join Accept OFF!</b>")
        return
    
    if cmd == "welcome_menu": 
        welcome_cmd(call.message)
    elif cmd == "stats": 
        stats_cmd(call.message)
    elif cmd == "pin_menu":
        if not contents: 
            send(call.message.chat.id, "⚠️ Pehle content add!")
            return
        t = "📌 <b>PIN CONTENT</b>\n\n"
        for i, item in enumerate(contents, 1):
            prev = item.get("content", item.get("filename", ""))[:30] if item["type"] == "text" else item.get("filename", item["type"].upper())
            t += f"{i}. {'📝' if item['type']=='text' else '📁'} {prev}\n"
        t += "\nNumber (0=unpin):"
        user_states[uid] = "pin_select"
        send_html(call.message.chat.id, t)
    elif cmd == "add_text": 
        user_states[uid] = "adding_text"
        send_html(call.message.chat.id, "📝 Welcome text ✅\n\nUse {name} | {channel} | \"text\" for quotes\n\n/cancel")
    elif cmd == "add_file": 
        user_states[uid] = "adding_file"
        send_html(call.message.chat.id, "📁 File bhejo 📁\n\nCaption likho - ✅😂🔥⭐ sab auto premium!\n\n/cancel")
    elif cmd == "btn_add":
        if not contents: 
            send(call.message.chat.id, "⚠️ Pehle text add!")
            return
        user_states[uid] = "adding_button"
        t = "🔘 <b>ADD BUTTONS</b>\n\nKis content ke niche?\n\n"
        for i, item in enumerate(contents, 1):
            prev = item.get("content", item.get("filename", ""))[:30] if item["type"] == "text" else item.get("filename", item["type"].upper())
            t += f"<b>Content {i}:</b> {'📝' if item['type']=='text' else '📁'} {prev}\n"
        t += "\n<b>Format:</b>\n<code>Content Number\nButton1 ✅ | URL/blue/row:1\nButton2 🚀 | URL/green/row:1</code>\n\n/cancel"
        send_html(call.message.chat.id, t)
    elif cmd == "edit_menu":
        if not contents: 
            send(call.message.chat.id, "⚠️ No content!")
            return
        t = "✏️ <b>SELECT ✅</b>\n\n"
        for i, item in enumerate(contents, 1): 
            t += f"{i}. {'📝' if item['type']=='text' else '📁'} {item.get('content',item.get('filename',''))[:30]}\n"
        t += "\nNumber:"
        user_states[uid] = "edit_select"
        send_html(call.message.chat.id, t)
    elif cmd == "delete_menu":
        if not contents: 
            send(call.message.chat.id, "⚠️ No content!")
            return
        t = "🗑️ <b>SELECT</b>\n\n"
        for i, item in enumerate(contents, 1): 
            t += f"{i}. {'📝' if item['type']=='text' else '📁'} {item.get('content',item.get('filename',''))[:30]}\n"
        t += "\nNumber (0=cancel):"
        user_states[uid] = "delete_select"
        send_html(call.message.chat.id, t)
    elif cmd == "preview":
        if not contents: 
            send(call.message.chat.id, "👁️ <b>PREVIEW</b>\n\n")
            return
        t = "👁️ <b>PREVIEW</b>\n\n"
        for i, item in enumerate(contents, 1): 
            t += f"{i}. {'📝' if item['type']=='text' else '📁'} {item.get('content',item.get('filename',''))[:50]}\n"
        send_html(call.message.chat.id, t)
    elif cmd == "clear": 
        data["welcome_contents"] = []
        data["pinned_content"] = None
        save_data(data)
        send(call.message.chat.id, "✅ Cleared!")

# 📥 FILE UPLOAD (BYPASSING 20MB LIMIT USING FILE_ID)
@bot.message_handler(content_types=['video', 'photo', 'document', 'voice', 'audio'], func=lambda m: is_admin(m.from_user.id) and user_states.get(m.from_user.id) == "adding_file")
def handle_file_upload(message: types.Message):
    uid = message.from_user.id
    saved = False
    new_item = {"type": "", "content": "", "buttons": []}
    admin_caption = message.caption
    
    try:
        if message.video:
            cap = admin_caption if admin_caption else DEFAULT_CAPTIONS["video"]
            clean_cap, cap_entities = convert_premium_emojis(cap)
            new_item = {"type": "video", "content": message.video.file_id, "is_file_id": True, "caption": clean_cap, "caption_entities": cap_entities, "buttons": []}
            saved = True
        elif message.photo:
            cap = admin_caption if admin_caption else DEFAULT_CAPTIONS["photo"]
            clean_cap, cap_entities = convert_premium_emojis(cap)
            new_item = {"type": "photo", "content": message.photo[-1].file_id, "is_file_id": True, "caption": clean_cap, "caption_entities": cap_entities, "buttons": []}
            saved = True
        elif message.document:
            cap = admin_caption if admin_caption else DEFAULT_CAPTIONS["document"]
            clean_cap, cap_entities = convert_premium_emojis(cap)
            new_item = {"type": "document", "content": message.document.file_id, "is_file_id": True, "filename": message.document.file_name or "file", "caption": clean_cap, "caption_entities": cap_entities, "buttons": []}
            saved = True
        elif message.voice:
            cap = admin_caption if admin_caption else DEFAULT_CAPTIONS["voice"]
            clean_cap, cap_entities = convert_premium_emojis(cap)
            new_item = {"type": "voice", "content": message.voice.file_id, "is_file_id": True, "caption": clean_cap, "caption_entities": cap_entities, "buttons": []}
            saved = True
        elif message.audio:
            cap = admin_caption if admin_caption else DEFAULT_CAPTIONS["audio"]
            clean_cap, cap_entities = convert_premium_emojis(cap)
            new_item = {"type": "audio", "content": message.audio.file_id, "is_file_id": True, "caption": clean_cap, "caption_entities": cap_entities, "buttons": []}
            saved = True
    except Exception as e: 
        logger.error(f"File: {e}")
        
    if saved: 
        data["welcome_contents"].append(new_item)
        save_data(data)
        user_states.pop(uid, None)
        send(message.chat.id, "✅ File saved instantly via file_id (No size limit)! /welcome")
    else: 
        user_states.pop(uid, None)
        send(message.chat.id, "❌ Failed!")

# 🔄 STATES HANDLER
@bot.message_handler(func=lambda m: is_admin(m.from_user.id) and user_states.get(m.from_user.id) in ["adding_text", "adding_button", "edit_select", "delete_select", "pin_select"])
def handle_states(message: types.Message):
    uid = message.from_user.id
    state = user_states.get(uid, "")
    if message.text == '/cancel': 
        user_states.pop(uid, None)
        send(message.chat.id, "❌ Cancelled\n/welcome")
        return
    
    if state == "pin_select":
        try:
            idx = int(message.text.strip()) - 1
            contents = data.get("welcome_contents", [])
            if idx == -1: 
                data["pinned_content"] = None
                save_data(data)
                send(message.chat.id, "✅ Pin removed!")
            elif 0 <= idx < len(contents):
                data["pinned_content"] = idx
                save_data(data)
                prev = contents[idx].get("content", contents[idx].get("filename", ""))[:30]
                send(message.chat.id, f"📌 <b>PINNED!</b>\n\n#{idx+1}: {prev}...")
            else: 
                send(message.chat.id, "❌ Invalid!")
        except: 
            send(message.chat.id, "❌ Number!")
        user_states.pop(uid, None)
    elif state == "adding_text":
        data["welcome_contents"].append({"type": "text", "content": message.text, "buttons": []})
        save_data(data)
        user_states.pop(uid, None)
        send(message.chat.id, "✅ Text added! /welcome")
    elif state == "adding_button":
        lines = message.text.strip().split('\n')
        try: 
            content_idx = int(lines[0].strip()) - 1
        except: 
            send(message.chat.id, "❌ Pehli line: Content Number!\n\n/cancel")
            return
        contents = data.get("welcome_contents", [])
        if content_idx < 0 or content_idx >= len(contents): 
            send(message.chat.id, "❌ Invalid Content Number!\n\n/cancel")
            return
        added = 0
        for line in lines[1:]:
            if '|' in line:
                parts = line.split('|', 1)
                rest = parts[1].strip()
                btn_text = parts[0].strip()
                btn_row = 0
                if '/row:' in rest:
                    up = rest.split('/row:')
                    rest = up[0].strip()
                    try: 
                        btn_row = int(up[1].strip())
                    except: 
                        pass
                if '/style:' in rest:
                    up = rest.split('/style:')
                    btn_url = up[0].strip()
                    c = up[1].strip().lower() if len(up) > 1 else "blue"
                else: 
                    btn_url = rest
                    c = "blue"
                btn_color = COLOR_MAP.get(c, "primary")
                if "buttons" not in contents[content_idx]: 
                    contents[content_idx]["buttons"] = []
                clean_btn_text, icon_emoji_id = extract_button_icon(btn_text)
                contents[content_idx]["buttons"].append({
                    "text": clean_btn_text,
                    "url": btn_url,
                    "color": btn_color,
                    "icon_emoji_id": icon_emoji_id,
                    "row": btn_row
                })
                added += 1
        if added > 0: 
            save_data(data)
            send(message.chat.id, f"✅ {added} buttons added to Content {content_idx+1}!\n/welcome")
        else: 
            send(message.chat.id, "❌ Koi button add nahi hua!\n\n/cancel")
        user_states.pop(uid, None)
    elif state == "edit_select":
        contents = data.get("welcome_contents", [])
        try:
            idx = int(message.text.strip()) - 1
            if 0 <= idx < len(contents): 
                user_states[uid] = f"edit_save_{idx}"
                send(message.chat.id, f"✏️ Edit #{idx+1}:\n/cancel")
            else: 
                user_states.pop(uid, None)
                send(message.chat.id, "❌ Invalid!")
        except: 
            user_states.pop(uid, None)
    elif state.startswith("edit_save_"):
        idx = int(state.split("_")[-1])
        contents = data.get("welcome_contents", [])
        if 0 <= idx < len(contents) and message.text:
            old = contents[idx]
            if not old.get("is_file_id", False) and old["type"] != "text" and os.path.exists(old.get("content", "")): 
                try:
                    os.remove(old["content"])
                except:
                    pass
            contents[idx] = {"type": "text", "content": message.text, "buttons": old.get("buttons", [])}
            save_data(data)
        user_states.pop(uid, None)
        send(message.chat.id, "✅ Updated! /welcome")
    elif state == "delete_select":
        contents = data.get("welcome_contents", [])
        try:
            idx = int(message.text.strip()) - 1
            if idx == -1: 
                send(message.chat.id, "❌ Cancelled")
            elif 0 <= idx < len(contents):
                if data.get("pinned_content") == idx: 
                    data["pinned_content"] = None
                elif data.get("pinned_content") is not None and data["pinned_content"] > idx: 
                    data["pinned_content"] -= 1
                deleted = contents.pop(idx)
                if not deleted.get("is_file_id", False) and deleted["type"] != "text" and os.path.exists(deleted.get("content", "")): 
                    try:
                        os.remove(deleted["content"])
                    except:
                        pass
                save_data(data)
                send(message.chat.id, "✅ Deleted! /welcome")
        except: 
            pass
        user_states.pop(uid, None)

# 📨 USER → ADMIN FORWARDER
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice', 'audio', 'sticker', 'animation'], func=lambda m: not is_admin(m.from_user.id))
def user_to_admin(message: types.Message):
    user = message.from_user
    if user.id not in data["users"]: 
        data["users"].append(user.id)
        save_data(data)
    for aid in ADMIN_IDS:
        try: 
            bot.forward_message(aid, message.chat.id, message.message_id)
        except: 
            pass
    try: 
        send(message.chat.id, "✅ Message sent to admin!")
    except: 
        pass

# 📢 ADMIN BROADCAST
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice', 'audio', 'sticker', 'animation'], func=lambda m: is_admin(m.from_user.id) and not (m.text and m.text.startswith('/')))
def admin_broadcast(message: types.Message):
    users = data.get("users", [])
    if not users: 
        send(message.chat.id, "⚠️ No users!")
        return
    sent = 0
    failed = 0
    blocked_users = []
    is_forwarded = message.forward_from or message.forward_from_chat
    
    for uid in users:
        try:
            if is_forwarded:
                bot.forward_message(uid, message.chat.id, message.message_id)
            else:
                if message.text:
                    send(uid, message.text)
                elif message.photo:
                    cap = message.caption or ""
                    send_media_with_caption(bot.send_photo, uid, message.photo[-1].file_id, cap)
                elif message.video:
                    cap = message.caption or ""
                    send_media_with_caption(bot.send_video, uid, message.video.file_id, cap, supports_streaming=True)
                elif message.document:
                    cap = message.caption or ""
                    send_media_with_caption(bot.send_document, uid, message.document.file_id, cap)
                elif message.voice:
                    cap = message.caption or ""
                    send_media_with_caption(bot.send_voice, uid, message.voice.file_id, cap)
                elif message.audio:
                    cap = message.caption or ""
                    send_media_with_caption(bot.send_audio, uid, message.audio.file_id, cap)
                elif message.sticker:
                    bot.send_sticker(uid, message.sticker.file_id)
                elif message.animation:
                    cap = message.caption or ""
                    send_media_with_caption(bot.send_animation, uid, message.animation.file_id, cap)
            sent += 1
        except Exception as e:
            error_msg = str(e)
            if "Forbidden" in error_msg or "blocked" in error_msg.lower(): 
                blocked_users.append(uid)
            else: 
                logger.error(f"BC {uid}: {e}")
            failed += 1
    
    if blocked_users:
        for buid in blocked_users:
            if buid in data["users"]: 
                data["users"].remove(buid)
        save_data(data)
    
    report = f"✅ Sent: {sent}"
    if failed > 0: 
        report += f"\n❌ Failed: {failed}"
    if blocked_users: 
        report += f"\n🚫 Blocked (removed): {len(blocked_users)}"
    send_html(message.chat.id, report)

# 🌐 RENDER WEB SERVER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active on Render!"

def run_web():
    port = int(os.environ.get("PORT", 8000))
    app.run('0.0.0.0', port=port)

# 🚀 MAIN ENTRYPOINT
def main():
    logger.info("🤖 ALL-IN-ONE BOT STARTING...")
    
    threading.Thread(target=run_web, daemon=True).start()
    
    logger.info(f"💾 Data Path: {DATA_FILE}")
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f: 
                json.load(f)
        except:
            logger.warning("⚠️ Corrupt data.json deleted")
            os.remove(DATA_FILE)
            global data
            data = DEFAULT_DATA.copy()
            save_data(data)
            
    bot_info = bot.get_me()
    logger.info(f"✅ @{bot_info.username}")
    logger.info(f"💎 Premium Emojis: {len(PREMIUM_EMOJI_MAP)} LOADED!")
    logger.info(f"📥 Join Accept: {'ON' if data.get('join_enabled', True) else 'OFF'}")
    logger.info(f"🎯 ALL FEATURES ACTIVE!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    main()
