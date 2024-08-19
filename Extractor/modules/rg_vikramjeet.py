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


async def rgvikram_down(app, message, hdr1, api, raw_text2, fuk, batch_name, name, prog):
    vt = ""
    try:
        xx = fuk.split('&')
        for f in xx:
            res3 = requests.get(f"https://{api}/get/alltopicfrmlivecourseclass?courseid=" + raw_text2 + "&subjectid=" + f + "&start=-1", headers=hdr1)
            b_data2 = res3.json().get('data', [])
            vp = ""
            for data in b_data2:
                tid = data.get("topicid")
                if tid:
                    vp += f"{tid}&"

            vj = ""
            try:
                xv = vp.split('&')
                for y in range(len(xv)):
                    t = xv[y]
                    res4 = requests.get(f"https://{api}/get/livecourseclassbycoursesubtopconceptapiv3?courseid=" + raw_text2 + "&subjectid=" + f + "&topicid=" + t + "&conceptid=1&start=-1", headers=hdr1).json()
                    topicid1 = res4.get("data", [])
                    for data in topicid1:
                        type = data.get('material_type')
                        tid = data.get("Title")
                        if type == 'VIDEO':

                            if data.get('ytFlag') == 0:
                                dlink = next((link['path'] for link in data.get('download_links', []) if link.get('quality') == "720p"), None)
                                if dlink:
                                    parts = dlink.split(':')
                                    if len(parts) == 2:   
                                        encoded_part, encrypted_part = parts
                                        b = decrypt_data(encoded_part)
                                        cool2 = f"{b}"
                                    else:
                                        print(f"Unexpected format: {plink}\n{tid}")

                            elif data.get('ytFlag') == 1:
                                dlink = data.get('file_link')
                                if dlink:
                                    encoded_part, encrypted_part = dlink.split(':')
                                    b = decrypt_data(encoded_part)
                                    cool2 = f"{b}"
                                else:
                                    print(f"Missing video_id for {tid}")
                            else:
                                print("Unknown ytFlag value")
                            msg = f"{tid} : {cool2}\n"
                            vj += msg

                        elif type == 'PDF':
                            plink = data.get("pdf_link", "").split(':')
                            if len(plink) == 2:
                                encoded_part, encrypted_part = plink
                                bp = decrypt_data(encoded_part)
                                vs = f"{bp}"
                                msg = f"{tid} : {vs}\n"
                                vj += msg
                    res5 = requests.get(f"https://{api}/get/livecourseclassbycoursesubtopconceptapiv3?courseid=" + raw_text2 + "&subjectid=" + f + "&topicid=" + t + "&conceptid=2&start=-1", headers=hdr1).json()
                    topicid2 = res5.get("data", [])
                    for data in topicid2:
                        type = data.get('material_type')
                        tid = data.get("Title")
                        if type == 'VIDEO':

                            if data.get('ytFlag') == 0:
                                dlink = next((link['path'] for link in data.get('download_links', []) if link.get('quality') == "720p"), None)
                                if dlink:
                                    parts = dlink.split(':')
                                    if len(parts) == 2:   
                                        encoded_part, encrypted_part = parts
                                        b = decrypt_data(encoded_part)
                                        cool2 = f"{b}"
                                    else:
                                        print(f"Unexpected format: {plink}\n{tid}")

                            elif data.get('ytFlag') == 1:
                                dlink = data.get('file_link')
                                if dlink:
                                    encoded_part, encrypted_part = dlink.split(':')
                                    b = decrypt_data(encoded_part)
                                    cool2 = f"{b}"
                                else:
                                    print(f"Missing video_id for {tid}")
                            else:
                                print("Unknown ytFlag value
