### 前言

现如今，要说比较火的编程语言当属 JavaScript 和 Python 了，这两门语言都可以独立编写前端页面、后端服务器、手机 APP、电脑客户端等等，无所不能。不过，不同的编程语言有不同的侧重点。比如 JavaScript 写网页得心应手，Python 处理大数据信手拈来。那么，能不能取两者的优点，构建一个跨平台客户端框架呢？这就有了今天的主角：[vue-pywebview-pyinstaller](https://github.com/pangao1990/vue-pywebview-app)。

### 应用简介

[vue-pywebview-pyinstaller](https://github.com/pangao1990/vue-pywebview-app) 是一款基于 Vue3、pywebview 和 PyInstaller 框架，构建 macOS 和 windows 平台客户端的应用。本应用的视图层采用 HTML+JS+CSS，业务层采用本地 Python。考虑到某些生物计算场景数据量大，数据私密，因此将数据上传到服务器计算，并不一定是最优解，选择采用本地 Python 也是一种不错的选择。不过，如果需要调用远程 API，本应用也是支持的。

##### 应用优势

- 采用 Vue3 框架开发视图层，简洁高效
- 采用 Python 编程语音开发业务层，模块丰富
- 本应用已经封装打包环节，一键生成 macOS 和 windows 平台的客户端应用。开发者只需要关注试图效果和业务逻辑本身，将繁重复杂的打包环节交给本应用处理即可

##### 适用场景

- 对软件的用户界面有一定美感要求
- 需要用到 Python 中的人工智能、生信分析等模块
- 考虑搭建本地应用，使用本机计算和存储资源

##### 适用人群

熟悉 Vue3 和 Python 编程的程序员。

### 应用安装

#### 运行环境

- npm6.0+ ([NodeJs 安装教程](https://blog.pangao.vip/NodeJs安装教程/))
- Python3.5-3.8 ([Python 安装教程](https://blog.pangao.vip/Python环境搭建及模块安装))

**注意**：在 windows 系统下，由于 Pywebview3 所依赖的 pythonnet 包仅支持 Python3.5-3.8 版本，因此，推荐 win 用户使用 Python3.8 版本。

#### 应用下载

利用 git（[git 安装教程](https://blog.pangao.vip/Git安装教程/)） 下载应用，如下所示：

```
git clone https://github.com/pangao1990/vue-pywebview-app.git
```

或者，直接在我的 [github](https://github.com/pangao1990/vue-pywebview-app) 下载。

```
# 进入项目
cd vue-pywebview-app
```

进入项目，项目清单如下所示：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-1.png)

#### 初始化

下载完毕后，运行初始化命令，程序会自动下载安装对应操作平台的所需依赖软件，如下所示：

```
# 初始化
npm run init
```

没报错信息，则初始化完成，如下所示：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-2.png)

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-3.png)

项目里多了一个 node_modules 文件夹，用于存放 npm 下载的包；多了一个 pyenv 文件夹，用于存放 Python 虚拟环境。

### 应用运行

输入如下命令，即可启动应用：

```
npm run start
```

终端显示如下：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-4.png)

同时，会启动一个客户端程序，如下：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-5.png)

整体效果如下所示（gif 图片加载可能有点慢）：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-6.gif)

### 高级用法

#### 客户端引擎介绍

本应用基于 [pywebview](https://pywebview.flowrl.com) 构建客户端。而 pywebview 构架构建客户端的原理是利用本地电脑自带的浏览器引擎驱动，模拟生成客户端。本质上还是网页，或者说是一个浏览器，但是感官上和本地客户端没有差别。

那么，基于 pywebview 构架构建客户端的成败或质量，就与本地电脑的浏览器引擎息息相关了。

##### windows 系统

在 windows 系统上，大体上分为两类客户端引擎：正常模式和兼容模式。

- 正常模式

正常模式下，按照 edgechromium ，edgehtml， mshtml 的客户端引擎依次检索。如果本地电脑 edge 浏览器支持这些引擎，则客户端可以正常启动。否则，请安装对应的 [EdgeWebView2Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) 浏览器引擎。

- 兼容模式

如果本地电脑 edge 浏览器不支持这些引擎，同时也不想下载 [EdgeWebView2Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) ，那么就可以使用兼容模式。兼容模式的原理就是利用 [CEFPython](https://github.com/cztomczak/cefpython)，嵌入 Chromium 的 Web 浏览器控件。也就是只要本地电脑安装了谷歌浏览器 V66 版及其以上版本，即可正常启动客户端。缺点就是生成的安装包体积会增加大约 60M 左右。

##### macOS 系统

macOS 系统的浏览器引擎就没有那么多版本了，由于 macOS 系统的封闭性，在 macOS 系统就只有一种 WebKit 引擎可用。

不过，在 macOS 系统却存在另一个问题。那就是苹果自主研发的 M1 芯片。由于 windows 系统随处可见，我可以找很多电脑测试。mac 电脑我就只有一台 M1 芯片和一个 x86_64 芯片，做不了更多测试。总之，目前我这两台苹果电脑构建的客户端不能交叉使用，原因不明。

#### 构建客户端 API

构建客户端的主程序是在 pyapp 文件夹下的 main.py 和 mainCEF.py ，如下所示：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-7.png)

mainCEF.py 脚本的内容和 main.py 几乎一模一样，也就是 新增了一个 cef 模式，用于 windows 系统的兼容模式。

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-8.png)

main.py 里面主要是依靠 webview.create_window 和 webview.start 这两个 API 来构建客户端。其他的一些 API，我也会在后面的教程中详细介绍。或者可以直接查看 [pywebview 官网](https://pywebview.flowrl.com/guide/api.html) 了解详情。

##### webview.create_window

```
webview.create_window(title, url='', html='', js_api=None, width=800, height=600, \
                      x=None, y=None, resizable=True, fullscreen=False, \
                      min_size=(200, 100), hidden=False, frameless=False, \
                      minimized=False, on_top=False, confirm_close=False, \
                      background_color='#FFF')
```

创建一个新的 pywebview 窗口，并返回其实例。在开始 GUI 循环之前，窗口不会显示。

- **title** 窗口标题
- **url** 要加载的 URL。如果 URL 没有协议前缀，则将其解析为相对于应用程序入口点的路径。或者，可以传递 WSGI 服务器对象来启动本地 Web 服务器。
- **html** 要加载的 HTML 代码。如果同时指定了 URL 和 HTML，HTML 优先。
- **js_api** 将 python 对象暴露到当前 pywebview 窗口的 DOM 中。js_api 对象的方法可以通过调用 window.pywebview.api.<methodname>(<parameters>)从 Javascript 执行。请注意，调用 Javascript 函数会收到一个包含 python 函数的返回值。只有基本的 Python 对象（如 int、str、dict......）才能返回 Javascript。
- **width** 窗户宽度。默认值为 800px。
- **height** 窗户高度。默认值为 600px。
- **x** 窗口 x 坐标。默认值居中。
- **y** 窗口 y 坐标。默认值居中。
- **resizable** 是否可以调整窗口大小。默认值为 True
- **fullscreen** 从全屏模式开始。默认为 False
- **min_size** 指定最小窗口大小的（宽度、高度）元组。默认值为 200x100
- **hidden** 默认情况下创建一个隐藏的窗口。默认为 False
- **frameless** 创建一个无框窗口。默认值为 False。
- **minimized** 以最小化模式启动
- **on_top** 将窗口设置为始终位于其他窗口的顶部。默认值为 False。
- **confirm_close** 是否显示窗口关闭确认对话框。默认为 False
- **background_color** 加载 WebView 之前显示的窗口的背景颜色。指定为十六进制颜色。默认值为白色。
- **transparent** 创建一个透明的窗口。Windows 不支持。默认值为 False。请注意，此设置不会隐藏或使窗口铬透明。将窗口 chrome setframeless 隐藏为 True。

##### webview.start

```
webview.start(func=None, args=None, localization={}, gui=None, debug=False, http_server=False)
```

启动 GUI 循环并显示之前创建的窗口。此函数必须从主线程调用。

- **func** 启动 GUI 循环时调用的函数。
- **args** 函数参数。可以是单个值，也可以是元组值。
- **localization** 带有本地化字符串的词典。默认字符串及其键在 localization.py 中定义
- **gui** 强制使用特定的 GUI。允许的值是 cef、qt 或 gtk，具体取决于平台。
- **debug** 启用调试模式。
- **http_server** 启用内置 HTTP 服务器。如果启用，本地文件将使用随机端口上的本地 HTTP 服务器提供服务。对于每个窗口，都会生成一个单独的 HTTP 服务器。对于非本地 URL，此选项将被忽略。

#### 域间通信

##### 从 Python 调用 Javascript

window.evaluate_js(code, callback=None)允许您使用同步返回的最后一个值执行任意 Javascript 代码。如果提供了回调函数，则解析 promise，并调用回调函数，结果作为参数。Javascript 类型转换为 Python 类型，例如 JS 对象到 Python 字典，数组到列表，未定义为 None。由于实现限制，字符串“null”将被计算为 None。另外，evaluate_js 返回的值限制为 900 个字符内。

##### 从 Javascript 调用 Python

从 Javascript 调用 Python 函数可以通过两种不同的方法完成。

- 通过将 Python 类的实例暴露给 create_window 的 js_api。该类的所有可调用方法都将以 pywebview.api.method_name 的形式公开到 JS 域中。方法名称不得以下划线开头。
- 通过将函数传递给窗口对象的 expose(func)这将以 pywebview.api.func_name 的形式将一个或多个函数公开到 JS 域。与 JS API 不同，expose 也允许在运行时公开函数。如果 JS API 和以这种方式公开的函数之间存在名称冲突，则后者优先。

#### 打包客户端

pywebview 建议 macOS 用 [py2app](https://py2app.readthedocs.io/en/latest/) 打包，windows 用 [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/) 打包。但是我发现 pyinstaller 也可以很顺畅得打包 macOS 应用，虽然移植有点问题。

我就不介绍 pyinstaller 的打包方法了，后面我会出这个框架详细的打包介绍。这里我将打包方法封装在应用中，只需要按命令打包即可。

```
# 预打包，带console，方便输出日志信息
npm run pre

# 预打包，带console，兼容模式，仅win系统
npm run pre:cef

# 预打包，带console，生成文件夹，仅win系统
npm run pre:folder

# 预打包，带console，生成文件夹，兼容模式，仅win系统
npm run pre:folder:cef


# 正式打包
npm run build

# 正式打包，兼容模式，仅win系统
npm run build:cef

# 正式打包，生成文件夹，仅win系统
npm run build:folder

# 正式打包，生成文件夹，兼容模式，仅win系统
npm run build:folder:cef
```

---

更多编程教学请关注公众号：**潘高陪你学编程**

![image](https://cdn.jsdelivr.net/gh/pangao1990/pangao1990.github.io@master/pic/潘高陪你学编程.jpg)

---
