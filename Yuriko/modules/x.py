from Yuriko import (
    DEV_USERS,
    EVENT_LOGS,
    OWNER_ID,
    STRICT_GBAN,
    DRAGONS,
    SUPPORT_CHAT,
    SPAMWATCH_SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    sw,
    dispatcher,
)
from pyrogram import filters
from Yuriko.services.telethon import tbot as pbot
from Yuriko.services.PyMongo import mongoPY as db
from telethon import events

gban = {}
rgban = {}
gban_users = db.gbanusers

def create_gban(user, reason):
    gban_users.update_one(
            {"user_id":user},
            {
                "$set": {
                    "reason": reason
                }
            },
            upsert=True,
        )

@pbot.on(events.NewMessage(incoming=True, pattern="/gban (.*)"))
async def gban(message):
	reply_to_message = await message.get_reply_message()
	if not message.sender_id in OPERATORS:
		return
	if message.reply_to_message:
		user = message.reply_to_message.from_id.user_id
		reason = message.text.split(" ")[1]
	else:
		args = message.text.split(" ", 2)
		user = args[1]
		reason = args[2]

	if not user or not reason:
		await message.reply("You didn't give the one of the Required Parameters, User ID and Reason")
		return

	see_user = await message.client.get_entity(user)
	user_id = see_user.id
	create_gban(user_id, reason)
	MSG_GBAN = f"""
**New Global Ban**
Admin: {message.from_user.mention} [`{message.from_user.id}`]
User: {see_user.mention} [`{see_user.id}`]
Reason: {reason}
"""
	await client.send_message(OWNER_ID, MSG_GBAN)
	await message.reply(MSG_GBAN)

	gban_keyboard = InlineKeyboardMarkup(
		[
			[
				InlineKeyboardButton(
					text="✅αρρяσνє",
					callback_data=f"gban_approve_{user_id}_{reason}"
				)
			],
			[
				InlineKeyboardButton(
					text="❌∂є¢ℓιηє",
					callback_data="gban_decline"
				)
			]
		]
	)
	try:
		await pbot.send_message(chat_id=OWNER_ID, text=gban_approval, parse_mode="html", reply_markup=gban_keyboard)
	except:
		pass
	return
	
	gban[user_id] = True
	rgban[user_id] = message.text.split(reason)
