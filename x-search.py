#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import argparse


if __name__ == '__main__':
    # 创建一个解析器对象
    parser = argparse.ArgumentParser(
        prog="x-search",  # 程序名，默认为sys.argv[0]
        description="x-search 一个方便web打点，一键信息收集的工具",  # 程序描述
        epilog="如果存在问题，请在github上发起lssue",  # 帮助信息底部的文本
        add_help=False
    )
    # 添加可选参数
    parser.add_argument('-op',metavar='[path]', type=str, default='output.txt', help='输出报告路径，示例：D://output.txt')
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出")

    # 解析命令行参数
    args = parser.parse_args()
