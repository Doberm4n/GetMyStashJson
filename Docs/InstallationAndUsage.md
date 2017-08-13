## Installation and usage (Windows):

1. Install Python 2.7 (https://www.python.org/downloads/);

2. Install psutil library (https://pythonhosted.org/psutil/):
```
pip install psutil
```

3. Install Python language bindings for Selenium WebDriver (https://pypi.python.org/pypi/selenium):
```
pip install -U selenium
```

4. Download ChromeDriver - WebDriver for Chrome (https://sites.google.com/a/chromium.org/chromedriver/downloads) .zip archive and unpack .exe from archive;

5. Download and unpack sources from this repository;

6. in sources folder go to ..\Config\getMyStashJsonConfig.json and open getMyStashJsonConfig.json in editor.

 Set "chromedriver_path" (downloaded ChromeDriver - WebDriver for Chrome) and "user_profile_path" (path to Chrome browser user profile).

 Example of getMyStashJsonConfig.json (double backslashes required):
 ```
 {
  "chromedriver_path": "D:\\GetMyStashJson\\chromedriver_win32\\chromedriver.exe",
  "user_profile_path": "C:\\Users\\userName\\AppData\\Local\\Google\\Chrome\\User Data"
}
```

7. Make sure you are authenticated on official Path of Exile site;

8. Close Chrome browser if it is running (also it is better to close all tabs too);

9. run gmsj.py (from downloaded sources folder) from console with the following args:
```
-l <league> -a <account name> (optional -c <character>) -r <index range or specific index/indexes> (example: -r "[1-5, 7, 1]")
```

Examples:
```
gmsj.py -l Standard -a MyPoEAccountName
```
- If you want to save character inventory, use this:
```
gmsj.py -c MyCharacterName -a MyPoEAccountName 
```
- To get stash tabs with indexes 0, 2 to 5, 11 and 25 to 50, use this:
```
gmsj.py -c MyCharacterName -a MyPoEAccountName -r "[0, 2-5, 11, 25-50]"
```
and wait until json data is saved for each Stash Tab in separate .json files in sources\outputJson folder.
