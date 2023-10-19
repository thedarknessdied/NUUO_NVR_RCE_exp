# NUUO_NVR_RCE_exp
NUUO NVR Remote command execution for video storage management devices

## Attention
I have developed a tool for local testing and POC development, which is for technical learning reference only. Please do not use it for illegal purposes. Any direct or indirect consequences and losses caused by individuals or organizations using the information provided in this article are the responsibility of the user themselves and have nothing to do with the author!!!

<img width="294" alt="1697677069859" src="https://github.com/thedarknessdied/NUUO_NVR_RCE_exp/assets/56123966/d2a11d08-153d-4cf1-b154-689f123c53ec">


## Description
Lanling EIS, a simple and efficient work style, is a mobile office platform specifically designed for growth enterprises for communication, collaboration, and socializing, covering management needs such as OA, communication, customer, personnel, and knowledge

## installation
> pip install -r requirements.txt

## Tools Usage
```python
python 蓝凌EIS智慧协同平台任意文件上传.py -h
usage: 蓝凌EIS智慧协同平台任意文件上传.py [-h] (-u URL | -f FILE) [--upload UPLOAD | --content CONTENT] [--random-agent RANDOM_AGENT | -a USERAGENT] [-d DELAY] [-t THREAD] [--proxy PROXY] --file-type FILE_TYPE

Upload any file on Lanling EIS smart collaboration platform

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Enter target object
  -f FILE, --file FILE  Input target object file
  --upload UPLOAD       Enter the filepath
  --content CONTENT     write the content by yourself
  --random-agent RANDOM_AGENT
                        Using random user agents
  -a USERAGENT, --useragent USERAGENT
                        Using the known User-agent
  -d DELAY, --delay DELAY
                        Set multi threaded access latency (setting range from 0 to 5)
  -t THREAD, --thread THREAD
                        Set the number of program threads (setting range from 1 to 50)
  --proxy PROXY         Set up the proxy
  --file-type FILE_TYPE
                        Upload file type(default is asp)
```
