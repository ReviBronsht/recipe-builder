let mongoose = require('mongoose');

const ingredient_schema = new mongoose.Schema({
    ingredient_name:{type:String, required: true},
}, {collection:'ingredients'});

const ingredient_model = mongoose.model('ingredients_model',ingredient_schema);
module.exports = ingredient_model;
        
