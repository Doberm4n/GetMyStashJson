#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import psutil
import json
from selenium import webdriver
import time
import stash_values


version = '0.9.1'
link = 'https://github.com/Doberm4n/GetMyStashJson'

class getStash():

    def getStashJson(self, league, accountName, character, delay, driverPath, profilePath, indexRange):
        driver = None

        if not verify():
            return
        if self.checkChromeIsRunning():
            if query_yes_no("\nClose now?"):
                os.system("taskkill /im chrome.exe /f >nul 2>&1")
                print "\nComplete"
            else:
                print "\nExit"
                return

        try:
            print '\nRunning Chrome browser...'

            options = webdriver.ChromeOptions()
            options.add_argument('user-data-dir=' + profilePath) #Path to your chrome profile
            driver = webdriver.Chrome(executable_path=driverPath, chrome_options=options)

            print '\nPlease do not interact with browser tab, where JSON data is loading'

            print "\nDelay: " + str(delay) + ' sec'
            time.sleep(5)

            if character:
                url = stash_values.urlCharacter[0] + str(character) + stash_values.urlCharacter[1] + str(accountName)
                print 'Opening url: ' + url
                driver.get(url)
                pre = driver.find_element_by_tag_name("pre").text
                data = json.loads(pre)
                self.writeJson(data, character, 0)
                driver.quit()
                print "\nComplete"
                return

            if indexRange:
                indexRange = indexRange.replace('[', '').replace(']', '').split(',')
                for i in range(len(indexRange)):
                    if '-' in indexRange[i]:
                        temp = indexRange[i].split('-')
                        for j in range(int(temp[0]), int(temp[1]) + 1):
                            url = stash_values.urlStashIndex[0] + str(j) + stash_values.urlStashIndex[1] +str(league) + stash_values.urlStashIndex[2] + str(accountName)
                            print 'Opening url: ' + url
                            driver.get(url)
                            pre = driver.find_element_by_tag_name("pre").text
                            data = json.loads(pre)
                            self.writeJson(data, league, j-1)
                            print "Delay: " + str(delay) + ' sec'
                            time.sleep(delay)
                    else:
                        url = stash_values.urlStashIndex[0] + str(int(indexRange[i])) + stash_values.urlStashIndex[1] +str(league) + stash_values.urlStashIndex[2] + str(accountName)
                        print 'Opening url: ' + url
                        driver.get(url)
                        pre = driver.find_element_by_tag_name("pre").text
                        data = json.loads(pre)
                        self.writeJson(data, league, int(indexRange[i])-1)
                        print "Delay: " + str(delay) + ' sec'
                        time.sleep(delay)
                driver.quit()
                print "\nComplete"
                return

            #open first tab json
            url = stash_values.urlStashIndex[0] + str(0) + stash_values.urlStashIndex[1] +str(league) + stash_values.urlStashIndex[2] + str(accountName)
            print 'Opening url: ' + url
            driver.get(url)
            pre = driver.find_element_by_tag_name("pre").text
            data = json.loads(pre)
            stashCount = data['numTabs']
            print 'Stash tabs count: ' + str(stashCount) + '\n'
            self.writeJson(data, league, 0)

            #open next tab jsons
            for i in range(1, stashCount):
                url = stash_values.urlStashIndex[0] + str(i) + stash_values.urlStashIndex[1] + str(league) + stash_values.urlStashIndex[2] + str(accountName)
                print "Delay: " + str(delay) + ' sec'
                time.sleep(delay)
                print 'Processing tab: ' + str(i+1)
                print 'Opening url: ' + url
                driver.get(url)
                pre = driver.find_element_by_tag_name("pre").text
                data = json.loads(pre)
                self.writeJson(data, league, i)
            print "\nComplete"
            driver.quit()

        except Exception, e:
                print "Error: " + str(e)
        except KeyboardInterrupt:
            print 'Exit... (Keyboard Interrupt)'
            if driver: driver.quit()
            pass

    def writeJson(self, dump, name, stashNumber):
        try:
            with open('outputJson\\' + str(stashNumber + 1) + '_' + str(name) +'.json', 'w') as outfile:
                print 'Writing json file: ' + str(stashNumber + 1) + '_' + str(name) + '.json'
                json.dump(dump, outfile)
                print 'Saved: ' + str(stashNumber + 1) + '_' + str(name) + '.json\n'
        except Exception, e:
                print "Error: " + str(e)

    def checkChromeIsRunning(self):
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "chrome.exe":
                print '\nPlease close Chrome browser before running this app'
                return True


def main(argv):
    print '\nGetMyStashJson for PoE'
    print 'version: ' + str(version)
    print '(' + link + ')'
    delay = 5
    league = None
    accountName = None
    character = None
    indexRange = None
    try:
        opts, args = getopt.getopt(argv,"c:l:a:d:r:",["character", "league", "accountName", "delay", "indexRange"])
    except getopt.GetoptError:
       print 'Usage: -l <league> -a <account name> -d <delay>(default: 5sec) optional -c <character> -r <index range or specific index/indexes> (example: -r "[1-5, 7, 1]")'
       sys.exit(2)
    for opt, arg in opts:
      if opt in ("-l", "--league"):
         league = str(arg)
      elif opt in ("-a", "--accountName"):
         accountName = str(arg)
      elif opt in ("-d", "--delay"):
         delay = int(arg)
      elif opt in ("-c", "--character"):
         character = str(arg)
      elif opt in ("-r", "--indexRange"):
         indexRange = str(arg)

    if not league and not character:
        print '\nLeague not specified'
        print '\nUsage: -l <league> -a <account name> -d <delay>(default: 5sec) optional -c <character> -r <index range or specific index/indexes> (example: -r "[1-5, 7, 1]")'
        sys.exit(2)
    if not accountName and not character:
        print '\nAccount name not specified'
        print '\nUsage: -l <league> -a <account name> -d <delay>(default: 5sec) optional -c <character> -r <index range or specific index/indexes> (example: -r "[1-5, 7, 1]")'
        sys.exit(2)

    config = loadConfig()

    if config:
        getStashInstance = getStash()
        getStashInstance.getStashJson(league, accountName, character, delay, config['chromedriver_path'], config['user_profile_path'], indexRange)

def loadConfig():
    try:
        with open('Config\getMyStashJsonConfig.json') as data_file:
            return json.load(data_file)
    except Exception, e:
        print "\nError: " + str(e)
        print 'Please check config file'

def verify():
  print '\nChecking config...'
  data = loadConfig()
  res = True
  if data:
    if not data['chromedriver_path'] or not os.path.isfile(data['chromedriver_path']):
        print 'Wrong chromedriver_path'
        res = False
    else:
        print 'chromedriver_path defined'
    if not data['user_profile_path'] or not os.path.isdir(data['user_profile_path']):
        print 'Wrong user_profile_path'
        res = False
    else:
        print 'user_profile_path defined'
    return res

def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Exit... (Keyboard Interrupt)'
        sys.exit(2)
