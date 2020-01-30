from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.neural_network import MLPRegressor
import joblib
import time
import pandas as pd
data = pd.read_csv('house_price.csv')
data = data.iloc[:,1:]
label_enc = LabelEncoder()
data.iloc[:,0] = label_enc.fit_transform(data.iloc[:,0])
data.head()
y = data['Price']
X = data.drop('Price', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1
start = time.time()
mlp = MLPRegressor(hidden_layer_sizes=(100,100,100), activation="relu", batch_size=10, learning_rate_init=0.001, max_iter=400, random_state=1)
mlp.fit(X_train, y_train)
end = time.time()
pred = mlp.predict(X_test)
r2_score(y_test, pred)
joblib.dump(mlp,'house_price.sav')
