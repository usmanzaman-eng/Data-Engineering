import pandas as pd
import numpy as np
df = pd.read_csv("Iris.csv")

#Calculating mean of sepal length of specie Iris-setosa
specie_1=df.query("Species == 'Iris-setosa'")
specie_1["SepalLengthCm"].mean()

#Calculating mean of sepal length of specie Iris-versicolor
specie_2=df.query("Species == 'Iris-versicolor'")
specie_2["SepalLengthCm"].mean()

#Calculating mean of sepal length of specie Iris-virginica
specie_1=df.query("Species == 'Iris-virginica'")
specie_1["SepalLengthCm"].mean()
