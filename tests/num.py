import numpy as np 

z = np.linspace(0, 10, 11) 
r = np.linspace(0, 1, 11)

c = np.column_stack((z,r))
print(c)
