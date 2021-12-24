import requests
import socket
import sys
import random


host = 'localhost'
OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110


def close(code, public="", private=""):
    if public:
        print(public)
    if private:
        print(private, file=sys.stderr)
    print("Exit with code {}".format(code), file=sys.stderr)
    exit(code)


def isDown(ex):
    close(DOWN, public=f"Connection error: {ex}")


def put(id, flag):
    global host
    try:
        resp = requests.get(f'http://{host}/api/add_flag',
            params={
                'key': id,
                'value': flag
            })
    except Exception as ex:
        isDown(ex)
    if resp.status_code != 200:
        close(MUMBLE, private=f"Wrong status code: {resp.status_code}")
    try:
        jsono = resp.json()
    except Exception as ex:
        print(f"Text of response: {resp.text}", file=sys.stderr)
        close(MUMBLE, private=f"Failed to decode json response: {ex}")
    if 'Success' not in jsono or jsono['Success'] != True:
        close(MUMBLE, private="Wrong json response")


def get(id, flag=None):
    global host
    try:
        resp = requests.get(f'http://{host}/api/get_flag',
            params={
                'key': id,
            })
    except Exception as ex:
        isDown(ex)
    if resp.status_code != 200:
        close(MUMBLE, private=f"Wrong status code: {resp.status_code}")
    try:
        jsono = resp.json()
    except Exception as ex:
        print(f"Text of response: {resp.text}", file=sys.stderr)
        close(MUMBLE, private=f"Failed to decode json response: {ex}")
    if 'NoFlag' in jsono:
        if flag is None:
            return False
        close(MUMBLE, private=f"No flag retrieved by the specified id: {id}")
    if 'Value' not in jsono:
        close(MUMBLE, private=f"Both NoFlag and Value in response not provided")
    if flag is None:
        return jsono['Value']
    if flag != jsono['Value']:
        close(CORRUPT, private=f"Returned flag value {jsono['Value']}. Expected flag value {flag}.")
    close(OK)


def info():
    close(OK, public='{"vulns": 1, "timeout": 30, "attack_data": ""}')


def randWord(symbol_count, alphabet):
    res = [random.choice(alphabet) for _ in range(symbol_count)]
    return ''.join(res)


def randId():
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    a = randWord(4, alphabet)
    b = randWord(4, alphabet)
    c = randWord(4, alphabet)
    return f'{a}-{b}-{c}'


def randFlag():
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    a = randWord(31, alphabet)
    return f'{a}='


def check(gen_count=100, logging=False):
    flags = [(randId(), randFlag()) for _ in range(gen_count)]
    for id, flag in flags:
        put(id, flag)
        if logging:
            print(id, flag)
    for id, flag in flags:
        actual_flag = get(id)
        if actual_flag != flag:
            close(MUMBLE, private=f"Flag was not stored =( id={id}, flag should be {flag} but have {actual_flag}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        close(CHECKER_ERROR, private="Not enough arguments. Mode is not set =(")
    mode = sys.argv[1]
    if mode == 'info':
        info()
    elif mode in ['check', 'put', 'get', 'gen']:
        if len(sys.argv) < 3:
            close(CHECKER_ERROR, private="Not enough arguments. Hostname is not set")
        host = sys.argv[2]
        if mode == 'check':
            check()
        elif mode == 'gen':
            check(logging=True)
            exit(0)
        else:
            if len(sys.argv) < 5:
                close(CHECKER_ERROR, private="Not enough arguments. id and/or flag are not set")
            id = sys.argv[3]
            flag = sys.argv[4]
            if mode == 'put':
                put(id, flag)
                close(OK, public=id)
            else:
                get(id, flag)
        close(OK)
    else:
        close(CHECKER_ERROR, private=f"Bad mode value: {mode}")
