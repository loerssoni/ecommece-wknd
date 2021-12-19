# ecommece-wknd
A practice project for fun on a kaggle dataset.
A lot of use cases, but for now exploring demand forecasting.
The dataset is very clean, so not the most realistic for the usual tasks, but some practice on fast iteration on AWS.
Apparently the data is also biased due to the fact that only orders where a review was left were sampled.

### repo structure
shared contains modularized code constructed that define functions for data ingestion, preprocessing, backtesting etc.

exploratory contains EDA / Experiment type work in notebooks

pipeline contains definition of a model pipeline (Kubeflow?)

#### todo
- serving scripts / conceptual workflow of pulling data and creating batch preditions
- pipeline concept work


#### notes
There's some fun stuff that could be done with this data.

We have reviews, delivery times, delivery distances etc.

These provide opportunity for both feature engineering for different tasks and interesting hypotheses to test.
Examples could be
- customer on churn/CLV (+effects of e.g. delivery times, location remoteness, or review favourability)
- payments (on-time, defaults etc.)