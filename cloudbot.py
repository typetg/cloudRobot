import pyrogram, requests
from datetime import datetime
from pyrogram import Client
import configparser as ConfigParser
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3 as sl
app = Client("cloudrobot")
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

#Variables
db_channel = int(Config['vars']['db_channel'])
db_channel_without = str(db_channel)
db_channel_without = str(db_channel_without[4:])
con = sl.connect('cloud.db', check_same_thread=False)
cur = con.cursor()
admin_list = Config['vars']['admins'].split(" ")
admins_l = []
for a in admin_list:
	admins_l.append(int(a))
app.start()
db_chat = app.get_chat(chat_id=db_channel)
link_ = db_chat['invite_link']
app.stop()
start_text='''Welcome to your Telegram cloudRobot 🌩️

Just create a folder with "/addfolder NAME" and then send me files to upload and save. Currently you can save the following formats:

📷 Photos

🎬 Videos

🎤 Voice messages

🎧 Music

🏳️ Stickers

🔤 Text

🔁 Other formats(like pdf, exe or apk)'''
#Keyboards

#A list that appears when uploading a file, to select which folder it should go to
def folder_list_input(app, message_id):
	sql = "SELECT * FROM folder"
	cur.execute(sql)
	folder = cur.fetchall()
	con.commit()
	keyboard = []
	for fo in folder:
		keyboard = keyboard + [[InlineKeyboardButton(str(fo[1])+" 📁", callback_data="folder_input#"+str(fo[0])+"#"+str(message_id),)]]
	return InlineKeyboardMarkup(keyboard)

#Lists all folders as a list
def show_folder(app):
	sql = "SELECT * FROM folder"
	cur.execute(sql)
	folder = cur.fetchall()
	con.commit()
	keyboard = []
	for fo in folder:
		keyboard = keyboard + [[InlineKeyboardButton(str(fo[1])+" 📂", callback_data="show_folder#"+str(fo[0]),)]]
	keyboard = keyboard + [[InlineKeyboardButton("🔙 Back", callback_data="start_screen",),InlineKeyboardButton("❌ Close", callback_data="close",)]]
	return InlineKeyboardMarkup(keyboard)

#Lists all folders as a list
def show_files(app, folder_id):
	sql = "SELECT * FROM TG_index WHERE folder='"+folder_id+"'"
	cur.execute(sql)
	images = cur.fetchall()
	con.commit()
	keyboard = []
	for img in images:
		keyboard = keyboard + [[InlineKeyboardButton(str(img[2])+" ", callback_data="select_file#"+str(img[1]),)]]
	keyboard = keyboard + [[InlineKeyboardButton("❌ Close", callback_data="close",),InlineKeyboardButton("📁 all folders", callback_data="lister",)]]
	return InlineKeyboardMarkup(keyboard)

#Menu after calling a file
def select_menu(app, message_id):
	sql = "SELECT * FROM TG_index WHERE message_id="+str(message_id)
	cur.execute(sql)
	file = cur.fetchone()
	sql = "SELECT * FROM folder WHERE id="+file[3]
	cur.execute(sql)
	folder = cur.fetchone()
	con.commit()
	keyboard = []
	keyboard = keyboard + [[InlineKeyboardButton("📥 Get File 📥", callback_data="get_file#"+str(message_id),)]]
	keyboard = keyboard + [[InlineKeyboardButton("👀 View in Database 👀", url="https://t.me/c/"+str(db_channel_without)+"/"+str(message_id),)]]
	keyboard = keyboard + [[InlineKeyboardButton("🗑️ Delete 🗑️", callback_data="delete_file#"+str(message_id),)]]
	keyboard = keyboard + [[InlineKeyboardButton("❌ Close", callback_data="close",),InlineKeyboardButton(str("📁 "+folder[1]), callback_data="show_folder#"+str(folder[0])),InlineKeyboardButton("📁 all folders", callback_data="lister",)]]
	return InlineKeyboardMarkup(keyboard)

