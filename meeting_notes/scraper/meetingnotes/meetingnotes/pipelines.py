# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, hashlib, requests
from pathlib import Path

from meetingnotes import get_id_from_google_drive_url, download_google_drive_file


class MeetingnotesPipeline(object):
    def process_item(self, item, spider):
        url_hash = hashlib.md5(item['link'].encode("utf8")).hexdigest()

        # Make ward dir
        ward_path = os.path.join('notesfiles', item['ward'])
        os.makedirs(ward_path, exist_ok=True)

        file_path = os.path.join(ward_path, f"{url_hash}.pdf")

        # Google Drive only
        google_id = get_id_from_google_drive_url(item['link'])
        resp = download_google_drive_file(google_id)

        # Write
        Path(file_path).write_bytes(download_google_drive_file(google_id).content)
        
        # with open(file_path, "wb+") as f:
        #     resp = 
        #     f.write(resp.content)

        item['file_dl_path'] = file_path
        return item
