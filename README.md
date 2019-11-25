# Newspaper Topic Modelling

* Scraped around 280.000 articles from Spiegel Online distributed in 11 topics

## Research Questions:

Is it possible to recreate and classify topics assigned to news articles by using a topic modelling algorithm on their respective content?

### Subquestions

* Which of the topics has the most topic markers put out by the algorithm?

* Which of the topic markers is classified the most?

* Are articles of a certain topic classified more accurately than others?

### Results
 
* The model was run on a linear SVM, with topics generated through LDA.
* The average accuracy on both the test set and the entire dataset is 79%, with a recall of 78%, with precision ranging from 68% to 93% between the (unevenly distributed) classes.
