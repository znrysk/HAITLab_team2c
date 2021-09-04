import numpy as np
import pandas as pd
from scipy.optimize import lsq_linear
import codecs

def calc(food_id_list):

  df = pd.read_csv('nutrients_data_shaped.csv')
  df['food']=df['food'].str.replace('　', ' ')
  data=df[['NO','food','ENERC_KCAL','PROT-','FAT-','CHOAVLDF-','K','CA','MG','P','FE','ZN','CU','VITA_RAE','VITD','TOCPHA','VITK ','THIA','RIBF','NE','VITB6A','VITB12','FOL','PANTAC','VITC','FIB-','NACL_EQ']]

  data2= data[data['NO'].isin(food_id_list)]
  data2matrix=np.delete(data2.to_numpy(),[0,1],1).astype('float').T
  A=data2matrix
  B=np.array([2650,65,59,384,2500,800,340,1000,7.5,11,0.9,850,8.5,6.0,150,1.4,1.6,15,1.4,2.4,240,5,100,24,5]) 
  B=B*(1/3)
  data2_food_name = pd.DataFrame(data2['food'])
  data2_food_name.reset_index(drop=True, inplace=True)

  #食材量の上限と下限を設定します。
  df_ub = pd.read_csv('df_ub.csv')
  df_ub['ub (g)'] = df_ub['ub (g)'] * (1/100)

  lb = [0]*len(food_id_list)
  ub_tmp_df = df_ub[df_ub['food_id'].isin(food_id_list)]
  ub = ub_tmp_df['ub (g)'].tolist()

  lsqL_res = pd.DataFrame((lsq_linear(A,B,bounds=(lb,ub)).x)*100)
  lsqL_res[lsqL_res[0]<0.001]=0
  data2_need_nutrients_amount = pd.concat([data2_food_name, lsqL_res], axis=1)
  data2_need_nutrients_amount = data2_need_nutrients_amount.rename(columns={0:'必要な量(g)'})
  result = data2_need_nutrients_amount
  
  return_list = []
  for return_data in result.values:
    return_list.append([
      codecs.decode(return_data[0].encode()),
      round(return_data[1])
    ])

  nutrients_result = pd.concat([pd.DataFrame(np.dot(data2matrix,lsq_linear(A,B,bounds=(lb,ub)).x)),pd.DataFrame(B)],axis=1)
  nutrients_result.insert(0,'栄養素',['エネルギー(kcal)','タンパク質(g)','脂質(g)','炭水化物(g)','カリウム(mg)','カルシウム(mg)','マグネシウム(mg)','リン(mg)','鉄(mg)','亜鉛(mg)','銅(mg)','ビタミンA(μg)','ビタミンD(μg)','ビタミンE(mg)','ビタミンK(μg)' ,'ビタミンB1(mg)','ビタミンB2(mg)','ナイアシン(mg)','ビタミンB6(mg)','ビタミンB12(μg)','葉酸(μg)','パントテン酸(mg)','ビタミンC(mg)','食物繊維(g)','食塩相当量(g)'])
  nutrients_result.columns=['栄養素','最適化食材で得られる栄養','1食の栄養摂取基準']
  result2 = nutrients_result
  return2_list = []
  for return2_data in result2.values:
    return2_list.append([
      codecs.decode(return2_data[0].encode()),
      round(return2_data[1],2),
      round(return2_data[2],2)
    ])
  return return_list,return2_list

if __name__ == "__main__":
   app.run()
