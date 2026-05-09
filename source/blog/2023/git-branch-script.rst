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
``./bashrc`` への追加でさらに使いやすくなります
何か意見改善点あればぜひ教えてください！！

制作品
------

完成品
^^^^^^

.. code-block:: shell

   #!/usr/bin/env bash

   set -u

   show_help() {
     cat <<'EOF'
   usage: gcn [options] [branch_number]

   options:
     -h  show help
     -p  pull the target branch after switch
     -m  merge previous branch into target branch after switch
     -d  delete previous branch after switch (confirmation required)

   examples:
     gcn 3
     gcn -p 2
     gcn -md 5
     gcn -mpd 1
   EOF
     exit 0
   }

   confirm_delete() {
     local branch_name="$1"

     echo
     echo "Delete previous branch: ${branch_name}"
     read -r -p "Type 'yes' to delete this branch: " answer

     [ "$answer" = "yes" ]
   }

   is_protected_branch() {
     local branch_name="$1"

     case "$branch_name" in
       main|master|develop|development)
         return 0
         ;;
       *)
         return 1
         ;;
     esac
   }

   sort_branches() {
     local prioritized=(
       main
       master
       develop
       test
       staging
       clientdemo1
     )

     local sorted=()
     local branch
     local p
     local found

     for p in "${prioritized[@]}"; do
       for branch in "${branches[@]}"; do
         if [ "$branch" = "$p" ]; then
           sorted+=("$branch")
           break
         fi
       done
     done

     for branch in "${branches[@]}"; do
       found=0
       for p in "${prioritized[@]}"; do
         if [ "$branch" = "$p" ]; then
           found=1
           break
         fi
       done

       if [ "$found" -eq 0 ]; then
         sorted+=("$branch")
       fi
     done

     branches=("${sorted[@]}")
   }

   switch_branch() {
     local target_branch="$1"

     echo ">> git switch $target_branch"
     git switch "$target_branch"
   }

   pull_branch() {
     local target_branch="$1"

     echo ">> git pull origin $target_branch"
     git pull origin "$target_branch"
   }

   merge_previous_branch() {
     local previous_branch="$1"

     echo ">> git merge $previous_branch"
     git merge "$previous_branch"
   }

   delete_previous_branch() {
     local previous_branch="$1"

     if is_protected_branch "$previous_branch"; then
       echo "Refusing to delete protected branch: $previous_branch"
       return 1
     fi

     if confirm_delete "$previous_branch"; then
       echo ">> git branch -d $previous_branch"
       git branch -d "$previous_branch"
     else
       echo "Canceled branch deletion."
     fi
   }

   # option flags
   do_pull=0
   do_merge=0
   do_delete=0

   while getopts ":hpmd" opt; do
     case "$opt" in
       h)
         show_help
         ;;
       p)
         do_pull=1
         ;;
       m)
         do_merge=1
         ;;
       d)
         do_delete=1
         ;;
       \?)
         echo "Invalid option: -$OPTARG"
         echo
         show_help
         ;;
     esac
   done

   shift $((OPTIND - 1))

   mapfile -t branches < <(git for-each-ref --format='%(refname:short)' refs/heads/)
   if [ "${#branches[@]}" -eq 0 ]; then
     echo "No local branches found."
     exit 1
   fi

   sort_branches

   before_branch="$(git rev-parse --abbrev-ref HEAD)"

   echo "Available branches:"
   for i in "${!branches[@]}"; do
     printf "%3d: %s\n" "$i" "${branches[$i]}"
   done

   if [ $# -ge 1 ]; then
     branch_number="$1"
   else
     read -r -p "Enter branch number to switch: " branch_number
   fi

   if [ -z "${branch_number:-}" ] || [ "$branch_number" = "q" ]; then
     echo "Canceled."
     exit 1
   fi

   if ! [[ "$branch_number" =~ ^[0-9]+$ ]]; then
     echo "Invalid branch number: $branch_number"
     exit 1
   fi

   target_branch="${branches[$branch_number]:-}"

   if [ -z "$target_branch" ]; then
     echo "Invalid branch number: $branch_number"
     exit 1
   fi

   echo "chosen branch: <$target_branch>"

   if [ "$before_branch" = "$target_branch" ]; then
     echo "You are already on '$target_branch'."
     exit 1
   fi

   if ! switch_branch "$target_branch"; then
     echo "Failed to switch branch."
     exit 1
   fi

   if [ "$do_pull" -eq 1 ]; then
     if ! pull_branch "$target_branch"; then
       echo "Failed to pull branch: $target_branch"
       exit 1
     fi
   fi

   if [ "$do_merge" -eq 1 ]; then
     if ! merge_previous_branch "$before_branch"; then
       echo "Failed to merge branch: $before_branch"
       exit 1
     fi
   fi

   if [ "$do_delete" -eq 1 ]; then
     delete_previous_branch "$before_branch"
   fi

### 使い方

シェルスクリプトを実行するとブランチの一覧が表示され、数字を指定することで、そのブランチに移動することができる。

.. code-block:: shell

   $ ./git_checkout_by_number.sh
   　　Available branches:
      0: main
      1: develop
      2: feature/branch1
      3: feature/branch2
    Enter branch number to switch:	１
    >> git switch develop
    Switched to branch 'develop'

オプションを指定することで、移動後に追加の操作が可能です：

- `-p`: 移動後に `git pull` を実行
- `-m`: 移動前にいたブランチを移動先ブランチにマージ
- `-d`: 移動前にいたブランチを削除（確認あり）

.. code-block:: shell

   $ ./git_checkout_by_number.sh -p 2
   $ ./git_checkout_by_number.sh -md 3
   $ ./git_checkout_by_number.sh -mpd 1

スクリプトの説明
----------------

## オプション解析

`getopts` を使用してオプションを正しく解析します。

.. code-block:: shell

   while getopts ":hpmd" opt; do
     case "$opt" in
       h) show_help ;;
       p) do_pull=1 ;;
       m) do_merge=1 ;;
       d) do_delete=1 ;;
       \?) echo "Invalid option: -$OPTARG"; show_help ;;
     esac
   done

