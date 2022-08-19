const express = require('express');
const recipeRoutes = express.Router();
const request = require('request');
const recipeModel = require('../models/recipeModel');
const ingredientsModel = require('../models/ingredientsModel');
const directionsModel = require('../models/directionsModel');


recipeRoutes.get('/c', (req, res) => {
    let data1;
    const { spawn } = require('child_process');

    var filePath = "C:\\Users\\revib\\Downloads\\Backend\\Backend\\routes\\classification.py";
    recipe = {
        "normalized_ingredients": ["flour", "egg", "milk"],
        "normalized_amounts": ["2.5 tsp", "1.0 tbsp", "1.0 tsp", "0.5 tsp"],
        "directions_keywords": ["prepare", "batter"]
    }
    var cmdLineArgs = ["soup", JSON.stringify(recipe)];
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
})

recipeRoutes.get('/b', (req, res) => {
    let data1;
    const { spawn } = require('child_process');

    var filePath = "C:\\Users\\revib\\Downloads\\Backend\\Backend\\routes\\recommendation.py";
    recipe = {
        "normalized_ingredients": ["flour", "egg", "milk"],
        "normalized_amounts": ["2.5 tsp", "1.0 tbsp", "1.0 tsp", "0.5 tsp"],
        "directions_keywords": ["prepare", "batter"]
    }
    var cmdLineArgs = ["soup", "soup1", JSON.stringify(recipe)];
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
})

//Test API
recipeRoutes.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
});

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
recipeRoutes.get('/recipe-builder', function (req, res) {
    console.log("recipe-builder requested (GET)");
    let filter = {};
    let res_ingredients = [];
    let res_directions = [];
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
recipeRoutes.get('/all-recipes', function (req, res) {
    console.log("all-recipe requested (GET)");

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

//enables viewing the full recipe details
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

//Filter request - TBD

//Delete request - TBD

//Update request - TBD

// recipeRoutes.get('/update/:id', function (req, res) {

// });

// recipeRoutes.get('/add', function (req, res) {
//     console.log("Recieved a GET request to fetch the 'Add a student' page.");
//     res.render('add', { degreeArr: degreeArr, selectedDegree: 'ba', baseURL: req.baseUrl });
// });

module.exports = recipeRoutes;