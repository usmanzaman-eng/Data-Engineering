import fire
import mlflow
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score
    
    
def main(max_k: int):
    X_train, X_test, Y_train, Y_test = get_data()
    k_list = range(1, max_k)
    for k in k_list:
        with mlflow.start_run():
            knn_pipe = setup_knn_pipeline(k)
            knn_pipe.fit(X_train, Y_train)
            Y_pred=knn_pipe.predict(X_test)
            model_metadata = {"k": k}
            track_with_mlflow(knn_pipe, Y_pred, Y_test, mlflow, model_metadata)   


def get_data():
    wine = datasets.load_wine()
    wine_x = wine.data
    wine_y = wine.target

    x_train, x_test, y_train, y_test = train_test_split(
        wine_x, wine_y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    return x_train, x_test, y_train, y_test   
            
                 
def setup_knn_pipeline(k):
    knn = KNeighborsClassifier(n_neighbors=k)
    return knn
            
            
def track_with_mlflow(model, Y_pred, Y_test, mlflow, model_metadata):
    mlflow.log_params(model_metadata)
    mlflow.log_metric("f1_score", f1_score(Y_pred,Y_test,average="micro"))
    mlflow.sklearn.log_model(model, "knn", registered_model_name="new_knn")


if __name__ == "__main__":
    fire.Fire(main)