#Start-Board
def start_board(app):
	global link_
	keyboard = [[InlineKeyboardButton("📁 Show all folders", callback_data="lister",)], [InlineKeyboardButton("🗂️ Database Channel", url=link_,)],[InlineKeyboardButton("🔗 Bot creator", url="t.me/typeBots"),InlineKeyboardButton("️📝 Repo", url="https://github.com/typetg/cloudRobot"]]
	return InlineKeyboardMarkup(keyboard)


#Keyboard after delete file

def delete_board(app):
	keyboard = [[InlineKeyboardButton("🏠 Start", callback_data="start_screen"),InlineKeyboardButton("📁 Show all folders", callback_data="lister",)]]
	return InlineKeyboardMarkup(keyboard)

#Repo Link

def no_access(app, message):
	keyboard = [[InlineKeyboardButton("Start your own Telegram cloud Robot🌩️", url="https://github.com/typetg/cloudRobot")]]
	app.send_message(chat_id=message.chat.id, text="**Sorry this is not your Telegram Cloud Bot.**", reply_markup=InlineKeyboardMarkup(keyboard))


#Callback-Handler

@app.on_callback_query()
def my_handler(app, callback_query):
	global admins_l
	if callback_query.from_user.id in admins_l:
		if "folder_input#" in callback_query.data:
			data = callback_query.data.split("#")
			folder_id = data[1]
			message_id = data[2]
			sql = "SELECT * FROM folder WHERE id="+str(folder_id)
			cur.execute(sql)
			folder_name = cur.fetchone()
			con.commit()
			sql = "UPDATE TG_index set folder="+str(folder_id)+" WHERE message_id="+str(message_id)
			cur.execute(sql)
			con.commit()
			app.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message["message_id"], text="Sucessfully uploaded to your Cloud ☁️", reply_markup=None)
		elif "lister" in callback_query.data:
			app.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message["message_id"], text="Choose a folder:", reply_markup=show_folder(app))
		elif "show_folder#" in callback_query.data:
			data = callback_query.data.split("#")
			app.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message["message_id"], text="All saved Files:", reply_markup=show_files(app, data[1]))
		elif "select_file#" in callback_query.data:
			data = callback_query.data.split("#")
			sql = "SELECT * FROM TG_index WHERE message_id="+data[1]
			cur.execute(sql)
			file = cur.fetchone()
			link = "https://t.me/c/"+str(db_channel_without)+"/"+str(file[1])
			rename = "/rename "+str(file[1])+";NEW TITEL"
			message_text = "**💬 Titel**: `"+str(file[2])+"`\n\n**📅 Upload date:** `"+str(file[4])+"`\n\n**🔗 Link**: `"+link+"`\n\n**🖊️ Rename**: `"+rename+"`"
			app.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message["message_id"], text=message_text, reply_markup=select_menu(app, data[1]))
		elif "get_file#" in callback_query.data:
			data = callback_query.data.split("#")
			message_id = int(data[1])
			app.forward_messages(chat_id=callback_query.from_user.id ,from_chat_id=db_channel, message_ids=message_id)
		elif "close" in callback_query.data:
			app.delete_messages(chat_id=callback_query.from_user.id, message_ids=callback_query.message["message_id"])
		elif "delete_file#" in callback_query.data:
			data = callback_query.data.split("#")
			app.delete_messages(chat_id=db_channel, message_ids=int(data[1]))
			sql = "DELETE FROM TG_index WHERE message_id="+data[1]
			cur.execute(sql)
			con.commit()
			app.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message["message_id"], text="**🗑️ The file was successfully deleted from your database**", reply_markup=delete_board(app))
		elif callback_query.data == "start_screen":
			app.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message["message_id"], text=start_text, reply_markup=start_board(app))


#Command-Handler

@app.on_message(filters.command("addfolder"))
def my_handler(app, message):
	global admins_l
	if message.chat.id in admins_l:
		text = message.text
		text = text.split("/addfolder ")
		app.send_message(chat_id=message.chat.id, text="⭐ The folder called: '"+text[1]+"' was created! ⭐")
		sql = "INSERT INTO folder(folder) VALUES(?)"
		data = (text[1],)
		with con:
			cur.execute(sql, data)
	else:
		no_access(app, message)

@app.on_message(filters.command("start"))
def my_handler(app, message):
	global admins_l
	if message.chat.id in admins_l:
		app.send_message(chat_id=message.chat.id, text=start_text, reply_markup=start_board(app))
	else:
		no_access(app, message)

@app.on_message(filters.command("rename"))
def my_handler(app, message):
	global admins_l
	if message.chat.id in admins_l:
		text = message.text
		text = text.split("/rename ")
		select = text[1].split(";")
		sql = "UPDATE TG_index set titel='"+str(select[1])+"' WHERE message_id="+str(select[0])
		cur.execute(sql)
		con.commit()
		text = "🖊️ **The title of the file was successfully changed to**: "+select[1]
		rename_keyboard = []
		rename_keyboard = rename_keyboard + [[InlineKeyboardButton("🔙 back to file", callback_data="select_file#"+str(select[0]),),InlineKeyboardButton("📁 all folders", callback_data="lister",)]]
		app.send_message(chat_id=message.chat.id, text=text, reply_markup=InlineKeyboardMarkup(rename_keyboard))
	else:
		no_access(app, message)

#Media-Handler

@app.on_message(filters.media | filters.text)
def my_handler(app, message):
	global admins_l
	if message.chat.id in admins_l:
		text = message.text
		db_data = app.forward_messages(
	chat_id=db_channel,
	from_chat_id=message.chat.id,
	message_ids=message.message_id

	)
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		caption = db_data.caption
		if caption == None:
			caption = "File from: "+str(date_time)
		message_id = db_data.message_id
		sql = "INSERT INTO TG_index(message_id, titel, upload_date) VALUES(?, ?, ?)"
		data = (str(message_id), caption, str(date_time))
		with con:
			cur.execute(sql, data)
		app.send_message(chat_id=message.chat.id, text="Choose a folder for ur file:", reply_markup=folder_list_input(app, message_id))
	else:
		no_access(app, message)
app.run()
