const express = require('express');
const recipeRoutes = express.Router();
const recipeModel = require('../models/recipeModel');
const ingredientsModel = require('../models/ingredientsModel');
const directionsModel = require('../models/directionsModel');

//Homepage
recipeRoutes.get('/', function (req, res) {
    console.log("Homepage requested (GET)");

    let filter = {};
    recipeModel.find(filter, function (err, recipes) {

        if (err) {
            console.log("error finding recipe", err);
        }
        else {
            res.send(JSON.stringify(recipes));
        }
    }).limit(5);

});

//Get the recipe builder page
recipeRoutes.get('/recipe-builder', function (req, res) {
    console.log("recipe-builder requested (GET)");
    let filter = {};
    let res_ingredients = [];
    let res_directions = [];
    //Get the ingredients and directions from the database
    ingredientsModel.find(filter, function (err, ingredients) {

        if (err) {
            console.log("error finding ingredients", err);
        }
        else {
            res_ingredients = ingredients;
            directionsModel.find(filter, function (err, direcions) {

                if (err) {
                    console.log("error finding directions", err);
                }
                else {
                    res_directions = direcions;
                    res.send({"ingredients":res_ingredients,"directions":res_directions});
                }
            });
        }
    });
});

//Recieves a POST request to the Recipe Builder page:
/*
Parameters:
algorithm: the algorithm to be used for building the recipe
name: the name of the recipe
type: the type of the recipe
recipe_ingredients: the ingredients of the recipe
recipe_directions: the directions of the recipe
serving_size: the serving size of the recipe
The algorithm is then chosen - "clustering" or "recommendation" or "classification"
The server then launches the appropriate algorithm (python script) as a child process.
*/

recipeRoutes.post('/recipe-builder', function (req, res) {
    console.log("recipe-builder requested (POST)");
    console.log(req.body);

    if (req.body.algorithm) var algorithm = req.body.algorithm;
    else var algorithm = "";

    if (req.body.name) var name = req.body.name;
    else var name = "";
    if (req.body.type) var type = req.body.type;
    else var type = "";
    if (req.body.recipe_ingredients) var ingredients = req.body.recipe_ingredients;
    else var ingredients = "";
    if (req.body.recipe_directions) var directions = req.body.recipe_directions;
    else var directions = "";
    if (req.body.serving_size) var size = req.body.serving_size;
    else var size = "";

    if(algorithm == "clustering"){
    let data1;
    const { spawn } = require('child_process');

    var filePath = __dirname + "\\clustering.py";
    var cmdLineArgs = [type];
    var args = cmdLineArgs;
    args.unshift(filePath);
    console.log(args)
    const pyProg = spawn('python3', args);
    pyProg.stdout.on('data', function (data) {
        data1 = data.toString();

    })
    pyProg.on('close', (code) => {
        console.log("code", code);
        console.log(data1);
        res.send(data1);
    })}

    if(algorithm == "recommendation") {
        var ingredients_names = [];
        var ingredients_amounts = [];

        ingredients.forEach(i => {
            ingredients_names.push(i[0]);
            var amount = i[1] + " " + i[2];
            ingredients_amounts.push(amount);
        });

        let data1;
        const { spawn } = require('child_process');
    
        var filePath =  __dirname + "\\recommendation.py";
        recipe = {
            "normalized_ingredients": ingredients_names,
            "normalized_amounts": ingredients_amounts,
            "directions_keywords": directions
        }
        var cmdLineArgs = [type, name, JSON.stringify(recipe), size];
        var args = cmdLineArgs;
        args.unshift(filePath);
        console.log(args)
        const pyProg = spawn('python3', args);
        pyProg.stdout.on('data', function (data) {
            data1 = data.toString();
    
        })
        pyProg.on('close', (code) => {
            console.log("code", code)
            console.log(data1);
            res.send(data1);
        })
    }

    if(algorithm == "classification") {
        var ingredients_names = [];
        var ingredients_amounts = [];

        ingredients.forEach(i => {
            ingredients_names.push(i[0]);
            var amount = i[1] + " " + i[2];
            ingredients_amounts.push(amount);
        });

        let data1;
        const { spawn } = require('child_process');
    
        var filePath =  __dirname + "\\classification.py";
        recipe = {
            "normalized_ingredients": ingredients_names,
            "normalized_amounts": ingredients_amounts,
            "directions_keywords": directions
        }
    var cmdLineArgs = [type, JSON.stringify(recipe)];
    var args = cmdLineArgs;
    args.unshift(filePath);
    console.log(args)
    const pyProg = spawn('python3', args);
    pyProg.stdout.on('data', function (data) {
        data1 = data.toString();

    })
    pyProg.on('close', (code) => {
        console.log("code", code)
        console.log(data1);
        res.send(data1);
    })
    }
});

