# Should I stay or should I go? - Predicting KKBox User Churn

Spotify has reigned supreme the music streaming industry for many years now, boasting over 80 million tracks and 456 million active users in 2023. 
Despite its large selection of music, however, it has only a small selection of Chinese songs. As a spotify user based in the US, I was frustrated 
since I couldn't find many of the Chinese songs my parents used to blast in the car.

Luckily, KKBox has filled this void for my family and I. The Taiwan-based company features an impressive 45 million tracks to listen from and is 
extremely popular in countries like Japan, Taiwan, Hong Kong, and Malaysia. My goal of this project is to build a model that can predict KKBox user 
churn based off a user's transaction and listening history. I will also explore the top features associated with churn using a dataset from [Kaggle](https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge/overview). 
The [Jupyter Notebook](https://github.com/Marsha1113302/Data_Science_Projects_Marshall_Lee/blob/main/KKBox_Churn_Prediction/KKBox%20Churn%20Prediction%20Project.ipynb) can also be found in this repo.

## Step 1: Clean and normalize data for analysis


The dataset comprises four tables. The first, train, contains information on whether or not a user churned in April 2017. The second, transactions, shows a user's transaction history and other details. The third, user information, contains a user's listening history and some personal information. The fourth, membership information, shows a user's registration information.

Cleaning this dataset was tricky since some of the transaction data was purposely labeled with an inaccurate date by the poster. Take a look at user '5ty4nZkq54z93wQtBN7RHVYj8rNghBDCVBH+3xmxf0I=' - he clearly renewed his subscription on a weekly basis but the transaction date doesn't reflect this.

![image](https://user-images.githubusercontent.com/115581803/215577054-78e218f3-821b-4af2-aa4e-56b1e1e4fbb0.png)

To solve this problem, I separated the duplicate entries from the non-duplicate entries first. Then, I took the sum of the membership duration and the latest transaction date to avoid removing any relevant data for my analysis.
After further aggregation and cleaning, I merged the remaining tables to our dataframe.

## Step 2: EDA

The dataset is imbalanced in that only 6% of all users appeared to have churned in March 2017. Since I'm looking for any visible correlation between our variables, I start by plotting
bar charts of every feature against user churn. A couple of interesting trends pop up.

*Users with longer memberships seem to churn more often. We see the same with payment amount and payment plan days.*

![image](https://user-images.githubusercontent.com/115581803/215580292-fe4115ea-0322-4025-841e-2f54289b216c.png)

![image](https://user-images.githubusercontent.com/115581803/215590228-9fcd6a73-ec0d-4e62-9deb-5ad7ae0e72a5.png)

![image](https://user-images.githubusercontent.com/115581803/215590550-8bcb5f44-bff7-41b4-aef8-ba7f9595d98b.png)

*There also seems to be a slight increase in churn rate for users that listen to around 40-50 unique songs.*

![image](https://user-images.githubusercontent.com/115581803/215591035-1baf3af2-926b-42cd-9a4c-895dd2bfedf4.png)

## Step 3: Preprocessing/Model building

I will be using F1 and recall scores to judge model performance here. Accuracy would not be appropriate due the how skewed our dataset is. The three models I
will test here are Random Forest, Logistic Regression, and Extreme Gradient Boost. The test scores for each model are:

![image](https://user-images.githubusercontent.com/115581803/215592230-6ee4ba2f-6300-40b8-9ff3-722ce584dd73.png)

XGB wins by a slight margin, but going with Random Forest would be a very viable option as well. We will use Randomized Search cross validation to tune it and prevent overfitting.
