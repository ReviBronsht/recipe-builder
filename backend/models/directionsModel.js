 let mongoose = require('mongoose');

const direction_schema = new mongoose.Schema({
    keyword:{type:String, required: true},
}, {collection:'directions_keywords'});

const direction_model = mongoose.model('directions_model',direction_schema);

module.exports = direction_model;