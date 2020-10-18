#!/usr/bin/python
import asyncio
import os
import sys
import pytesseract
from classes.scraper import Scraper
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# If you don't have tesseract executable in your PATH, include the following:
from security import Authorizer, Messenger


class Archiver(Scraper):
    def __init__(self):
        self.configfile = os.getcwd() + f"/src/security/config"
        self.keyfile = os.getcwd() + f"/src/security/private_key.pem"
        self.security_manager = Authorizer()
        self.key_service = Messenger()
        self.key_service.init(configfile=self.configfile, keyfile=self.keyfile)
        self.server = self.key_service.config['cloud.mongodb']
        self.command = sys.argv
        self.watson_nlu = ""
        self.nlu_authenticator = ""
        pytesseract.pytesseract.tesseract_cmd = os.environ['TESSERACT_PATH']
        self.init()

    def init(self):
        # watson image visualizer
        #
        # watson nlu
        self.nlu_authenticator = IAMAuthenticator(self.key_service.config['watson']['watson_nlu_key'])
        self.watson_nlu = NaturalLanguageUnderstandingV1(
            version='2020-08-01',
            authenticator=self.nlu_authenticator
        )
        self.watson_nlu.set_service_url(self.key_service.config['watson']['watson_nlu_url'])


async def main():
    print("Archiver")


if __name__ == "__main__":
    # loop to keep main thread running
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
