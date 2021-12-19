# ecommece-wknd
A practice project for fun on a kaggle dataset.
A lot of use cases, but for now exploring demand forecasting.
The dataset is very clean, so not the most realistic for the usual tasks, but some practice on fast iteration on AWS.
Apparently the data is also biased due to the fact that only orders where a review was left were sampled.

#### notes
There's some fun stuff that could be done with this data.

We have reviews, delivery times, delivery distances etc.

These provide opportunity for both feature engineering for different tasks and interesting hypotheses to test.
Examples could be
- customer on churn/CLV (+effects of e.g. delivery times, location remoteness, or review favourability)
- payments (on-time, defaults etc.)


#### todo
- experiments to construct pay-day -type variables for demand forecasting
- initial model experiments + pipeline construction for aggregate and product categories
- perhaps experiments with external data, e.g. weather?
