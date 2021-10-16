#! /usr/bin/python3
import sys, re
import yaml

with open("config.yaml", "r") as config:
    try:
        config = yaml.safe_load(config)
    except yaml.YAMLError as exc:
        config = None
        print(exc)
CSI = "\x1B["
COLORS = {
    'aqua': '36',
    'blue': '34',
    'red': '31',
    'white': '37',
    'green': '32',
    'yellow': '33',
    'pink': '35'
}

KEYWORDS = ['ip']
if __name__ == "__main__":
    if config is None:
        print('No config detected')
        exit()
    for line in sys.stdin:
        l = line.lower()
        if 'ip' in config:
            pat = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
            IPs = pat.findall(l)
            if IPs is not None:
                for ip in IPs:
                    line = line.replace(ip, f'{CSI}{COLORS["white"]};40m"{ip}{CSI}0m')
        for key in config.keys():
            if key not in KEYWORDS:
                for item in config[key]['words']:
                    compiled = re.compile(re.escape(item), re.IGNORECASE)
                    line = compiled.sub(f'{CSI}{COLORS[config[key]["color"]]};40m"{item}{CSI}0m', line)
        print(line.rstrip("\n"))
