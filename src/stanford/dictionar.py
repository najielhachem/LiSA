import numpy as np

def getDictionnary(lines, n):
  dic = {}
  arr_dic = []
  i = 1
  for line in lines:
    words = line.split()
    for word in words:
      if(word in dic):
        arr_dic[dic[word]] = (arr_dic[dic[word]][0], arr_dic[dic[word]][1] + 1)
      else:
        dic[word] = i
        arr_dic.append((word, 0))
        i = i + 1
  arr_dic = np.array(arr_dic)
  idx = np.argsort(arr_dic[:,1])
  arr_dic = arr_dic[idx]
  arr_dic = arr_dic[::-1]
  arr_dic = arr_dic[:n]
  dic= {arr_dic[i][0]:i for i in range(len(arr_dic)) }
  return dic

def vectorizeText(dic,text):
   vec = np.zeros(len(dic))
   for word in text.split():
     if (word in dic):
       vec[dic[word]] = 1
   return vec
    
   
      
        
