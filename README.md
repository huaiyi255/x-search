# x-search
x-search 一个方便web打点，一键信息收集的工具

## 目录信息
```
├─dit  各种爆破字典
├─finger  各种指纹信息
└─src  各种功能脚本
```

## 更新计划
**0.1 实现基本功能**
- [x] 对命令行参数输入的选项参数进行解析
- [x] 检测域名是否存在cdn，以及判断cdn运营商
- [ ] 尝试对cdn进行绕过
- [ ] 检测域名是否存在泛解析，以及判断泛解析运营商
- [ ] 尝试对泛解析绕过
- [ ] 识别waf
- [ ] 证书查询，whois，爆破等方式获取子域名
- [ ] 路径爆破，谷歌，baidu 搜索，github，获取敏感路径，文件信息
- [ ] ip反查域名获得更多资产，设置反查层数。通过fofa，鹰图等进行信息收集，扩大资产面
- [ ] 通过网站指纹信息进行指纹识别
- [ ] 自定义代理
- [ ] 实现任意子脚本多进程或者多协程的处理
- [ ] 通过poc，exp进行漏扫
- [ ] 对c段或指定网段的ip 端口服务进行扫描（使用nmap或者自己写）
- [ ] 对未授权进行自动化利用
- [ ] 识别蜜罐
- [ ] 目标网站js扫描
