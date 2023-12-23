# 万智牌卡片助手
###### 一个可以帮助你批量下载 [万智牌](#外部链接) 卡片图片的工具。

[![license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/M1a0w0/MTGCardHelper/blob/main/LICENSE)
[![en-us](https://img.shields.io/badge/language-English-green)](https://github.com/M1a0w0/MTGCardHelper/blob/main/README.md)
[![zh-cn](https://img.shields.io/badge/语言-简体中文-blue)](https://github.com/M1a0w0/MTGCardHelper/blob/main/README_zh-cn.md)

## downloadCardImg_V1.py
#### 第一次尝试批量下载万智牌卡图。
- 它是基于 [Scryfall](#外部链接)

## downloadCardImg_V2.py
- 它是基于 [Scryfall API Documentation](#外部链接)
### 使用方法
- 安装依赖
```text
pip install -r requirements.txt
```
- 在你运行 `downloadCardImg_V2.py` 之前，请修改路径变量，在 `line 31` `line 32`

## MTG Card Helper.html
#### 它提供了一个GUI，更易于使用。而且只要你有浏览器就可以使用。
- 它只在 `Microsoft Edge` 上测试过
### 使用方法
- 只需下载此文件，然后在浏览器上打开它。
### 细则
- 关于在页面顶端的 `https://api.scryfall.com/cards/`。通常你不需要修改它。它是Scryfall的API。
- 关于 Languages Code，参考 [Scryfall Languages](https://scryfall.com/docs/api/languages)。 请使用 `CODE` 而不是 `PRINTED CODE`。你可以搜索多种语言的卡图。在 Code 与 Code 之间使用 `,` 隔开。举例：`zhs,en`
- 在填写 `deck list` 和 `Languages Code` 之后，单击 `searchCard`。
- 关于标题 `cardName` 之前的复选框，它可以选中所有的搜索结果。
- 关于按钮 `copySelected`，它可以复制所有选中的搜索结果的卡片图像链接到你的剪切板。
- `hasToken = true` 代表这张卡有衍生物。
- 单击卡片名称，可以跳转到相应卡片的Scryfall页面。
- 关于按钮 `previewCard`，可以预览关于该卡片的图片。
- 关于预览的图片，它是完整png，你可以直接保存而不用担心清晰度。

## 许可
查看 `LICENSE` 文件获取完整协议。万智牌卡片助手使用 `MIT license`。

#### 外部链接
> [万智牌](https://magic.wizards.com/)

> [Scryfall](https://scryfall.com)

> [Scryfall API Documentation](https://scryfall.com/docs/api)
