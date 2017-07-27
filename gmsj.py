#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import psutil
import json
from selenium import webdriver
import time
import stash_values

version = '0.9.0'
link = 'https://github.com/Doberm4n/POEStashJsonViewer'

def getStash(league, accountName, delay, driverPath, profilePath):
    if not verify():
        return
    if checkChromeIsRunning():
        return

    #return

    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + profilePath) #Path to your chrome profile
    driver = webdriver.Chrome(executable_path=driverPath, chrome_options=options)

    #open first tab json
    url = stash_values.urlStashIndex[0] + str(0) + stash_values.urlStashIndex[1] +str(league) + stash_values.urlStashIndex[2] + str(accountName)
    print 'Opening url: ' + url
    driver.get(url)
    pre = driver.find_element_by_tag_name("pre").text
    data = json.loads(pre)
    stashCount = data['numTabs']
    print 'Stash tabs count: ' + str(stashCount) + '\n'
    writeJson(data, league, 0)

    #open next tab jsons
    for i in range(stashCount):
        url = stash_values.urlStashIndex[0] + str(i) + stash_values.urlStashIndex[1] + str(league) + stash_values.urlStashIndex[2] + str(accountName)
        print "Delay: " + str(delay) + ' sec'
        time.sleep(delay)
        print 'Processing tab: ' + str(i)
        print 'Opening url: ' + url
        driver.get(url)
        pre = driver.find_element_by_tag_name("pre").text
        data = json.loads(pre)
        #stashCount = data['numTabs']
        writeJson(data, league, i)

    driver.quit()

def writeJson(dump, league, stashNumber):
    try:
        with open(str(stashNumber + 1) + '_' + str(league) +'.json', 'w') as outfile:
            print 'Writing json file: ' + str(stashNumber + 1) + '_' + str(league) + '.json'
            json.dump(dump, outfile)
            print 'Saved: ' + str(stashNumber + 1) + '_' + str(league) + '.json\n'
    except Exception, e:
            print "Error: " + str(e)

def checkChromeIsRunning():
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == "chrome.exe":
            print '\nPlease close Chrome browser before running this app'
            return True


def main(argv):
    print '\nGetMyStashJson for PoE'
    print 'version: ' + str(version)
    print '(' + link + ')'
    try:
        opts, args = getopt.getopt(argv,"l:a:d:",["league", "accountName", "delay"])
    except getopt.GetoptError:
       print 'Usage: -l <league> -a <account name> -d <delay>'
       sys.exit(2)
    for opt, arg in opts:
      if opt in ("-l", "--league"):
         league = str(arg)
      elif opt in ("-a", "--accountName"):
         accountName = str(arg)
      elif opt in ("-d", "--delay"):
         delay = int(arg)

    config = loadConfig()

    if config:
        getStash(league, accountName, delay, config['chromedriver_path'], config['user_profile_path'])

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
   main(sys.argv[1:])
