## 前言

[**PPX**](https://blog.pangao.vip/docs-ppx/)（曾用名 vue-pywebview-pyinstaller）。第一个 **P** 表示 **P**ython ，当然，也可以表示 **P**angao（潘高，也就是我本人）。第二个 **P** 表示 **P**ywebview ，也可以表示 **P**yinstaller 。第三个 **X** 表示无限可能，指视图层可以使用 Vue、React、Angular、HTML 中的任意一种。

## 搭后语

现如今，要说比较火的编程语言当属 JavaScript 和 Python 了，这两门语言都可以独立编写前端页面、后端服务器、手机 APP、电脑客户端等等，无所不能。不过，不同的编程语言有不同的侧重点。比如 JavaScript 写网页得心应手，Python 处理大数据信手拈来。那么，能不能取两者的优点，构建一个跨平台客户端框架呢？这就有了今天的主角：[PPX](https://blog.pangao.vip/docs-ppx/)。

## 应用简介

[PPX](https://blog.pangao.vip/docs-ppx/) 基于 pywebview 和 PyInstaller 框架，构建 macOS 、 Windows 和 Linux 平台的客户端。本应用的视图层支持 Vue、React、Angular、HTML 中的任意一种，业务层支持 Python 脚本。考虑到某些生物计算场景数据量大，数据私密，因此将数据上传到服务器计算，并不一定是最优解，采用本地 Python 也是一种不错的选择。不过，如果需要调用远程 API，本应用也是支持的。

#### 应用优势

- 视图层可使用任意一款你喜欢的前端框架，比如 Vue、React、Angular、HTML 等，迁移无压力
- 采用 Python 编程语言开发业务层，模块丰富
- 本应用已经封装打包环节，一键生成 macOS 、 Windows 和 Linux 平台的客户端应用。开发者只需要关注视图效果和业务逻辑本身，将繁重复杂的打包环节交给本应用处理即可

#### 适用场景

- 对软件的用户界面有一定美感要求
- 需要用到 Python 中的人工智能、生信分析等模块
- 考虑搭建本地应用，使用本机计算和存储资源

#### 适用人群

熟悉 Python3 和 任意一款前端框架，如 Vue、React、Angular、HTML 编程的程序员。

## 应用安装

#### 运行环境

- Node.js 16.14+ ([Node.js 安装教程](https://blog.pangao.vip/NodeJs安装教程/))

- pnpm 8.x+ ([pnpm 安装教程](https://pnpm.io/zh/installation))

- Python3.8-3.11 ([Python 安装教程](https://blog.pangao.vip/Python环境搭建及模块安装))

#### 应用下载

利用 git（[git 安装教程](https://blog.pangao.vip/Git安装教程/)） 下载应用，如下所示：

```shell
git clone https://github.com/pangao1990/PPX.git
```

或者，直接在 [github](https://github.com/pangao1990/PPX) 下载。

```shell
# 进入项目
cd PPX
```

进入项目，项目清单如下所示：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-1.png)

#### 初始化

下载完毕后，运行初始化命令，程序会自动下载安装对应操作平台的所需依赖软件，如下所示：

```shell
# 初始化 (linux系统中需要输入sudo命令密码)
pnpm run init
```

没报错信息，则初始化完成，如下所示：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-2.png)

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-3.png)

项目根目录多了一个 node_modules 文件夹和 pnpm-lock.yaml 文件，用于存放 pnpm 下载的包。

## 应用运行

输入如下命令，即可启动应用：

```shell
pnpm run start
```

终端显示如下：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-4.png)

同时，启动一个客户端程序，如下：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-5.png)

整体效果如下所示（gif 图片加载可能有点慢）：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-6.gif)

## 高级用法

### 客户端引擎介绍

本应用基于 [pywebview](https://pywebview.flowrl.com) 构建客户端。而 pywebview 构架构建客户端的原理是利用本地电脑自带的浏览器引擎驱动，模拟生成客户端。本质上还是网页，或者说是一个浏览器，但是感官上和本地客户端没有差别。

那么，基于 pywebview 构架构建客户端的成败或质量，就与本地电脑的浏览器引擎息息相关了。

#### Windows 系统

在 Windows 系统上，大体上分为两类客户端引擎：正常模式和兼容模式。

- 正常模式

正常模式下，按照 edgechromium ，edgehtml， mshtml 的客户端引擎依次检索。如果本地电脑 edge 浏览器支持这些引擎，则客户端可以正常启动。否则，请安装对应的 [EdgeWebView2Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) 浏览器引擎。

- 兼容模式

如果本地电脑 edge 浏览器不支持这些引擎，同时也不想下载 [EdgeWebView2Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) ，那么就可以使用兼容模式。兼容模式的原理就是利用 [CEFPython](https://github.com/cztomczak/cefpython)，嵌入 Chromium 的 Web 浏览器控件。也就是只要本地电脑安装了谷歌浏览器 V66 版及其以上版本，即可正常启动客户端。缺点就是生成的安装包体积会增加大约 60M 左右。

#### macOS 系统

macOS 系统的浏览器引擎就没有那么多版本了，由于 macOS 系统的封闭性，在 macOS 系统就只有一种 WebKit 引擎可用。

不过，在 macOS 系统却存在另一个问题。那就是苹果自主研发的 M 系列芯片。用 x86_64 芯片打包的应用可以在 x86_64 和 M 芯片电脑上运行，用 M 芯片打包的应用只能在 M 芯片电脑上运行。

### 构建客户端 API

构建客户端的主程序是 main.py ，如下所示：

![image](https://blog.pangao.vip/pic/JavaScript和Python打造跨平台客户端应用——vue-pywebview-pyinstaller-7.png)

main.py 里面主要是依靠 webview.create_window 和 webview.start 这两个 API 来构建客户端。其他的一些 API，我也会在后面的教程中详细介绍。或者可以直接查看 [pywebview 官网](https://pywebview.flowrl.com/guide/api.html) 了解详情。

#### webview.create_window

```
webview.create_window(title, url=None, html=None, js_api=None, width=800,
    height=600, x=None, y=None, screen=None, resizable=True, fullscreen=False,
    min_size=(200, 100), hidden=False, frameless=False, easy_drag=True,
    focus=True, minimized=False, maximized=False, on_top=False,
    confirm_close=False, background_color='#FFFFFF', transparent=False,
    text_select=False, zoomable=False, draggable=False,
    server=http.BottleServer, server_args={}, localization=None)
```

创建一个新的客户端窗口并返回其实例。在 GUI 循环启动之前，窗口不会显示。如果在 GUI 循环期间调用该函数，则会立即显示该窗口。

- **`title`** 窗口标题。
- **`url`** 要加载的 URL。如果 URL 没有协议前缀，则将其解析为相对于应用程序入口点的路径。**或者，可以传递 WSGI 服务器对象来启动本地 Web 服务器。**
- **`html`** 要加载的 HTML 代码。**如果同时指定了 URL 和 HTML，则 HTML 优先。**
- **`js_api`** 将 Python 对象暴露给当前应用窗口的 DOM。即可在 Javascript 代码中通过调用 `window.pywebview.api.<methodname>(<parameters>)` 执行 Python 对象的方法。**调用 Javascript 函数会收到一个 promise ，该 promise 将包含 Python 函数的返回值。只有基本的 Python 对象（如 int、str、dict、...）才能返回到 Javascript。**
- **`width`** 窗口宽度。默认值为 **800** 。
- **`height`** 窗户高度。默认值为 **600** 。
- **`x`** 窗口 x 坐标。默认值 **居中** 。
- **`y`** 窗口 y 坐标。默认值 **居中** 。
- **`screen`** 屏幕显示窗口。`screen` 是由 `webview.screens` 返回的屏幕实例 。
- **`resizable`** 是否可以调整窗口大小。默认值为 **True** 。
- **`fullscreen`** 是否开启全屏模式。默认为 **False** 。
- **`min_size`** 指定最小窗口大小的元组（宽度、高度）。默认值是 **(200, 100)** 。
- **`hidden`** 是否隐藏窗口。默认为 **False** 。
- **`frameless`** 是否开启无框窗口。默认值为 **False** 。
- **`easy_drag`** 是否开启无框窗口的拖动模式。可通过拖动任何点来移动窗口。默认值为**True**。**该参数仅对无框窗口有效，对普通窗口无效。**
- **`focus`** 是否创建一个可聚焦的窗口。默认为 **True** 。
- **`minimized`** 是否开启最小化模式。默认为 **False** 。
- **`maximized`** 是否开启最小化模式。默认为 **False** 。
- **`on_top`** 设置窗口始终在其他窗口的顶部。默认为 **False** 。
- **`confirm_close`** 是否显示窗口关闭确认对话框。默认为 **False** 。
- **`background_color`** 加载 WebView 之前显示的窗口的背景颜色。指定为十六进制颜色。默认是 **'#FFFFFF'** 。
- **`transparent`** 是否开启透明窗口。默认为 **False** 。**不支持 Windows 系统。**
- **`text_select`** 是否启用 document 文本选择。默认值为 **False** 。想要单独控制每个元素的文本选择，请使用 CSS 属性 [**user-select**](https://developer.mozilla.org/zh-CN/docs/Web/CSS/user-select) 。
- **`zoomable`** 是否启用文档缩放。默认为 **False** 。
- **`draggable`** 是否启用图像和链接对象拖动。默认为 **False** 。
- **`vibrancy`** 启用窗口毛玻璃效果。默认为 **False** 。**仅支持 macOS 。**
- **`server`** 设置自定义 WSGI 服务器实例。默认为 **http.BottleServer** 。
- **`server_args`** 传递给服务器实例化的字典参数。
- **`localization`** 传递给每个窗口的本地化字典参数。

#### webview.start

```
webview.start(func=None, args=None, gui=None, debug=False, menu=[],
              http_server=False, http_port=None, user_agent=None,
              server=http.BottleServer, server_args={}, localization={})
```

启动 GUI 循环，并显示已经创建的窗口。**此函数必须从主线程调用。**

- **`func`** 启动 GUI 循环时调用的函数。
- **`args`** 调用函数的传参。可以是单个变量，也可以是元组。
- **`gui`** 指定 GUI 模式，可选值为 `None`、`cef`、`qt`、`gtk`。更多细节请查看 [渲染器](https://pywebview.flowrl.com/guide/renderer.html#gtk-webkit2) 。
- **`debug`** 是否启用调试模式。默认为 **False** 。
- **`http_server`** 是否启用内置 HTTP 服务器。默认为 **False** 。如果启用，将会为每个窗口开启一个独立的 HTTP 服务器，并使用随机端口。对于非本地 URL，此参数被忽略。
- **`http_port`** 指定 HTTP 服务器的端口号。默认 **随机端口** 。
- **`user_agent`** 设置 User-Agent 字符串。
- **`menu`** 传递菜单对象列表以创建应用程序菜单。
- **`server`** 设置自定义 WSGI 服务器实例。默认为 **http.BottleServer** 。
- **`server_args`** 传递给服务器实例化的字典参数。
- **`localization`** 本地化字典参数。

### 域间通信

这里的通信指的是 JavaScript（视图层，前端）和 Python（业务层，后端）的相互访问。

#### 从 Python 调用 Javascript

在 `Python` 代码中调用 `window.evaluate_js(code, callback=None)` 可以执行 `JavaScript` 代码。

- 在视图层代码中，绑定函数到 `window` 。

```JavaScript
// JavaScript

window['py2js_demo'] = (res) => {
    const resDict = JSON.parse(res)
    console.log('js', resDict)
}
```

- 在业务层代码中，调用视图层的函数。

```Python
# Python

import webview

def system_py2js(window):
    '''调用js中挂载到window的函数'''
    info = {'appName': 'PPX'}
    infoJson = json.dumps(info)
    window.evaluate_js(f"py2js_demo('{infoJson}')")

window = webview.create_window()
webview.start(system_py2js, window)
```

#### 从 Javascript 调用 Python

在 `Python` 代码中将类的实例传给 `create_window` 的 `js_api` 。在 `JavaScript` 代码中调用 `pywebview.api.method_name` 即可。

- 在业务层代码中，将类的实例传给 `create_window` 的 `js_api` 。

```Python
# Python

import webview

class Api:
    def system_getAppInfo(self):
        return {'appName': 'PPX'}

if __name__ == '__main__':
    api = Api()
    webview.create_window(js_api=api)
    webview.start()
```

- 在视图层代码中，调用业务层的函数。

```JavaScript
// JavaScript

window.pywebview.api.system_getAppInfo().then((res) => {
    console.log('js', res)
})
```

### 打包客户端

```
###########
# 简单用法 #
###########

# 初始化
pnpm run init

# 开发模式
pnpm run start

# 正式打包
pnpm run build

# 预打包，带console，方便输出日志信息
pnpm run pre


###########
# 进阶用法 #
###########

# 初始化，cef兼容模式
pnpm run init:cef

# 开发模式，cef兼容模式【仅win系统】
pnpm run start:cef

# 预打包，带console，cef兼容模式【仅win系统】
pnpm run pre:cef

# 预打包，带console，生成文件夹【仅win系统】
pnpm run pre:folder

# 预打包，带console，生成文件夹，cef兼容模式【仅win系统】
pnpm run pre:folder:cef

# 正式打包，单个exe程序【仅win系统】
pnpm run build:pure

# 正式打包，cef兼容模式【仅win系统】
pnpm run build:cef

# 正式打包，生成文件夹【仅win系统】
pnpm run build:folder

# 正式打包，生成文件夹，cef兼容模式【仅win系统】
pnpm run build:folder:cef
```

应用打包分为两步进行：

- 打包成可执行文件
- 打包成安装程序

#### 打包成可执行文件

基于 [Pyinstaller](https://www.pyinstaller.org) 将项目代码打包成可执行文件。

- 在 `Windows` 环境下打包成 `exe` 格式的可执行文件。
- 在 `macOS` 环境下打包成 `app` 格式的可执行文件。（用 `x86_64` 芯片打包的应用可以在 `x86_64` 和 `M` 芯片电脑上运行，用 `M` 芯片打包的应用只能在 `M` 芯片电脑上运行）
- 在 `Linux` 环境下打包成二进制格式的可执行文件。(在特定 CPU 架构下打包就只能在特定 CPU 架构下运行)

打包过程，会先由 `pyapp/spec/getSpec.py` 脚本生成 `windows.spec` 或 `macos.spec` 或 `linux.spec` 打包配置文件，之后基于该配置文件进行打包。

::: tip 注意  
这里需要注意一个问题。因 `Pyinstaller` 的打包机制，可能会造成某些动态库或者 Python 模块并没有被打包进可执行文件。因此，可能出现在生产环境运行没问题。但是打包后，就提示某些动态库或模块丢失。遇到这种情况，就需要在打包配置文件中添加丢失的动态库或模块。  
:::

##### 添加动态链接库

也可以简单的理解为， `addDll` 用于添加文件

```Python

# 示例
# 动态库是以元组形式字符串添加
# 以下示例表示将本地包中的 icudtl.dat 和 zh-CN.pak 文件添加到打包中
addDll = """
    ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/icudtl.dat', './'),
    ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/locales/zh-CN.pak','./locales')
    """
```

##### 添加 Python 模块

也可以简单的理解为， `addModules` 用于添加文件夹

```Python

# 模块是以元组形式字符串添加
# 以下示例表示将本地包中的 requests 模块整体添加到打包中
addModules = "('../../gui/dist', 'web'), ('../../static', 'static')"
```

#### 打包成安装程序

- 在 `Windows` 环境下，基于 [InnoSetup](https://jrsoftware.org/isinfo.php) ，打包成 `exe` 格式的安装程序
- 在 `macOS` 环境下，基于 [appdmg](https://github.com/LinusU/node-appdmg) ，打包成 `dmg` 格式的安装程序
- 在 `Linux` 环境下，基于 dpkg ，打包成 `deb` 格式的安装程序

##### 打包成 exe

打包过程，会先由 `pyapp/package/exe/getIss.py` 脚本生成 `InnoSetup.iss` 打包配置文件，之后基于该配置文件进行打包。

打包所需的数据均来自于 `pyapp/config/config.py` 配置文件。该文件几乎不需要修改。

::: warning 注意  
值得一提的是，安装包的唯一 `GUID` 。这个唯一编号取自于 `pyapp/config/config.py` 配置文件。在 `pnpm run init` 初始化之前，需要手动把 `pyapp/config/config.py` 配置文件中的 `appISSID` 置空，**PPX** 会自动生成一个唯一 `appISSID` ，生成后请勿修改！否则安装程序将会重复安装多个应用，而非覆盖安装。  
:::

```Python
# pyapp/config/config.py

# 初始化之前，请手动将 appISSID 设置为 ''
appISSID = ''    # Inno Setup 打包唯一编号。在执行 pnpm run init 之前，请设置为空，程序会自动生成唯一编号，生成后请勿修改！！！
```

```Python
# pyapp/package/exe/getIss.py

import os
from config.config import Config

appName = Config.appName    # 应用名称
appVersion = Config.appVersion  # 应用版本号
appVersion = appVersion[1:]    # 去掉第一位V
appDeveloper = Config.appDeveloper  # 应用开发者
appBlogs = Config.appBlogs  # 个人博客
rootDir = os.path.dirname(pyappDir)
buildDir = os.path.join(rootDir, 'build')
logoPath = os.path.join(rootDir, 'pyapp', 'icon', 'logo.ico')
appISSID = Config.appISSID    # 安装包唯一GUID
```

##### 打包成 dmg

打包过程，会先由 `pyapp/package/dmg/getJson.py` 脚本生成 `dmg.json` 打包配置文件，之后基于该配置文件进行打包。

在打包之前，请替换 `pyapp/package/dmg/bg.png` 背景图片和 `pyapp/package/dmg/潘高的小站.webloc` 网址文件。

```Python{4,19-24}
{
    "title": "''' + appName + '''",
    "icon": "../../icon/logo.icns",
    "background": "bg.png",
    "icon-size": 50,
    "contents": [
        {
            "x": 160,
            "y": 120,
            "type": "file",
            "path": "../../../build/''' + appName + '''.app"
        },
        {
            "x": 430,
            "y": 120,
            "type": "link",
            "path": "/Applications"
        },
        {
            "x": 450,
            "y": 243,
            "type": "file",
            "path": "./潘高的小站.webloc"
        }
    ],
    "window": {
        "size": {
            "width": 590,
            "height": 416
        }
    },
    "format": "UDBZ"
}
```

##### 打包成 deb

打包过程，会先由 `pyapp/package/deb/makeDeb.py` 脚本生成 `control` `postinst` `PPX.desktop` 等打包配置文件，之后基于这些配置文件进行打包。

::: warning 提示  
PPX 仅在 Ubuntu 22.04.2 版测试成功，其他 Linux 版本还请开发者自行测试。  
:::

#### 跨平台打包

在本机电脑操作，只能打包出本系统对应的程序包。如果想打包出三种系统的程序包，需要借助 `Github Action` 的能力。

::: warning 提示  
这里需要有 Github 操作基础。  
:::

**PPX** 已经预先写好了 `.github/workflows/main.yml` 文件。

```yaml
name: build
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    steps:
      - name: 拉取项目代码
        uses: actions/checkout@v4

      - name: 安装node环境
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: 安装pnpm
        uses: pnpm/action-setup@v4
        id: pnpm-install
        with:
          version: 9
          run_install: false

      - name: 获取pnpm仓库目录
        id: pnpm-cache
        shell: bash
        run: |
          echo "STORE_PATH=$(pnpm store path)" >> $GITHUB_OUTPUT

      - name: 设置pnpm缓存
        uses: actions/cache@v4
        with:
          path: ${{ steps.pnpm-cache.outputs.STORE_PATH }}
          key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
          restore-keys: |
            ${{ runner.os }}-pnpm-store-

      - name: 安装Python3环境
        uses: actions/setup-python@v5
        with:
          python-version: "3.9"
          cache: "pip"

      - name: 初始化打包环境
        run: pnpm run init

      - name: 开始打包
        run: pnpm run build

      - name: 上传打包完成的程序包
        uses: actions/upload-artifact@v4
        with:
          name: Setup_${{ runner.os }}
          retention-days: 1
          path: build/*-*_*.*
```

将代码提交至 `Github` 后，在 `Actions` 下会自动生成三种系统的程序包。

#### 打包后程序白屏的一些解决方案

**PPX** 显示 GUI 窗口的本质是显示 HTML 页面，因此出现白屏现象极有可能是系统不支持正常显示 HTML 页面。

一般情况下，macOS 不会出现白屏。在 Windows 系统下出现白屏，可以按以下步骤排查：

- 确保底层依赖软件已经正确安装

  - [.NET Framework](https://dotnet.microsoft.com/zh-cn/download/dotnet-framework) 软件版本需大于 4.0
  - [WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) 本地电脑能支持的最新版本

- 使用 CEF 模式打包

  CEF 模式打包本质上是内置一个 Chrome v66 的浏览器，用于支持显示 HTML 页面。

  ```shell
  pnpm run build:cef
  ```

### 数据库迁移

在 api/db/models.py 中修改数据库格式后，执行以下命令迁移数据库。

注意：迁移数据库前，需要对 sqlalchemy 数据库对象映射框架有所了解。

```
# 迁移数据库
m=备注迁移信息 pnpm run alembic
```

### HMR 原理

- 使用 npm-run-all 并行启用 vite(自带热更新) 和 pywebview
- 使用 nodemon 监听 `api/*` `pyapp/*` `main.py` 等文件，有修改自动重启应用，达到 HRM 效果

\*注：这里感谢 [WnagoiYy](https://github.com/WnagoiYy) 同学的 PR。

## 注意问题

- 在 Windows 系统下，只能打包 exe 等适用于 Windows 的程序，不能打包 mac 系统下的 app 程序。同理，mac 也是一样。(**不过，基于 Github Action 可实现同时打包三种安装包**)
- 在 Windows 系统下，请不要使用中文路径，否则可能会出现 cannot call null pointer pointer from cdata 'int(_)(void _, int)' 等错误信息。mac 系统无此问题。

## 历史版本

#### V5.1.0

- 修复打包成 Linux 系统程序中遇到的一些问题
- 将 Actions 自动生成的程序包拆分为 3 个不同系统的程序包，方便分批下载

#### V5.0.0

- 新增支持打包成 Linux 系统可用的程序（仅测试 Ubuntu 22.04.2 版系统）
- pywebview 模块升级到 5.2
- pyinstaller 模块升级到 6.10.0

#### V4.4.0

- Python 的安装源由[清华源](https://pypi.tuna.tsinghua.edu.cn/simple)改为[中科大源](https://pypi.mirrors.ustc.edu.cn/simple/)。
- 在 win 系统下，执行 `pnpm run build` 打包命令时，PPX 会先生成文件夹式程序（而非是先打包成一个 exe 程序），再打包成安装程序。经测试，打包成文件夹式程序比打包成一个 exe 程序的运行速度会更快些。
- 明确 `Config.codeDir` 为代码根目录，一般情况下，也是程序所在的绝对目录（但在 build:pure 打包成的独立 exe 程序中，codeDir 是执行代码的缓存根目录，而非程序所在的绝对目录）；明确 `Config.appDataDir` 为电脑上可持久使用的隐藏目录。更多细节请查看 `pyapp/config/config.py` 中的【系统配置信息】部分。

#### V4.3.0

- 修复某些情况下，打包后软件打开白屏的问题。（[pull#50](https://github.com/pangao1990/PPX/pull/50)）

#### V4.2.2

- 修复在 win 系统下，设置中文软件名时，打包找不到正确路径的问题。

#### V4.2.1

- 修复自带数据库存储变量命名错误的问题（[issues#33](https://github.com/pangao1990/PPX/issues/33)）

#### V4.2.0

- 删除字节码加密功能（原因见[issues](https://github.com/pyinstaller/pyinstaller/pull/6999)）
- pywebview 模块升级到 4.4.1
- pyinstaller 模块升级到 6.2.0

#### V4.1.0

- 修复某些情况下，自动检测软件升级失效的问题
- 访问网络资源的库由 requests 改为 httpx
- pywebview 模块升级到 4.1
- pyinstaller 模块升级到 5.10.1

#### V4.0.1

- 修复 python 创建 venv 虚拟环境时，pip 不是最新版的问题

#### V4.0.0

- 新增 MacOS 环境打包成 .dmg 安装包，Windows 环境打包成 .exe 安装包（基于 Github Action 可实现同时打包两种安装包）
- 新增自动检测软件升级
- 改 npm 为 pnpm ，节省磁盘空间并提升安装速度
- 项目正式改名为 PPX

#### V3.1.1

- 解决数据库操作时，session 冲突的问题
- 修复了一些已知问题

#### V3.1.0

- 优化数据迁移

#### V3.0.0

- 新增 SQLite 数据库支持，使用 sqlalchemy 进行 ORM 操作，使用 alembic 进行数据迁移与映射
- 新增 static 静态文件夹，可以存放 cache 缓存、db 数据库等，这些文件都将被直接打包到程序包中
- 新增 python 调用 js 函数的示例
- 在 config.py 中新增配置信息，如代码所在绝对目录等
- 修复 python 代码无法打印日志的问题
- 构建程序包时，实时更新打包配置文件 spec
- 调整项目文件夹结构
- pywebview 模块升级到 4.0

#### V2.0.0

- 将 Vue3 框架整体分离至 gui 文件夹，如此一来，你可以随意替换 gui 文件夹下的前端框架，使用 Vue、React、Angular、HTML ，或者你喜欢的其他框架均可
- 整理框架结构，优化代码逻辑

#### V1.3.0

- 新增热更新

#### V1.0.0

- 初始版本

---

<br/>

## 打赏 🥰🥰🥰

<div style="margin-top:20px">
  <div style="margin-bottom:10px;">如果这款应用对你有帮助，或者想给我微小的工作一点点资瓷，请随意打赏。</div>
  <table rules="none">
	  <tr>
		  <td align="center">
			  <img src="https://blog.pangao.vip/images/wechatpay.jpg" alt="潘高 微信支付" style="width:240px; height:240px;" />
			  <br/>
			  <font color="#159718">微信支付</font>
		  </td>
		  <td align="center">
			  <img src="https://blog.pangao.vip/images/alipay.png" alt="潘高 支付宝" style="width:240px; height:240px;" />
			  <br/>
			  <font color="#217cfb">支付宝</font>
		  </td>
	  </tr>
  </table>
  </div>
</div>

---

<br/>

## 致谢 🥳🥳🥳

本应用自开源以来，获得了很多人的支持。

这离不开各位小伙伴的赞赏、意见和 PR，感谢你们！

我会朝着 **加速软件开发向开源运动转变** 的理念，继续前进。

### 🍄 Rewarders

|     昵称     |   金额   |              备注              |
| :----------: | :------: | :----------------------------: |
|    \*\*亮    |  100 元  | 感谢 PPX 项目，小小支持一下 ✊ |
|  jackiexiao  | 16.66 元 |           PPX yes！            |
|  Karinyooo   |  512 元  |        天使投资，哈哈！        |
|     XXX      |  100 元  |                                |
|      mQ      |  50 元   |           PPX 加油！           |
|     min      | 6.66 元  |                                |
|      mQ      |  100 元  |         帮助了许多东西         |
|   icebear    |  30 元   |                                |
|   icebear    |  100 元  |                                |
|     mlw      |  11 元   |                                |
|   veteran    |   5 元   |                                |
|      ly      |   1 元   |                                |
|   漫倦彧翾   |   1 元   |                                |
| 潘多拉的盒子 |   5 元   |                                |
|   Shirley    | 6.66 元  |                                |
|     夏林     |   2 元   |                                |
|     曾姐     |   5 元   |                                |

### 🍄 Stargazers

[![Stargazers](https://reporoster.com/stars/pangao1990/PPX)](https://github.com/pangao1990/PPX/stargazers)

### 🍄 Forkers

[![Forkers](https://reporoster.com/forks/pangao1990/PPX)](https://github.com/pangao1990/PPX/network/members)

---

更多编程教学请关注公众号：**潘高陪你学编程**

![image](https://blog.pangao.vip/pic/潘高陪你学编程.jpg)

---

<br/>
<p align="center">
  <a href="https://github.com/pangao1990/PPX#">
    <img src="http://randojs.com/images/backToTopButton.png" alt="Back to top" height="29"/>
  </a>
</p>
