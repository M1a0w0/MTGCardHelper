# MTGCardHelper
###### A tool that can help you easily download the [Magic The Gathering (MTG)](#external-link)'s card image.

[![license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/M1a0w0/MTGCardHelper/blob/main/LICENSE)
[![en-us](https://img.shields.io/badge/language-English-blue)](https://github.com/M1a0w0/MTGCardHelper/blob/main/README.md)
[![zh-cn](https://img.shields.io/badge/语言-简体中文-green)](https://github.com/M1a0w0/MTGCardHelper/blob/main/README_zh-cn.md)

## downloadCardImg_V1.py
#### This is my first attempt that try to download the MTG's card image by batch.
- It is dependent on [Scryfall](#external-link)

## downloadCardImg_V2.py
- It is dependent on [Scryfall API Documentation](#external-link)
### Usage
- Install requirements
```text
pip install -r requirements.txt
```
- Before you run `downloadCardImg_V2.py`, change the path variable on `line 31` `line 32`

## MTG Card Helper.html
#### It provides a GUI that can make you more easily to use. It can be used as long as you have a browser(recommend Microsoft Edge).
### Usage
- Just download this file, then open it on your browser.
### Details
- About the `https://api.scryfall.com/cards/` on top of the page. For usual, you don't need to change it. It is Scryfall's API.
- For the Languages Code, refer to [Scryfall Languages](https://scryfall.com/docs/api/languages). Please use `CODE` instead of `PRINTED CODE`. You can search the card on more than one language. Between Code and Code, use `,` to separate. Example: `zhs,en`
- After fill in `deck list` and `Languages Code`, click `searchCard`.
- About the checkbox before title `cardName`, it can select all result.
- About the button `copySelected`, it can copy all selected result's card image uri to your clipboard.
- `hasToken` = true means this card has token.
- Click card's name, it can jump to this card's scryfall page.
- About the button `previewCard`, it can show you image about this card.

## License
See the `LICENSE` file for details. In summary, MTGCardHelper is licensed under the `MIT license`.

#### External Link
> [Magic The Gathering (MTG)](https://magic.wizards.com/)

> [Scryfall](https://scryfall.com)

> [Scryfall API Documentation](https://scryfall.com/docs/api)