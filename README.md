# Project
Project/src  フォルダ内で(ここ重要)
python src/main.py　で実行
create dataset from dataset folder? (y/n): y (データセットを作る,datasetフォルダに入っているデータがdatasetに格納される)
create dataset from dataset folder? (y/n): y (データセットを作らない
enter database name (datasetの名前を入力) 

select operation: dataset (データセットを作る操作に移動
  |
  _>   (dataset) select operation: 

        create 追加したいデータの相対パス　名前 (データセットにデータを追加
        retrieve name (データセット内に一致する名前を探しそのデータを出す
        retrieve-names  (データセットに登録されている名前一覧
        update old_name new_name (old_name の名前を new_name に変更
        delete name ((データセット内に一致する名前を探しそのデータを削除
例
create dataset from dataset folder? (y/n): y
enter database name: aaaa 
select operation: dataset
(dataset) enter path to database: aaaa
(dataset) select operation: retrieve-names
['K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K09', 'K10', 'Q']
(dataset) select operation: retrieve K01
TitleBICM-ID for Relay System Allowing Intra-linkErrors .............
(dataset) select operation: update K01 G01
None
(dataset) select operation: retrieve-names
['G01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K09', 'K10', 'Q']
(dataset) select operation: delete G01
None
(dataset) select operation: retrieve-names
['K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K09', 'K10', 'Q']
(dataset) select operation: create ../dataset/AnwarKhoiru1_20.txt K01
(dataset) select operation: retrieve-names
['K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K09', 'K10', 'Q', 'K01']

      
