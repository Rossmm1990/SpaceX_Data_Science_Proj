import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, recall_score, accuracy_score, precision_score, f1_score
from pathlib import Path

# Class to run the entire Decision Tree Pipeline, from data loading to model evaluation
class CreateDecisionTree():
    def __init__(self, csv):
        self.csv = csv
        self.df = None
        self.X = None
        self.Y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.stratified_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        self.preprocessor = None
        self.param_grid = {
            'classifier__max_depth': [3, 5, 10, None],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__criterion': ['gini', 'entropy']
        }
        self.y_pred = None
        self.model = None
        self.classification_report = None
        self.recall_score = None
        self.accuracy_score = None
        self.percision_score = None
        self.f1_score = None
        self.confusion_matrix = None
    
    def create_df(self):
        
        csv_path = Path.cwd().parent / 'data' / 'clean_data' / self.csv
        self.df = pd.read_csv(csv_path)
    
    # Gets the X and Y variables from the df and splits then into trainngin and test sets    
    def prep_split_df(self):
        self.df[['launch_site', 'version_booster', 'outcome', 'gridfins', 'reused', 'landingpad', 'block']] = self.df[['launch_site', 'version_booster', 'outcome', 'gridfins', 'reused', 'landingpad', 'block']].astype('category')
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        self.X = self.df.drop(['outcome', 'version_booster', 'gridfins'], axis=1)
        self.Y = self.df['outcome']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=42, stratify=self.Y)
    
    # Creates the preprocessing pipeline for numeric and categorical features
    def create_preprocessor(self):
        
        # Pipeline for numeric features (imputes missing values with the mean and then scales them)
        numeric_feature = ['payload_mass', 'reusedcount']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        
        # Pipeline for categorical features (one-hot encodes them)
        categorical_features = ['launch_site','reused', 'block', 'landingpad']
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_feature),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
     
    # Creates the decision tree model pipeline      
    def create_model(self):
        dt_pipe = dt_pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', DecisionTreeClassifier())
        ])
        
        # Performs Grid Search with Cross-validation to find best hyperparameters for the model
        grid_search_dt = GridSearchCV(dt_pipe, self.param_grid, cv=self.stratified_cv, scoring='recall', error_score='raise')
        grid_search_dt.fit(self.X_train, self.y_train)
        
        self.model = grid_search_dt .best_estimator_ # Save the best model found by GridSearchCV

    # Gets the predicted Y value to get model reports
    def get_y_pred(self):
        self.y_pred = self.model.predict(self.X_test)
    
    # Generates and prints evaluation metrics 
    def get_model_report(self):
        print('Test accuracy:', accuracy_score(self.y_test, self.y_pred))
        print('Test recall:', recall_score(self.y_test, self.y_pred))
        print('Test precision:', precision_score(self.y_test, self.y_pred))
        print('Test f1_score:', f1_score(self.y_test, self.y_pred))
        print('confusion matrix:', confusion_matrix(self.y_test, self.y_pred))
    
    # Running the pipeline with a sample CSV file   
    def run_all(self):
        self.create_df()
        self.prep_split_df()
        self.create_preprocessor()
        self.create_model()
        self.get_y_pred()
        self.get_model_report()
            


test = CreateDecisionTree('cleaned_df_data_training_2025_05_07.csv')
test.run_all()