import asyncio
import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Parser:
    async def drive_auth(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("mycreds.txt")
        return gauth

    async def drive_setup(self, file_id):
        gauth = await self.drive_auth()
        gfile = GoogleDrive(gauth).CreateFile({'id': file_id})
        gfile.GetContentFile('response_a.json')
        return gfile

    async def download_file(self, file_id):
        gfile = await self.drive_setup(file_id)
        return json.loads(gfile.content.read().decode('utf-8'))

    async def parse_a(self, file_id):
        await asyncio.sleep(30)
        return await self.download_file(file_id)
