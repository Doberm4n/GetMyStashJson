#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import psutil
import json
from selenium import webdriver
import time
import stash_values


version = '0.9.0'
link = 'https://github.com/Doberm4n/GetMyStashJson'

class getStash():

    def getStashJson(self, league, accountName, delay, driverPath, profilePath):
        if not verify():
            return
        if self.checkChromeIsRunning():
            return

        try:
            print '\nRunning Chrome browser...'

            options = webdriver.ChromeOptions()
            options.add_argument('user-data-dir=' + profilePath) #Path to your chrome profile
            driver = webdriver.Chrome(executable_path=driverPath, chrome_options=options)

            print "\nDelay: " + str(delay) + ' sec'
            time.sleep(5)

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

            driver.quit()

        except Exception, e:
                print "Error: " + str(e)
        except KeyboardInterrupt:
            print 'Exit... (Keyboard Interrupt)'
            driver.quit()
            pass

    def writeJson(self, dump, league, stashNumber):
        try:
            with open(str(stashNumber + 1) + '_' + str(league) +'.json', 'w') as outfile:
                print 'Writing json file: ' + str(stashNumber + 1) + '_' + str(league) + '.json'
                json.dump(dump, outfile)
                print 'Saved: ' + str(stashNumber + 1) + '_' + str(league) + '.json\n'
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
    try:
        opts, args = getopt.getopt(argv,"l:a:d:",["league", "accountName", "delay"])
    except getopt.GetoptError:
       print 'Usage: -l <league> -a <account name> -d <delay>(default: 5sec)'
       sys.exit(2)
    for opt, arg in opts:
      if opt in ("-l", "--league"):
         league = str(arg)
      elif opt in ("-a", "--accountName"):
         accountName = str(arg)
      elif opt in ("-d", "--delay"):
         delay = int(arg)

    if not league:
        print '\nLeague not specified'
        print '\nUsage: -l <league> -a <account name> -d <delay>(default: 5sec)'
        sys.exit(2)
    if not accountName:
        print '\nAccount name not specified'
        print '\nUsage: -l <league> -a <account name> -d <delay>(default: 5sec)'
        sys.exit(2)

    config = loadConfig()

    if config:
        getStashInstance = getStash()
        getStashInstance.getStashJson(league, accountName, delay, config['chromedriver_path'], config['user_profile_path'])

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

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Exit... (Keyboard Interrupt)'
        sys.exit(2)
