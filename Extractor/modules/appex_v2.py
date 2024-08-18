import json
import os
import requests
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from pyrogram import filters
from Extractor import app


def decrypt_data(encoded_data):
    try:
        key = "638udh3829162018".encode("utf8")
        iv = "fedcba9876543210".encode("utf8")
        decoded_data = b64decode(encoded_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error decrypting data: {str(e)}")


async def course_content(app, api, message, raw_text2, batch_name, name, parent_Id, hdr1):
    try:
        scraper = cloudscraper.create_scraper()
        html = scraper.get(f"https://{api}/get/folder_contentsv2?course_id={raw_text2}&parent_id={parent_Id}", headers=hdr1).content
        output = json.loads(html)
        data_list = output.get('data', [])
        vj = ""
        for data in data_list:
            try:
                if data['material_type'] == 'FOLDER':
                    id = data["id"]
                    await course_content(app, api, message, raw_text2, id, hdr1)
                elif data['material_type'] == 'VIDEO':
                    tid = data.get("Title")
                    download_links = data.get('download_links', [])
                    for link in download_links:
                        if link.get('quality') == "720p":
                            dlink = link.get('path')
                            if dlink:
                                parts = dlink.split(':')
                                if len(parts) == 2:
                                    encoded_part, encrypted_part = parts
                                    cool2 = decrypt_data(encoded_part)
                                    msg = f"{tid} : {cool2}\n"
                                    vj += msg
                            else:
                                print(f"Unexpected format: {dlink}\n{tid}")
                    pdf_link = data.get("pdf_link", "").split(':')
                    if len(pdf_link) == 2:
                        encoded_part, encrypted_part = pdf_link
                        vs = decrypt_data(encoded_part)
                        msg = f"{tid} : {vs}\n"
                        vj += msg
                elif data['material_type'] == 'PDF':
                    tid = data.get("Title")
                    pdf_link = data.get("pdf_link", "").split(':')
                    if len(pdf_link) == 2:
                        encoded_part, encrypted_part = pdf_link
                        vs = decrypt_data(encoded_part)
                        msg = f"{tid} : {vs}\n"
                        vj += msg
            except Exception as e:
                print(f"Error processing data: {str(e)}")
                
        mm = f"{batch_name}"
        cap = f"**App Name :- {name}\nBatch Name :-** `{batch_name}`"
        with open(f'{mm}.txt', 'a') as f:
            f.write(f"{vj}")
        await app.send_document(message.chat.id, document=f"{mm}.txt", caption=cap)
        file_path = f"{mm}.txt"
        os.remove(file_path)
        await message.reply_text("Done")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.reply_text("An error occurred. Please try again later.")
