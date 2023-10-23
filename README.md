# NUUO_NVR_RCE_exp
NUUO NVR Remote command execution for video storage management devices

## Attention
I have developed a tool for local testing and POC development, which is for technical learning reference only. Please do not use it for illegal purposes. Any direct or indirect consequences and losses caused by individuals or organizations using the information provided in this article are the responsibility of the user themselves and have nothing to do with the author!!!

<img width="317" alt="1697677290986" src="https://github.com/thedarknessdied/NUUO_NVR_RCE_exp/assets/56123966/a0f3ff04-eec6-4a6e-befb-3a5283bb7ee1">



## Description
NUUO NVR is a network video recorder owned by NUUO Corporation in Taiwan, China, China. The device has a remote command execution vulnerability, which can be used by an attacker to execute arbitrary commands, thereby obtaining the privileges of the server.

## installation
> pip install -r requirements.txt

## Tools Usage
```python
python Network_Video_Recorder_Login.py -h
usage: Network_Video_Recorder_Login.py [-h] (-u URL | -f FILE) [--random-agent RANDOM_AGENT] [--time-out TIME_OUT] [-d DELAY] [-t THREAD] [--proxy PROXY]

NUUO NVR Video Storage Management Device Remote Command Execution

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Enter target object
  -f FILE, --file FILE  Input target object file
  --random-agent RANDOM_AGENT
                        Using random user agents
  --time-out TIME_OUT   Set the HTTP access timeout range (setting range from 0 to 5)
  -d DELAY, --delay DELAY
                        Set multi threaded access latency (setting range from 0 to 5)
  -t THREAD, --thread THREAD
                        Set the number of program threads (setting range from 1 to 50)
  --proxy PROXY         Set up HTTP proxy
```
