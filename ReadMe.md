GitHub link: https://github.com/NavyBirdComics/recipe-builder

########################################################################################################################

Machine Learning Algorithms: The app uses several algorithms. First, the user enters the type of recipe they'd like to make. Then a clustering algorithm runs to find unique recipes from that type (using cluster_centers). The clustering algorithm outputs suggestions for possible recipes and possible serving sizes. The user then picks a serving size and enters the first ingredients/directions. Then the recommendation algorithms run to generate a recipe according to the entered ingredients/directions, recipe type and serving size. Finally, a regression algorithm runs to rate the user's recipe

Clustering: The clustering algorithm runs on the recipes of the same type as the user's recipe that got a good rating (>4.5). It finds possible recipes by creating clusters from found recipes, and uses cluster_centers to find the average recipe from each cluster. It returns those recipes' ingredients and directions to give suggestions to the user, and their serving sizes to allow the user to choose a logical serving size for their recipe.

Cluster analysis, or clustering, is an unsupervised machine learning task. It involves automatically discovering natural grouping in data. The clustering algorithm is Kmeans. k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster.

Recommendation: The app uses two algorithms to recommend recipes, first it uses apriori association-rule to find which ingredients and directions to recommend

association-rule is a rule based machine learning method for discovering interesting relations between variables in large databases. It identifies strong rules in databases. Apriori is an algorithm for frequent item set mining and association rule learning over relational databases. It proceeds by identifying the frequent individual items in the database and extending them to larger and larger item sets as long as those item sets appear sufficiently often in the database.

In our case, (using all recipes of the same type as the user's recipe that got a good rating (>4.5)) it finds which ingredients/directions are likely to be together in a recipe, and so finds which ingredients/directions are likely to be in the same recipe as the user's ingredients/directions, and generates the recipe from them.

After it finds which ingredients and directions to recommend, it finds the amounts of the ingredients through cosine similarity.

Cosine similarity is a measure of similarity between two sequences.

In our case, it creates a cosine similarity matrix between all relevant recipes and sorts them to find the most similar recipes to the generated recipe. It averages the amounts of all ingredients in them, and inserts the right ingredients amounts into the generated recipe.

Finally, it uses the directions_keywords collection to identify which directions are of type 'prepare', which are of type 'cook' and which are of type 'finish', and orders the recommended directions accordingly.

Classifications:

The classification algorithm is used to predict if the user's recipe is good or not. It does so by dividing the recipes into classes ('good' recipes are recipes with rating >= 4.5, 'bad' recipes are recipes with rating < 4.5). It trains on what makes a recipe good, based on ingredients and directions, and predicts whether the user's recipe is good or not.

classification refers to a predictive modeling problem where a class label is predicted for a given example of input data. For classification, we use SGDClassifier (Linear classifiers with SGD training). This estimator implements regularized linear models with stochastic gradient descent (SGD) learning: the gradient of the loss is estimated each sample at a time and the model is updated along the way with a decreasing strength schedule (aka learning rate).

########################################################################################################################

The Server (backend):

Initialization: Using the terminal, make sure to first cd into the backend directory. To start the server, use the following command: npm start. Contingent upon starting up the client (frontend) concurrently, the server will start serving requests from the client. The server is initialized either on the port defined as an environment variable PORT or 3001.

General Information: This server utilizes technology from the MERN stack, i.e. Mongo, Express and Node. React is used as the client (read more at the section "The Client"). The server connects to the DB using the Mongoose library, using localhost on port 27017, under the DB name "precent_recipeDB". Mongoose provides an easy way to include validation with MongoDB. The server is mounted on "/recipe" and serves ONLY JSON (GET and POST) requests.

Router Information: The server utilizes Child Proccesses to launch algorithms, depending upon the specific task to be performed. For more detailed information, please refer to the recipeRouter.js file, under the Routes directory.

Mongoose Models: Three models are utilized in this project: directionsModel, ingredientsModel and recipeModel. They allow for maximum standradization across all recipes displayed on the site.

########################################################################################################################

The Client (frontend): By default, the user would start at the landing page which includes a short description about the website and 2 buttons: to the "all recipes" page and to the "recipe builder" page.

"all recipe" page: fetch all of the db's recipes.
"recipe builder" page: use the algorithm. This page shows the correct form according to the user's stage in the recipe build process and calls for algorithms accordingly.
"home" page: short description about the website and 5 top recipes
"about us" and "privacy policy": text desciption about us and about the website's privacy policy..
The frontend uses Axios to send async HTTP requests to the backend.

########################################################################################################################

The Scrapers:

The Scraper for Obtaining Recipes from the Site atkins.com: Generally speaking, the script systematically goes over each and every one of the pages within a particular category (i.e. diet). To reduce points of failure, the category to be scraped must be enabled manually.

The Scraper for Obtaining Recipes from the Site allrecipes.com: Generally speaking, the script systematically goes over each and every one of the pages within a particular category (i.e. diet). To reduce points of failure, the category to be scraped must be enabled manually.

The Scraper for Obtaining Directions Keywords from the Site supercook.com

The Scraper for Obtaining Cooking Keywords from the Site enchantedlearning.com

All scrapers are written in Python and use Selenium with Chrome driver. The final result is saved locally to a JSON file. ########################################################################################################################

Normalization & DB:

We use MongoDB database because of its flexible schema which makes it easy to evolve the data format and make it easy to program with. In the database, we store the recipes collection, as well as the directions keywords and ingredients (cooking keywords).

During the normalization (three normalization files), the ingredients and directions keywords collections are used to fetch ingredients names and directions from the scraped recipes. Ingredients amounts are fetched using common amount keywords.

Finally, it normalizes the ingredients amounts to the same scale by calculating the precentage of their volume from the total recipe. It does so by first converting every amount to tablespoons (ingredients measured by volume get converted directly, ingredients measured by weight or unit get converted using conversion tables gotten from MapReduce and other websites)