//Get the all-recipes page
recipeRoutes.get('/all-recipes', function (req, res) {
    console.log("all-recipes requested (GET)");

    let filter = {};
    let maxPage = 0;

    recipeModel.find(filter, function (err, recipes) {

        if (err) {
            console.log("error finding recipe", err);
        }
        else {
            recipeModel.countDocuments({}, function (err, c) {
                maxPage = parseInt(c / 6);
                console.log(maxPage);
                res.send(JSON.stringify({ "recipes": recipes, "max_page": maxPage }));
            });
        }
    }).skip(0).limit(6);
});

//Recieves a POST reqeust to filter the recipes shown on the all-recipes page
recipeRoutes.post('/all-recipes', function (req, res) {
    console.log("all-recipe requested (POST)");
    console.log(req.body);
    let maxPage = 0;

    if (req.body.title) var title = req.body.title;
    else var title = "";
    if (req.body.diets) var diets = req.body.diets;
    else var diets = [];
    if (req.body.page) var page = (req.body.page - 1) * 6;
    else var page = 0;

    let filter = { "$expr": { "$and": [] } };

    if (title.trim() != "") {
        filter['$expr']["$and"].push({ "$regexMatch": { "input": "$recipe_title", "regex": title, "options": "i" } });
    };

    if (diets.length > 0) {
        diets.forEach((diet) => {
            filter['$expr']["$and"].push({ "$in": [diet, "$diets"] });
        })
    };

    recipeModel.find(filter, function (err, recipes) {
        if (err) {
            console.log("error finding recipe", err);
        }
        else {
            recipes.forEach((r, i) => {
                console.log(r.recipe_title);
            });
            recipeModel.countDocuments(filter, function (err, c) {
                maxPage = parseInt(c / 6);
                if (maxPage == 0 || c % 6 != 0) { maxPage++; }
                console.log(maxPage);
                res.send(JSON.stringify({ "recipes": recipes, "max_page": maxPage }));
            });
        }
    }).skip(page).limit(6);
});

//Enables viewing the full recipe details
recipeRoutes.get('/:recipe_id', function (req, res) {
    let recipe_id = req.params.recipe_id;
    if (recipe_id) {
            recipeModel.findById(recipe_id, function (err, recipe){
                if (!err) {
                    res.send(JSON.stringify(recipe));
                }
                else {
                    res.send("Error retrieving the requested recipe");
                }
            });
    }
    else {
        res.send("Invalid recipe ID!");
    }
});

//Gets the Privacy Policy page
recipeRoutes.get('/privacy-policy', function (req, res) {
    console.log("Privacy Policy page requested (GET)");
    if (global.runmode == "HTML") {
        res.render('privacy-policy', { baseURL: req.baseUrl });
    }
    else {
        res.setHeader('Content-Type', 'application/json');
        res.json("JSON sent successfully (Privacy Policy)");
    }
});

//Gets the About us page
recipeRoutes.get('/about-us', function (req, res) {
    console.log("About us page requested (GET)");
    if (global.runmode == "HTML") {
        res.render('about-us', { baseURL: req.baseUrl });
    }
    else {
        res.setHeader('Content-Type', 'application/json');
        res.json("JSON sent successfully (About us)");
    }
});

module.exports = recipeRoutes;