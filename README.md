# DeepOne汉化工具


> [!待获取列表]  
>
> 680012_1(アントリ 特典 memoriral)


汉化方法参考了这个IrisMysteria的仓库[IrisMysteria-Translate](https://github.com/game-reverse/IrisMysteria-Translate)  
汉化工具使用的[GalTransl](https://github.com/cx2333-gt/GalTransl)

[redirector扩展地址](https://chromewebstore.google.com/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd)  
[gooreplacer扩展地址](https://chromewebstore.google.com/detail/gooreplacer/jnlkjeecojckkigmchmfoigphmgkgbip)

本地部署方法已弃用,请以前使用过本地部署补丁的切换到新版本。本地版本的相关代码依旧保留，想要自己替换文本的可以继续使用，但不负责维护了。

安卓客户端汉化实现请参看仓库 [DeepOne-Mod](https://github.com/anosu/DeepOne-Mod)

翻译人员：Atrili、mamomo、刚大木 、SK、科斯卡特

补丁制作：某江南的黎三金

特别鸣谢：518、红凯、anosu

汉化文件1周年及以前剧情、角色来自已关服的繁中服  
主线的第七章及往后，来自上述人员的汉化  
其余内容使用了GPT4/claude +GPT3.5 +deepseek进行汉化  

该补丁仅供交流学习，不得用于任何盈利行为。请于下载后24小时内删除。
有问题可以留issue,或者去QQ交流群927910543  


### 2025.2.4
更新之后项目改为使用游戏里的project.js重定向，不再需要更新浏览器扩展的规则
感谢anosu重写的project.js，具体代码参看js/project.js
从本次更新开始使用deepseek-v3进行翻译

### 2025.2.18
由于剧本获取接口的变动，导致现在少数氪金剧本无从获得，现在仓库readme页面添加一个待获取剧本列表，如果你有待获取剧本列表中的卡，并且愿意帮助我们，请在issue区留言


## [使用说明](https://lisanjin.github.io/DeepOne_translate_CN/)

### gooreplacer使用说明
1.在浏览器安装[gooreplacer扩展地址](https://chromewebstore.google.com/detail/gooreplacer/jnlkjeecojckkigmchmfoigphmgkgbip)  

2.打开gooreplacer扩展,点击配置规则  
![](/image/gooreplacer-2.png) 

3.点击在线规则，点击配置，输入https:/lisanjin.github.io/DeepOne_translate_CN/gooreplacer.json  
点击确认后，立刻更新  
![](/image/gooreplacer-3.png)  

**因为gooreplacer更新，上述流程在新版gooreplacer不再可以用，请使用下面的流程**  

1.在浏览器安装[gooreplacer扩展](https://chromewebstore.google.com/detail/gooreplacer/jnlkjeecojckkigmchmfoigphmgkgbip)  

2.在gooreplacer的设置页面点击Edit
![](/image/gooreplacer-4.png)

3.填入以下规则，save  
```
^https:\/\/tonofura-r-cdn-client\.deepone-online\.com\/client\/[0-9]+\.[0-9]+\.[0-9]+\/src\/project\.js,regex,redirect
url:https://lisanjin.github.io/DeepOne_translate_CN/js/project.js
```

### redirector使用说明

1.下载重定向字典<https://lisanjin.github.io/DeepOne_translate_CN/Redirector_online.json> (使用你的下载工具下载，或者在浏览器点击[这个链接](Redirector_online.json)后，按ctrl+s保存到本地)  

![](/image/1.png)

2.在浏览器安装[redirector扩展](https://chromewebstore.google.com/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd)（如果你使用过之前本地版本，即导入过Redirector.json的，请卸载重装  

手机请下载火狐浏览器后，安装[redirector附加组件](https://addons.mozilla.org/zh-CN/android/addon/redirector/)  

![](/image/2.png)  

![](/image/2-2.png)

3.打开redirector扩展，点击edit redirects，点击import导入在第一步下载的文件  

![](/image/3.png)
![](/image/3-2.png)
![](/image/3-3.png)

4.完成，打开游戏，手机请使用[sp版本的网页端](https://sp-play.games.dmm.co.jp/play/deeponer/)。如果需要切换回日语，打开redirector扩展后，点击disable redirector按钮即可

