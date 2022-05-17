let mongoose = require('mongoose');

const recipe_schema = new mongoose.Schema({
    recipe_title:{type:String, required: true},
    diets:{type:[String], required: true},
    description:{type:String},
    image:{type:String},
    cook_time:{type:String},
    prep_time:{type:String},
    ingredients:{type:[String], required: true},
    directions:{type:[String]},
    rating:{type:Number},
    comments:{type:[String]},
}, {collection:'recipes'});


const recipe_model = mongoose.model('recipe_model',recipe_schema);
module.exports = recipe_model;
        