## ブランチの取得とソート

ローカルブランチを取得し、優先ブランチ（main, master, develop等）を先頭にソートします。

.. code-block:: shell

   mapfile -t branches < <(git for-each-ref --format='%(refname:short)' refs/heads/)
   sort_branches

## 入力の取得と例外処理

引数でブランチ番号が指定されない場合は対話的に入力を求めます。
入力なしまたは `q` を入力するとキャンセルされます。

.. code-block:: shell

   if [ $# -ge 1 ]; then
     branch_number="$1"
   else
     read -r -p "Enter branch number to switch: " branch_number
   fi

   if [ -z "${branch_number:-}" ] || [ "$branch_number" = "q" ]; then
     echo "Canceled."
     exit 1
   fi

## ブランチの移動

`git switch` を使用してブランチを移動します。
同一ブランチへの移動は防止します。

.. code-block:: shell

   if [ "$before_branch" = "$target_branch" ]; then
     echo "You are already on '$target_branch'."
     exit 1
   fi

   switch_branch "$target_branch"

## 保護されたブランチの削除防止

main, master, develop, development ブランチは削除対象から除外します。

.. code-block:: shell

   is_protected_branch() {
     case "$branch_name" in
       main|master|develop|development)
         return 0
         ;;
       *)
         return 1
         ;;
     esac
   }

``.bashrc`` への登録
-----------------------

gitは比較的どこでも使うので ``./bashrc`` に登録したほうが使いやすいです
いちいちプロジェクトごとに置いとくのもignoreするのもめんどいですね
自分の場合は ``git_checkout_by_number.sh`` を ``/usr/local/bin/mine/`` において、
.bashrcに下記を追記しました。

.. code-block:: shell

   export PATH=/usr/local/bin/mine/:$PATH
   alias gcn='git_checkout_by_number'

.. code-block:: shell

   $ gcn

で利用できます

参考文献
--------

ごめんなさい
あったかもしれませんが忘れました
参考にした方ありがとうございました
