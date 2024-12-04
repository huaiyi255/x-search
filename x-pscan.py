import socket
import concurrent.futures
import time
import ipaddress
import os
import re
import pandas as pd
import argparse
import sys
import pyfiglet

def parse_args():
    if len(sys.argv) < 2:
        print("Usage: python3 x-pscan.py --help")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        prog="x-pscan",
        description="x-pscan 一个简易的端口存活扫描工具",
        epilog="如果存在问题，请在github上发起lssue",
        add_help=False
    )

    txt = 'x-pscan'

    testresult = pyfiglet.figlet_format(txt)
    print(testresult)

    strip = """输入要扫描的主机，可接受如下几种形式ip输入，为空时扫描的主机默认为127.0.0.1。\n
                第一种 网段 10.42.0.1/24，\n
                第二种 ip范围 10.42.0.1-10.51.3.1，\n
                第三种 ip单个ip或者多个ip  单个ip 10.42.0.1  多个ip 10.42.0.1,10.42.0.2,10.42.0.3 ，\n
                第四种 输入一个ip地址的文件列表路径，从文件种提取一个一个的单个ip，不会解析ip段等。"""
    strport = """输入要扫描的端口，可接受如下几种形式端口输入，为空时默认扫描。1-65535端口。\n
    第一种 20 或 20,30,80 ，\n
    第三种 1-65535  ，\n
    第四种 20,80-85,99 。
    """

    parser.add_argument("--help", action="help", help="显示帮助信息并退出")
    parser.add_argument('-h', metavar='host', type=str, help=strip)
    parser.add_argument('-p', metavar='port', type=str, help=strport)

    args = parser.parse_args()
    return args



def convert_to_ip_list(input_str):
    ip_list = []
    if os.path.isfile(input_str):
        with open(input_str, 'r', encoding='utf-8') as file:
            text = file.read()
        ip_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        ip_list += ip_addresses
    else:
        input_str = input_str.replace('，', ',')

        if '/' in input_str:
            network = ipaddress.ip_network(input_str, strict=False)
            ip_list.extend(network.hosts())
        elif '-' in input_str:
            start_ip, end_ip = input_str.split('-')
            start_ip = ipaddress.ip_address(start_ip)
            end_ip = ipaddress.ip_address(end_ip)
            while start_ip <= end_ip:
                ip_list.append(start_ip)
                start_ip += 1
        elif ',' in input_str:
            for ip_str in input_str.split(','):
                ip_list.append(ipaddress.ip_address(ip_str))
        else:
            ip_list.append(ipaddress.ip_address(input_str))
    ip_lst = set(ip_list)
    ip_end = sorted(ip_lst, key=ipaddress.ip_address)
    ip_end1 = []
    for i in ip_end:
        ip_end1.append(str(i))
    return ip_end1

def port_input(s):
    s = s.replace('，', ',')
    postlist = []
    if ',' in s and '-' in s:
        elements = s.split(',')
        for element in elements:
            if '-' in element:
                element_index = element.find('-')
                stat, end = element[:element_index], element[element_index + 1:]
                for i in range(int(stat), int(end) + 1):
                    postlist.append(i)
            else:
                postlist.append(int(element))
    elif ',' in s and '-' not in s:
        elements = s.split(',')
        for element in elements:
            postlist.append(int(element))
    elif '-' in s and ',' not in s:
        element_index = s.find('-')
        stat, end = s[:element_index], s[element_index + 1:]
        for i in range(int(stat), int(end) + 1):
            postlist.append(i)
    elif ',' not in s and '-' not in s:
        postlist.append(int(s))
    unique_elements = tuple(set(postlist))
    return unique_elements

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"{host}:{port} open")
            sock.sendall(b'Hello\r\n')
            banner = sock.recv(1024)
            banner1 = banner.decode('utf-8', errors='ignore')
            return {host: {port: banner1}}
        else:
            return 0
    except socket.error as e:
        str1 = "连接错误" + str(e)
        return {host: {port: str1}}
    finally:
        sock.close()

def scan_port_main(host, port):
    start_time = time.time()
    portlist = port_input(port)
    hosts = convert_to_ip_list(host)
    results = {}
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=2000) as executor:
        futures = [executor.submit(scan_port, host, port) for host in hosts for port in portlist]
    for future in concurrent.futures.as_completed(
            futures):
        result = future.result()
        if result != 0:
            keys = list(result.keys())
            first_key = keys[0]
            if first_key not in results:
                results[first_key] = {}
                results[first_key].update(result[first_key])
            else:
                results[first_key].update(result[first_key])
    df = pd.DataFrame(results)
    end_time = time.time()
    print(f'[+] 扫描完成，耗时: {end_time - start_time} 秒')

if __name__ == '__main__':
    args = parse_args()
    if args.h == None:
        scan_port_main("127.0.0.1", args.p)
    if args.p == None:
        scan_port_main(args.h, "1-65535")
    if args.h != None and args.p != None:
        scan_port_main(args.h, args.p)
    if args.h == None and args.p == None:
        scan_port_main("127.0.0.1", "1-65535")
