# 网络安全信息搜集平台
> 网络安全信息搜集平台服务端。为前端页面展示提供全套后台服务功能。

## 项目说明
* app.py
> 项目启动文件，包含全部的request请求接口和拦截器设置

* userManager.py
> 用户信息管理模块。提供对用户增、删、改、查、登录、注册等功能。

* dnsResolve.py.py
> DNS解析模块。提供对dns进行解析的功能。

* subdomainLookup.py
> 子域名解析模块。

* emailGrabbing.py
> 邮箱内容解析模块。目前只对指定邮箱账号中的内容进行扒取和解析。

* portDetection.py
> 端口检测模块。用于检测指定地址上指定端口的状态（开启/关闭）。

* requirements.txt
> 包管理文件。包含所有需要依赖的三方包。需要在项目启动前执行安装。

## To Start
1. 使用以下命令安装需要的Python依赖包。
```shell
pip install -r requirements.txt
```

2. 切换目录到当前路径下

3. 运行app.py
```shell
#前台执行
python3 app.py
#后台守护进程执行
nohup python3 app.py >> app.log 2>&1 &
```

## 备注
1. 更新依赖包文件可以使用以下命令
```shell
pip freeze > requirements.txt
```







