[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

這個應用主要是在執行圖片的Shading算法。  
可以判斷影像的光源是否分布不均的現象。

## 概念

> 此處**Y**值一率採用灰偕值來作計算

1. 規範中央Y值的範圍、四個角落Y值的PassLevel、以及四個角落對於中央Y值的對比值。  
  > Qualified Condition
  > * centerLow <= Center average gray value <= centerUP
  > * PassLow <= Gray value at corners (percentage) <= PassUP
  > * The difference between maximum and minimum gray values at corner should be less than or equal to **Diff**.  
  
2. 在中央區域找尋最大**Y**值的ROI。
3. 中央的**Y**值與四個角落的Y值作比較。
4. 四個角落**Y**值差異在一定範圍內。

## 輸入條件

- input_file: 欲檢測的圖片
- partition_n: 欲評比的中央區域，其邊長與該影像之長度比。(若n=2, 意思就是中央檢測區域會是 1/2 * 1/2)
- ROI: 有興趣的範圍，default value為 1/10 * 1/10

**目前設定:**

> _parameters_
> input_file = '19271_en_1.jpg'
> partition_n = 2
> ROI = (1/10, 1/10)

## 合格條件設定

> **Qualified Condition**
> * 100 <= Center average gray value <= 220
> * 70 <= Gray value at corners (percentage) <= 100
> * The difference between maximum and minimum gray values at corner: 20.


## 結果

[result_img](未完成上傳)
