from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from joblib import Parallel, delayed

def train_model(model, X_train, y_train):
    """
    Helper function to train a single model.
    """
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Helper function to evaluate a single model.
    """
    pred = model.predict(X_test)
    return classification_report(y_test, pred, output_dict=True)

def train_and_evaluate_models_parallel(X, y):
    """
    Train and evaluate models (Random Forest, SVM, and Logistic Regression) in parallel.
    """
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Initialize models
    rf_model = RandomForestClassifier()
    svm_model = SVC()
    lr_model = LogisticRegression(max_iter=200)

    # Train models in parallel
    models = Parallel(n_jobs=-1)(delayed(train_model)(model, X_train, y_train) for model in [rf_model, svm_model, lr_model])

    # Evaluate models in parallel
    evaluation_results = Parallel(n_jobs=-1)(delayed(evaluate_model)(model, X_test, y_test) for model in models)

    # Compile the results
    results = {
        "Random Forest": evaluation_results[0],
        "SVM": evaluation_results[1],
        "Logistic Regression": evaluation_results[2]
    }

    return results
