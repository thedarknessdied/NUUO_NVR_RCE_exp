# NUUO_NVR_RCE_exp
NUUO NVR Remote command execution for video storage management devices

## Description
PhpIPAM is an open source web IP address management application. Its goal is to provide a simple IP address management application. Phpipam has a default weak password, which can be exploited by attackers to obtain relevant information.

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
