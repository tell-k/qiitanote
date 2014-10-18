# ぼくのかんがえたさいきょうのQiitaメモ

## 概要 

* ローカルでメモを取りつつカジュアルにQiitaに投稿できるようにしたい。
* メモはSphinxでbuildできて手元で参照しやすくしたい。
* Alfred + Dashでも検索できるようにしたい。
* メモはVimで書きたい。
* Markdown記法で書いてもいい。

という欲求を満たすための環境構築メモ

## やりたいことイメージ図

![やりたいことイメージ図](http://dl.dropbox.com/u/540566/Screenshots/ixele0t~kyy~.png)

1. Markdownで色々メモる
2. Sphinxでbuildする
3. Sphinxドキュメントをブラウザで見れる
4. Kobitoとファイル連携しつつ、KobitoからQiitaに投稿
5. SphinxドキュメントをAlfred+Dashから素早く検索

## 環境

* OS X Marverics
* Python2.7

 * virtualenv(virtualenvwrapper)
 * pip
 * Sphinx

* homebrew
* Pandoc
* Apache
* Kobito.app
* Dash.app
* Alfred.app

## 準備

なにわともあれSphinxプロジェクトを用意

```
$ mkvirtualenv qiitanote # virualenvwrapperを使ってる

(qiitanote)$ pip install Sphinx
(qiitanote)$ mkdir qiitanote
(qiitanote)$ cd qiitanote
(qiitanote)$ sphinx-quickstarpt 

# 対話で色々きかれるのでポチポチ答えると作成おわり

# make htmlしてみる
(qiitanote)$ make html

# _build/html/以下にHTMLドキュメントが生成される
# ApacheでVirtualhostを切って、http://qiitanote.dev/ で_build/html以下を見れるようにしている

# ドキュメントの確認(Chromeが開く)
(qiitanote)$ open -a Google\ Chrome.app  http://qiitanote.dev
```

初期ディレクトリ構成

```
qiitanote
├── Makefile
├── _build
│   ├── doctrees
│   └── html <- ここにHTMLが生成される
├── _static
├── _templates
├── conf.py <- Sphinxの設定ファイル
└── index.rst
```

## Markdownで書く

* Sphinxは基本reStructuredText記法で文章を書くが、Qiitaへの投稿を考えてMarkdownで書くようにする。
* MarkdownのテキストもSphinxでビルドできるように、下記リンクの拡張を利用する。
* [Sphinx 文書に markdown フォーマットを利用する](http://tk0miya.hatenablog.com/entry/2012/12/19/233642)

Pandocのインスコ

```
(qiitanote)$ brew install pandoc
```

拡張の設定

```python
# conf.py を書き換える

# 以下の内容を追記
PROJECT_DIR = os.path.dirname(__file__)
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, "libs"))  # libs以下に拡張スクリプト設置
extensions += ["sphinxcontrib_markdown"]

markdown_title = 'Qiita Note'
source_suffix = '.md'
```

適当に.mdファイルを作って書いてみる

```
(qiitanote)$ touch fisrtnote.md
```

中身

```markdown
# My First Qiita Memo!!!

## 1. Hoge

hogehogehogehoge
hogehogehogehoge

## 2. Fuga

fugafugafugafuga
fugafugafugafuga
```

ビルド

```
(qiitanote)$ make html
```

結果

![Mifirst Qiita Memo](https://dl.dropboxusercontent.com/u/540566/Screenshots/bxvy-clb_9nm.png)

## Kobitoと連携させる

Qiitaに投稿するためにKobitoとファイル連携をさせる

* [Kobito v1.7.0リリース: コマンドラインからファイルを連携できるようになりました!](http://blog.qiita.com/post/59062715100/kobito-v1-7-0-release)

```
(qiitanote)$ open -a Kobito firstnote.md
```

* Kobitoが開いてファイル連携される。そのまま「Qiitaに投稿」を押せば投稿できる
* vimで編集した内容がリアルタイムでKobitoで見れるのは地味に嬉しい。逆にKobitoで編集した内容はmdファイルに反映される。
* 毎回連携コマンド叩くのは面倒なのでmake htmlした時に自動で連携させる。
* .mdファイルをさらって連携コマンドを叩きまくるスクリプトを作る

```python
# -*- coding: utf-8 -*-

import os
import time
import subprocess

TARGET_DIR = os.path.join(os.path.dirname(__file__), '..')
cmd = "open --hide -g -a Kobito {}"

# start Koibito.app
subprocess.call(cmd.format(""), shell=True)
time.sleep(3)

# associate .md file to Koibito.app
for root, dirs, files in os.walk(TARGET_DIR):
    for f in files:
        if f.endswith(".md"):
            f = os.path.abspath(os.path.join(root, f))
            subprocess.call(cmd.format(f), shell=True)

# hyde Kobito.app
subprocess.call(
    "osascript -e 'tell application \"Finder\"'"
    " -e 'set visible of process \"Kobito\" to false'"
    " -e 'end tell'",
    shell=True
)
```

* 「libs/associate_kobito.py」などとして保存
* Kobitoを起動してない状態で、連携コマンドを叩くとKobitoに二重登録されるので最初に起動してちょっと待ってる
* make htmlするたびにKobitoが前面に出るのがウザいので、終わったらWindowを隠してる

「make html」した時にこのスクリプトを実行するようにする

```Makefile
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	python libs/associate_kobito.py  # <= 追加
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
```

これでビルドすると勝手にKobitoにメモが現れる。

ここまでの構成

```
qiitanote
├── Makefile
├── _build
│   ├── doctrees
│   └── html
├── _static
├── _templates
├── conf.py
├── firstnote.md
├── index.md # <-追加
├── index.rst
└── libs
    ├── associate_kobito.py # <- 追加
    └── sphinxcontrib_markdown.py # <- 追加
```

## Alfred + Dash で検索する

折角書いたメモなので手元で簡単に検索したい。AlfredとDashを使って検索する。AlfredもDashも有料版買った。

* [Alfredとdashで超高速リファレンス - SlideShare](http://www.slideshare.net/duffytoy1/alfreddash)
* 設定は割愛

sphinxcontrib-dashbuilder を使うとSphinxドキュメントを簡単にDash用のDocsetにできる

* [sphinxcontrib-dashbuilder 0.1.0](https://pypi.python.org/pypi/sphinxcontrib-dashbuilder/0.1.0)

インストール

```
(qiitanote)$ pip install sphinxcontrib-dashbuilder
```

設定ファイル変更

```python 
# conf.py
extensions += ["sphinxcontrib_markdown", "sphinxcontrib.dashbuilder"]
dash_name = 'QiitaNote'
dash_icon_file = '_static/qiita.png' # <- faviconは適当にQiitaから持って来た
```

Makefileの書き換え

```Makefile
# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build
DOCSETSDIR    = ~/Library/Application\ Support/Dash/DocSets/QiitaNote # <- 追加

〜省略〜

# .PHONYにもdashを追加
.PHONY: dash help ... 

〜省略〜

# dashターゲットを追加
dash:
	$(SPHINXBUILD) -b dash $(ALLSPHINXOPTS) $(DOCSETSDIR)
	@echo
	@echo "Build finished. The Docset are in $(DOCSETSDIR)."
```

ビルド

```
(qiitanote)$ make dash
```

Dashで確認する。Dashの設定画面 > Docsets > Rescan ボタンを押す

![ReScan](http://dl.dropbox.com/u/540566/Screenshots/g0wi094zvvow.png)

DashのDocsetsにQiitaNoteが現れる

![Dashの画面](https://dl.dropbox.com/u/540566/Screenshots/0ytqb%7Eoy-_ax.png)

毎回「make dash」を打つのも面倒なので「make html」の時にもdashをビルドする。

```Makefile
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	$(SPHINXBUILD) -b dash $(ALLSPHINXOPTS) $(DOCSETSDIR) # <- 追加
	python libs/associate_kobito.py  
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
```

### Alfredで検索できない

* このままだと例えば見出しのHogeとかAlfredから検索できない。
* Dashは、DocSetsのDBファイル(sqlite)から検索用インデックスを検索してる。
* dashbuilderはreSTのindexをさらって、DBファイル(sqlite)を書き出してる。
* つまりreSTのindexが必要

Markdown -> reST変換時に見出しを強制的にindexにする。

```markdown
## Hoge

## Fuga 
```

こういう見出しがあるとする。 reSTに変換した時に下記のようにする。

```reStructuredText
.. index:: Hoge

Hoge
----

.. index:: Fuga

Fuga
----
```

libs/sphinxcontrib_markdown.py に下記処理を追加する。

```python
48  # insert index directive                                                                
49  newlines = []                                                                           
50  for line in source[0].split(u"\n"):                                                     
51      if self._is_heading_line(line):                                                     
52          prev = newlines[-1]                                                             
53          inedexline = u".. index:: {0}\n".format(prev)
54          newlines.insert(-1, inedexline)                                                 
55      newlines.append(line)
56  source[0] = "\n".join(newlines)
```

これで再度ビルドするとAlfredから見出しが検索できる

![Alfred検索](http://dl.dropbox.com/u/540566/Screenshots/in30plofu0-8.png)

ここまでの構成

```
qiitanote
├── Makefile
├── _build
│   └── doctrees
├── _static
│   └── qiita.png # <- 追加
├── _templates
├── conf.py
├── firstnote.md
├── index.md
├── index.rst
└── libs
    ├── associate_kobito.py
    └── sphinxcontrib_markdown.py
```

## Sphinxドキュメントの見た目を変える

* Qiitaぽい色見にしたい
* dashbuilderでdashに入れるとSphinxの検索が無効になる？-> 左カラムいらね。

拙作のsphinxテーマを利用する。

```
(qiitanote)$ pip install sphinxjp.themes.basicstrap
```

設定を変える

```python
# conf.py

extensions += ["sphinxcontrib_markdown", "sphinxcontrib.dashbuilder", 'sphinxjp.themes.basicstrap']
html_theme = 'basicstrap'
html_theme_options = {
    'noheader': True,

    'header_inverse': True,
    'relbar_inverse': True,

    'inner_theme': True,
    'inner_theme_name': 'bootswatch-sandstone',
}
```

ビルド

```
(qiitanote)$ make html
```

結果

![Qiita風](http://dl.dropbox.com/u/540566/Screenshots/3aah6a2-s9kk.png)

## 成果物

多少書いてある事と違いますが、Githubに置きました。ご査収ください。

https://github.com/tell-k/qiitanote

## TODO

* oktavia導入して検索できるようにしたい

## まとめ

* Qiitaに書くのはこれからなんですけどね。
* ほとんどQiitaと関係ないことばかりを書いたような気がする
* あとはぼくのやる気待ち。

## 追記(2014/10/18)

* ついさっきKobitoを2.0にアップグレードしたら「ファイル連携機能は一時的に無効にされています」という履歴が出て、早々に破綻した。。。かなしい

