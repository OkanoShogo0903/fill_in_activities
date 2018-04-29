# FILL IN ACTIVITY RECORD!!
このアプリケーション作るにあたってQiitaで記事書いたので、一応貼っとく  
[にょ](https://github.com/OkanoShogo0903/fill_in_activities)
## Install  
まずvimを入れます  
~~~
$ sudo apt-get install vim
~~~
次に、以下のコマンドをターミナルに打ち込んでいきます
~~~
$ git clone https://github.com/OkanoShogo0903/fill_in_activities
$ cd vim
$ conda env export > fill_in.yaml
~~~
次に、[このサイト](http://vaaaaaanquish.hatenablog.com/entry/2017/06/06/194546)を見て、この通りにインストールしましょう

## Hot Reference  
It is conda command 

* Export : 
~~~
$ conda env export > (EXPORT_NAME).yaml
~~~
* Inport : 
~~~
$ conda env create -f (EXPORT_NAME).yaml
~~~
* Create :
~~~
$ conda create -n py27 python=2.7 package_name
~~~
* Deleat :
~~~
$ conda env remove -n (EXPORT_NAME)
~~~

## TODO THINGS
- 初回起動時は、guiを立ち上げるか、localhostでなんかするかにして、フォームにいろいろいれてもらう
  - 学籍番号(ログインのため)
  - 大学のサイトにログインするためのパスワード(hash化して保存する?)
  - 初回使用時に必要なライブラリを入れてもらうためのPCのパスワード?
## Why?
kyassyu
https://www.regentechlog.com/2014/08/31/browsercookiejar/

## TODO
- アプリケーション版
  - GUI対応
  - notification.txtを作って、新しい機能とかをユーザに見やすくする
- 組み込み版
  - カメラを用いた顔認識
  - ラズパイ
    IntelのDNNスティック使ってTensorFlowとか動かすか??
  - Docker上でSQL運用
    複数人のパスワードを扱うためのSQL
    ハッシュとかどうこう
# ルール的な感じ
- 4/12 ~ 4/13とかはNG
- 年末やべぇよ...
- 他の人のコメント扱い方問題

