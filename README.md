# vim-bilibili-live

## 说明
这是一个可以让你在 Powerline 里看到 Bilibili 直播中的弹幕的插件

## 截图
![Screenshot1](../screenshot/1.jpg?raw=true)
![Screenshot2](../screenshot/2.jpg?raw=true)

## 安装

这个插件需要 [Powerline](http://github.com/powerline/powerline) 来工作。
不是 `vim-powerline` !

用你最喜欢的插件管理器

- [Pathogen](https://github.com/tpope/vim-pathogen)
  - `git clone https://github.com/feisuzhu/vim-bilibili-live ~/.vim/bundle/vim-bilibili-live`
- [Vundle](https://github.com/gmarik/vundle)
  - Add `Bundle 'https://github.com/feisuzhu/vim-bilibili-live'` to .vimrc
  - Run `:BundleInstall`
- [NeoBundle](https://github.com/Shougo/neobundle.vim)
  - Add `NeoBundle 'https://github.com/feisuzhu/vim-bilibili-live'` to .vimrc
  - Run `:NeoBundleInstall`
- [vim-plug](https://github.com/junegunn/vim-plug)
  - Add `Plug 'https://github.com/feisuzhu/vim-bilibili-live'` to .vimrc
  - Run `:PlugInstall`

之后你需要调整 Powerline 的主题配置。如果你没有折腾过，那么配置应该在这里：

> ~/.vim/bundle/powerline/powerline/config_files/themes/vim/default.json

找到 `powerline.segments.vim.plugin.tagbar.current_tag`, 把下面的加到前面：

>    {
>        "exclude_modes": ["nc"],
>        "function": "vim_bilibili_live.bilibili_live",
>        "draw_inner_divider": true,
>        "priority": 20
>    }

## 使用方法

比如你对 [http://live.bilibili.com/10920](http://live.bilibili.com/10920) 这个感兴趣，
那么 `:BilibiliLiveConnect 10920` 就可以订阅这个直播的弹幕了。
用 `:BilibiliLiveDisconnect` 关闭

## 协议
WTFPL
