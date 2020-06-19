import requests
import re 
import os
import logging
import time

def main():
    req = requests.get('https://www.rpg-paradize.com/site-Imagine+Your+Craft-108730')
    out = re.findall(r"Clic Sortant : (\d+)", req.text)[0]
    logging.info("Successfully got current votes : " + out)

    s = requests.Session()

    s.post("https://imagineyourcraft.fr/auth/connexion", data={'_username': os.environ['IYC_USERNAME'], '_password': os.environ['IYC_PASSWORD'], '_remember_me': 'on'}, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0 Safari/537.36"})

    if (s.cookies.get('iycf_user')):
        logging.info("Successfully Logged to IYC")
        req = s.post("https://imagineyourcraft.fr/vote/rpc/" + os.environ['IYC_USERNAME'] +"/keypad", headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0 Safari/537.36"})
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        mapping = {}
        for pos in range(0, len(req.json())) :
            mapping[req.json()[pos]] = letters[pos]
        logging.info("Successfully mapped keypad values")
        code = ""
        for letter in out:
            code += mapping[letter]
        logging.info("Current mapped code is : " + code)
        req = s.post("https://imagineyourcraft.fr/vote/rpc/" + os.environ['IYC_USERNAME'], data={'voteNb': code},headers={'Referer':"https://imagineyourcraft.fr/vote", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0 Safari/537.36"})
        if ('success' in req.json() and req.json()['success']):
            logging.info("You just earned " + str(req.json()['add']) + " points, total : " + str(req.json()['total']))
            delay = 60 * 60 * 3 + 60 * 1
        else:
            logging.error("Vote error : " + (req.json()['error'] if 'success' in req.json() else req.text))
            if ('error' in req.json() and re.search(r"Merci de patienter (\d+) minute\(?s\)? avant d'essayer de nouveau\.", req.json()['error'])):
                delay = (int(re.findall(r"Merci de patienter (\d+) minute\(?s\)? avant d'essayer de nouveau\.", req.json()['error'])[0]) + 1) * 60
            else:
                delay = 60 * 60 * 3 + 60 * 1

        req = s.get("https://imagineyourcraft.fr/auth/deconnection", headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0 Safari/537.36"})
        req = s.get(req.url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0 Safari/537.36", 'Connection':'close'})
        req.close()
        s.close()
        logging.info("Successfully disconnected from IYC Account, " + str(int(delay / 60)) + " minutes before next vote.")
        return delay
    else:
        logging.error("Could not login to IYC, quiting now")
        return 0


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/cron/vote.log', level=logging.INFO, format='%(asctime)s IYC Vote %(levelname)s: %(message)s')
    while True:
        delay = main()
        if(delay == 0):
            break
        else:
            time.sleep(delay)
            
