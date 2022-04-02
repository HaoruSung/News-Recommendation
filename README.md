## WSM Project 1: Ranking by Vector Space Models
### Introduction
#### Run Program
```
python main.py --query <query> --type <type>
```
*  #### Tow Argument
   query :
   
   ```
   query : Here is an example result for the query
   ```
   
   type : 
   
   ```
   1 = Term Frequency (TF) Weighting + Cosine Similarity
   
   2 = Term Frequency (TF) Weighting + Euclidean Distance
   
   3 = TF-IDF Weighting + Cosine Similarity
   
   4 = TF-IDF Weighting + Euclidean Distance
   ```

* #### Sample  
```
python main.py --query 'Trump Biden Taiwan China' --type 1
```
#### Result
1. query: Trump Biden Taiwan China 
  type: 1 Term Frequency (TF) Weighting + Cosine Similarity

  ```
  python main.py --query 'Trump Biden Taiwan China' --type 1
  ```

  ![](https://i.imgur.com/R0jb3mr.png)

1. query: Trump Biden Taiwan China 
  type: 2 Term Frequency (TF) Weighting + Euclidean Distance

  ```
  python main.py --query 'Trump Biden Taiwan China' --type 2
  ```

  ![](https://i.imgur.com/TqWutF2.png)

1. query: Trump Biden Taiwan China 
  type: 3 TF-IDF Weighting + Cosine Similarity

  ```
  python main.py --query 'Trump Biden Taiwan China' --type 3
  ```

  ![](https://i.imgur.com/cM8MO5x.png)


1. query: Trump Biden Taiwan China 
  type: 4 TF-IDF Weighting + Euclidean Distance

  ```
  python main.py --query 'Trump Biden Taiwan China' --type 4
  ```

  ![](https://i.imgur.com/SSVbSui.png)