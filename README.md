# FILL IN ACTIVITY RECORD!!
## Install  
まずvimは神なので、vimを入れます  
~~~
$ sudo apt-get install vim
~~~
次に、以下のコマンドをターミナルに打ち込んでいきます
~~~
$ git clone https://github.com/OkanoShogo0903/fill_in_activities
$ cd vim
$ conda env export > fill_in.yaml
~~~
次に、(このサイト)[http://vaaaaaanquish.hatenablog.com/entry/2017/06/06/194546]を見て、この通りにインストールしましょう

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
