import pandas as pd 
from tqdm import tqdm as tqdm
import os
import numpy as np
country =[]
for i in tqdm(os.listdir('.')):
	if '(' in i:
		country.append(i.split('(')[1])	
print(np.unique(np.array(country)))
