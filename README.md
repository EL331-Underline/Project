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
```
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
```


select operation: searcher (データセットを作る操作に移動  
  |  
  _>   (searcher) select operation:   
         search word-token word (データセット内にあるすべてのdataからword が含まれる部分を探し前後１０単語を出力)  
                    (searcher) save result? (y/n): y (結果を保存　(今日の日付のファイルができる  



例
```
create dataset from dataset folder? (y/n): y
enter database name: aaaa
select operation: dataset
(dataset) enter path to database: aaaa
(dataset) select operation: retrieve-names
['K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K09', 'K10', 'Q']
(dataset) select operation: exit
select operation: searcher
(searcher) enter path to database: aaaa
(searcher) select operation: search word-token it
                        the a-posteriori Log likelihood Ratios (LLRs) of thetwo decoders. Then, it can be further utilised in the iterative processing. Since the 
                            low energy values forboth the 4PSK and 8PSK modulations. Therefore, it is reasonable to rely on the Shannon/SW limitcalculation using the 
                        If thetransmitter is acknowledged that the frame is correctly detected, it continues to transmit the nextdata frame. However, if error happens 
             such as real-time and resourceconstraints. In the existing object-oriented design, it is hardto deal with these constraints.In object-oriented developments, we analyze 
                           to model concurrentsystems. Vijay K. Garg and M.T. Ragunath proposed it asalgebraic descriptions of the language of Petri nets[1].There are many 
                                                      . We can omit the parentheses in a CRE if it doesnot become ambiguous. For example, we can simply writea* .b 
                             PCM Device Driver DevelopmentTo evaluate our approach and to apply it in the developmentof a real application, we developed the PCM 
                              calculating theoutput value of the channel. Once calc is invoked, it generatesthe output for 1 clock time.Synth is a synthesizer for 
                         for hardware clock. Synth is synchronized withclock signals. Each time it synchronizes, it synthesizedan output value from the output values of 

(searcher) save result? (y/n): y
(searcher) select operation: eixt
available operations: search, exit
(searcher) select operation: exit
select operation: exit
souhei@souhei-System-Product-Name:~/Project/src$ ls
000-20240531-1840-it  aaaa           consistency.py  main.py
__pycache__           comparison.py  dataset.py      searcher.py
```
select operation: consistency
 -> consistency) enter path to database: file_name
    (consistency) select operation: compare
    (consistency) save result? (y/n): y (save result)
```
create dataset from dataset folder? (y/n): y
enter database name: aaaa
select operation: consistency
(consistency) enter path to database: aaaa
(consistency) select operation: compare
| decorrelators,path-by-path                                                                                                     | x   | x   | x   | x   | x   | x   | x   | x   | x   | x   | o |
| decorrelators.111.                                                                                                             | x   | x   | x   | x   | x   | x   | x   | x   | x   | x   | o |
| decorrelators.In                                                                                                               | x   | x   | x   | x   | x   | x   | x   | x   | x   | x   | o |
| decorrelators.The                                                                                                              | x   | x   | x   | x   | x   | x   | x   | x   | x   | x   | o |
| decorrelators.Therefore,                                                                                                       | x   | x   | x   | x   | x   | x   | x   | x   | x   | x   | o |
| decorrelatorto                                                                                                                 | x   | x   | x   | x   | x   | x   | x   | x   | x   | x   | o |


(consistency) save result? (y/n): y


```





