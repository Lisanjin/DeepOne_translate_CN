# DeepOne汉化工具

## 概述

翻译进度/待供档资源请查看[翻译状态](https://collect.deeponer.online/)

汉化翻译工具使用的[GalTransl](https://github.com/cx2333-gt/GalTransl)

本地部署方法已弃用,请以前使用过本地部署补丁的切换到新版本。本地版本的相关代码依旧保留，想要自己替换文本的可以继续使用，但不负责维护了。

安卓客户端汉化实现请参看仓库 [DeepOne-Mod](https://github.com/anosu/DeepOne-Mod)

翻译人员：Atrili、mamomo、刚大木 、SK、科斯卡特

补丁制作：某江南的黎三金

特别鸣谢：518、红凯、anosu

汉化文件1周年及以前剧情、角色来自已关服的繁中服  
主线的第七章及往后，来自上述人员的汉化  
其余内容使用了GPT4/claude +GPT3.5 +deepseek进行汉化

该补丁仅供交流学习，不得用于任何盈利行为。请于下载后24小时内删除。
有问题可以留issue,或者去[QQ交流群](https://qm.qq.com/q/rYyJ493WYo)

## 更新说明

### 2025.2.4

更新之后项目改为使用游戏里的project.js重定向，不再需要更新浏览器扩展的规则  
感谢anosu重写的project.js，具体代码参看js/project.js  
从本次更新开始使用deepseek-v3进行翻译

### 2025.2.18

由于剧本获取接口的变动，导致现在少数氪金剧本无从获得，现在仓库readme页面添加一个待获取剧本列表，  
如果你有待获取剧本列表中的卡，并且愿意帮助我们，请在issue区留言

### 2025.8.20

添加了一个规则，对dmm版（全年龄版）进行支持

### 2026.3.17

现在汉化由工作流自动进行，可以通过(https://collect.deeponer.online/) 查看翻译进度或是进行供档。

## [使用说明](https://lisanjin.github.io/DeepOne_translate_CN/)

### gooreplacer使用说明

1.在浏览器安装[gooreplacer扩展](https://chromewebstore.google.com/detail/gooreplacer/jnlkjeecojckkigmchmfoigphmgkgbip)

2.在gooreplacer的设置页面点击Edit
![](/image/gooreplacer-4.png)

3.填入以下规则，save

```
^https:\/\/tonofura-r-cdn-client\.deepone-online\.com\/client\/[0-9]+\.[0-9]+\.[0-9]+\/src\/project\.js,regex,redirect
url:https://lisanjin.github.io/DeepOne_translate_CN/js/project.js

^https:\/\/tonofura-w-cdn-client\.deepone-online\.com\/client\/[0-9]+\.[0-9]+\.[0-9]+\/src\/project\.js,regex,redirect
url:https://lisanjin.github.io/DeepOne_translate_CN/js/project.js
```
