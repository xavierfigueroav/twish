# Twish
*Twish* is a web application that allows you to host tweets classifiers (Machine Learning-based, rule-based, whatever-based). Once you have set up the app, your users can enter a search term and Twish will collect tweets based on it and classify them using the classifiers you set up.

![alt Twish main workflow animation](flow.gif)

## Features
- Tweets search box (uses Twitter API).
- Classified tweets visualizer.
- Email notifications when classification jobs complete.
- Search history.
- Customizable app name, logo and about page.

## Set up
1. Install [Docker Compose](https://docs.docker.com/compose/install) on your machine.
2. Get the source code on to your machine via git.

`git clone https://github.com/xavierfigueroav/twish && cd twish`

3. Edit the file `dev.env` and set values for the variables `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`.

4. Build and run the Docker containers.

`docker-compose up --build`

5. That's it. Open a web browser and hit the URL http://127.0.0.1:3000.


## Add your own classifiers
To add your own classfiers, you need to follow six steps.

### 1. Install your classifier dependencies.

Your classification logic surely has Python dependencies like numpy, pandas, scikit-learn, etc. To install your dependencies, you need to add them to the `requirements.txt` file. You can do that manually or can install them in the container and freeze them:

`docker exec -it twish_django_1 pip install <lib_1> [<lib_2>...]`

`docker exec -it twish_django_1 pip freeze > requirements.txt`

### 2. Add your serialized model files.

Not much to say about this. Just create a folder for your model files in the directory `backend/classifier/models/` and put your files there. The `example` folder is the home for the model files of the classifier Twish comes with out-of-the-box.

### 3. Add your preprocessing logic.

Very often, tweets need to be preprocessed before passing them into a classifier. If this is your case, you should place your preprocessing logic in `backend/classifier/preprocessors.py`. You are not required to, but you can follow the example preprocessor `LogisticRegressionPreprocessor`.

### 4. Add your prediction logic.

All the logic needed for your model to make predictions must be placed in the module `backend/classifier/predictors.py`. Your prediction logic must be encapsulated in a class that subclasses from `AbstractPredictor` and implements the `predict` method.

The `predict` method should return a collection of triples containing tweet and prediction information in the following order: tweet id, tweet date, tweet predicted label (instance of `PredictionLabel` from `backend/classifier/models.py`).

Although subclassing from `AbstractPredictor` forces you to implement the method `predict`, it does not force you to follow the parameter and return values format of it. However, you are strongly encouraged to follow it to avoid further changes in the codebase.

It is in your predictor class where you should use your preprocessor from step 3.

Take a look at the class `LogisticRegression` for an example on how to implement your own predictor class.

Note: Instances of classes in `predictors.py` are cached if you call `get_predictor` (in `backend/classifier/utils.py`, Twish already does so) instead of instantiating them directly. This is done to mitigate the cost of loading (likely) heavy model files for every prediction request. Yes, you should load your files from step 2 in your predictor class to take advantage of caching.

### 5. Register your classifier.

You need to tell Twish about your predictor for it to take it into account when making predictions.

a. Go to the [Django Admin site](http://localhost:8000/admin/). Log in using:
```
user: admin
password: admin
```
b. Add a new instance of the `Predictor` model. Your predictor's name MUST MATCH your predictor class' name you created in step 4. [Direct link](http://localhost:8000/admin/classifier/predictor/).

c. Modify the existing instance of the `App` model and set your new predictor as default predictor. [Direct link](http://localhost:8000/admin/classifier/app/).

### 6. Restart containers.

Great! You are almost done. Now, you need to restart the containers that host the backend logic.

`docker restart twish_celery_1 twish_django_1`

**Congratulations! You have your own web application to collect, classify and visualize tweets.**

## Deploy

Pending documentation.

## How to contribute

Pending documentation.
