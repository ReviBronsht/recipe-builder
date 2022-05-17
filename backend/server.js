//const mongoose = require('mongoose');
const express = require('express');
const urlencodedParser = express.urlencoded({ extended: false });
const app = express();
const recipeRoutes = require('./routes/recipeRouter');
mongoose = require('mongoose');
//Running in JSON mode
app.use(express.json());

//DB Connection
// mongoose.createConnection('mongodb://localhost:27017/precent_recipeDB', {
//      useNewUrlParser: true,
//      useUnifiedTopology: true
//  });
mongoose.connect('mongodb://localhost:27017/precent_recipeDB', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(()=>{
  console.log("DB connected");
}).catch(err=>{
  console.log("Database not connected"+err)
});
// const directionsModel = require('./models/directionsModel');
// const recipeModel = require('./models/recipeModel');
// const ingredientsModel = require('./models/ingredientsModel');
// const recipe_schema = new mongoose.Schema({
//     name:{type:String},
//   }, {collection:'recipes'});
  
//   const recipeModel = mongoose.model('',recipe_schema);


//  conn1.on('error', function (err) {
//      console.log("Error connecting to recipes:", err);
//  });
//  conn1.on('open', function () {
//      console.log("Connected to 'Recipe' DB.");
//  });


// const studentRoutes = require('./routes/recipeRouter');
// const log_model = require('./models/logModel');
//Logging function
// var my_log = async function(req, res, next) {
//     try {
//         let method = req.method;
//         let path = req.path;
//         let log = new log_model({ "method": method, "path": path, "runmode": runmode });
//         let savedLog = await log.save();
//         console.log("Successfully saved a log with the following info:\n", savedLog);
//         next();
//     }
//     catch (err) {
//         console.log("ERROR SAVING LOG FILE:", err);
//     }
// }
//app.use('/student', [my_log, studentRoutes]);

//Mounting the server (router) on /recipe
// app.get('/a', function(req, res) {
//     let filter = {};
//     ingredientsModel.find(filter,function(err,recipe) {
  
//   if(err){
//     console.log("error finding recipe", err);
//   }
//   else {
//   console.log(recipe);
//   }
//   });
//   }); 
app.use('/recipe', recipeRoutes);

//Serves static files, e.g. css files
app.use('/public',express.static('public'));

//404 Page (if no other routes from recipeRouter served the request)
// app.use([
//     //my_log, 
//     function (req, res, next) { //req, res, next
//         res.status(404).sendFile(__dirname + '/views/PageNotFound.html');
//     }
// ]);

//Server initialization
const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });