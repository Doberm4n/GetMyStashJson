rmdir /Q /S dist
mkdir dist
mkdir dist\Config
mkdir dist\Docs
mkdir dist\chromedriver_win32
mkdir dist\outputJson
copy *.py dist\
copy getMyStashJsonConfig.json dist
copy Config\*.* dist\Config
copy README.md dist
copy Docs\*.md dist\Docs
copy outputJson\readme.txt dist\outputJson
copy chromedriver_win32\chromedriver.exe dist\chromedriver_win32
