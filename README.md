# ipa_export
iOS一键打包脚本

使用时，请将脚本文件放在项目根目录下。与 xcproj文件在同一文件中。

ipa_adhoc.py 依赖 ipa_export.py
ipa_appstore.py 依赖 ipa_export.py

运行时请根据自己的实际情况修改  ipa_adhoc.py 和 ipa_appstore.py 中的配置参数。

运行以上两个脚本时，需要在命令行中传入一个参数。  'w'表示workspace    'p'表示 project

运行示例：
  ./ipa_adhoc.py w
