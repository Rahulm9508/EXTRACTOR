import json
import os
import requests
import threading
import asyncio
from pyrogram import filters
from pyrogram.types import Message
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import config
from Extractor import app

def decrypt_data(encoded_data):
    key = "638udh3829162018".encode("utf8")
    iv = "fedcba9876543210".encode("utf8")
    decoded_data = b64decode(encoded_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
    return decrypted_data.decode('utf-8')

async def appex_down(app, message, hdr1, api, raw_text2, fuk, batch_name, name, prog):
    try:
        xx = fuk.split('&')
        tasks = []
        for v in range(len(xx)):
            f = xx[v]
            task = asyncio.create_task(extract_links(hdr1, api, raw_text2, f))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        vt = ""
        for result in results:
            vt += result
        
        mm = batch_name
        cap = f"**App Name :- {name}\nBatch Name :-** `{batch_name}`"
        with open(f'{mm}.txt', 'a') as f:
            f.write(f"{vt}")
        await app.send_document(message.chat.id, document=f"{mm}.txt", caption=cap)
        await prog.delete()
        file_path = f"{mm}.txt"
        os.remove(file_path)
        await message.reply_text("Done")
    except Exception as e:
        print(str(e))
        await message.reply_text("An error occurred. Please try again later.")

async def extract_links(hdr1, api, raw_text2, f):
    try:
        res3 = requests.get(f"https://{api}/get/alltopicfrmlivecourseclass?courseid=" + raw_text2 + "&subjectid=" + f, headers=hdr1)
        b_data2 = res3.json().get('data', [])
        vp = ""
        for data in b_data2:
            tid = data.get("topicid")
            if tid:
                vp += f"{tid}&"
        
        vj = ""
        xv = vp.split('&')
        for y in range(len(xv)):
            t = xv[y]
            res4 = requests.get(f"https://{api}/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + t + "&start=-1&courseid=" + raw_text2 + "&subjectid=" + f, headers=hdr1).json()
            topicid = res4.get("data", [])
            for data in topicid:
                type = data.get('material_type')
                tid = data.get("Title")
                if type == 'VIDEO':
                    # ...
                    vj += msg
        
        return vj
    except Exception as e:
        print(str(e))
        return ""
