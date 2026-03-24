gitのブランチ移動を簡単にする
==============================

.. post:: 2023-11-15
   :tags: ShellScript, Git, ツール, 便利ツール
   :author: sion908
   :language: ja
   :location: blog/2023

はじめに
--------

gitでバージョン管理をしている
GUIの操作を覚えたくないのでCLIでやろうとするが長くなりがちなブランチ名をいちいちコピペするのもめんどくさい
というところで、ブランチの移動とやりたいときはマージまでコマンドで簡単にできないかとシェルスクリプトを作成した。
これでブランチの移動にストレスがなくなりました
`./bashrc`への追加でさらに使いやすくなります
何か意見改善点あればぜひ教えてください！！

制作品
------

### 完成品

.. code-block:: shell

   #!/bin/bash

   # helpの表示
   if [ "$1" = '-h' ]; then
     echo 'usage gcn <opt> <num>'
     echo ''
     echo 'opt'
     echo ' -h show help'
     echo ' -m integrate before into after'
     echo ' -p pull the branch after move'
     echo 'num'
     echo ' input the branch num'
     exit 1
   fi
   
   branches=($(git for-each-ref --format='%(refname:short)' refs/heads/))
   
   be_branch_name=($(git rev-parse --abbrev-ref HEAD))
   
   echo "Available branches:"
   for i in "${!branches[@]}"; do
     printf "%3d" "$i"
     echo ": ${branches[$i]}"
   done
   
   
   
   if [[ "$1" =~ ^[0-9]+$ ]]; then
     branch_number=$1
   else
     if [[ "$2" =~ ^[0-9]+$ ]]; then
       branch_number=$2
     else
       read -p "Enter branch number to checkout: " branch_number
   
       if [ -z "$branch_number" ] || [ $branch_number = "q" ]; then
         echo "Invalid branch number."
         exit 1
       fi
     fi
   fi
   
   af_branch_name=${branches[$branch_number]}
   echo "chosed branch: <" $af_branch_name ">"
   if [ -z "$af_branch_name" ]; then
     echo "Invalid branch number."
     exit 1
   else
     echo ">> git checkout $af_branch_name"
     git checkout $af_branch_name
   fi
   
   if [[ "$1" =~ [p] ]]; then
     # 引数がある場合は、引数の値を出力
     echo ">> git pull origin $af_branch_name"
     git pull origin $af_branch_name
   fi
   
   if [[ "$1" =~ [m] ]]; then
     # 引数がある場合は、引数の値を出力
     echo ">> git merge $be_branch_name"
     git merge $be_branch_name
   fi

### 使い方

.. code-block:: shell

   $ ./git_checkout_by_number.sh
   　　Available branches:
      0: develop
      1: feature/branch1
      2: feature/branch2
     Enter branch number to checkout:　１
     Switched to branch 'feature/branch1'

シェルスクリプトを実行するとブランチの一覧が表示され、数字を指定することで、そのブランチに移動することができる。
`./git_checkout_by_number.sh -m`
のように引数をとにかく何か入れることで、ブランチの移動をした後にその前にいたブランチがマージされる

スクリプトの説明
----------------

## ブランチの取得と表示

数字が二桁になっても揃うようにしている

.. code-block:: shell

   branches=($(git for-each-ref --format='%(refname:short)' refs/heads/))

   echo "Available branches:"
   for i in "${!branches[@]}"; do
     printf "%3d" "$i"
     echo ": ${branches[$i]}"
   done

## 入力の取得と例外処理

間違えた時とか用に入力なしまたは`q`を入力することで実行が止まるようにしている

.. code-block:: shell

   read -p "Enter branch number to checkout: " branch_number

   if [ -z "$branch_number" ] || [ $branch_number = "q" ]; then
     echo "Invalid branch number."
     exit 1
   fi

## ブランチの取得と`checkout`

移動先のブランチ名を取得し、あれば移動するようにする.
数字であれば範囲外のものを入れるとちゃんとエラーとなってくれるが、例えば`a`とか入れると0のブランチに飛ぶ
なぜ？？

.. code-block:: shell

   af_branch_name=${branches[$branch_number]}

   if [ -z "$af_branch_name" ]; then
     echo "Invalid branch number."
   else
     git checkout $af_branch_name
   fi

## マージの処理

あらかじめ取得してあった現在のブランチをマージするように
引数を指定してもいいが、表記揺れがあっても実行するように今回はとにかく引数があればこれが実行されることとした

.. code-block:: shell

   be_branch_name=($(git rev-parse --abbrev-ref HEAD))
   ...
   if [ $# -gt 0 ]; then
     # 引数がある場合は、引数の値を出力
     git merge $be_branch_name
   fi

`.bashrc`への登録
-----------------

gitは比較的どこでも使うので`./bashrc`に登録したほうが使いやすいです
いちいちプロジェクトごとに置いとくのもignoreするのもめんどいですしね
自分の場合は`git_checkout_by_number.sh`を`/usr/local/bin/mine/`において、
.bashrcに下記を追記しました。

.. code-block:: shell

   export PATH=/usr/local/bin/mine/:$PATH
   alias gcbn='git_checkout_by_number'

.. code-block:: shell

   $ gcbn

で利用できます

参考文献
--------

ごめんなさい
あったかもしれませんが忘れました
参考にした方ありがとうございました
