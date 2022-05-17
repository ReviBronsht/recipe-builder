//const mongoose = require('mongoose');
const express = require('express');
const urlencodedParser = express.urlencoded({ extended: false });
const app = express();
const recipeRoutes = require('../Routes/recipeRouter');

//Running in JSON mode
app.use(express.json());

//DB Connection
// global.conn1 = mongoose.createConnection('mongodb://localhost:27017/academy', {
//     useNewUrlParser: true,
//     useUnifiedTopology: true
// });
// global.conn2 = mongoose.createConnection('mongodb://localhost:27017/academylog', {
//     useNewUrlParser: true,
//     useUnifiedTopology: true
// });

// conn1.on('error', function (err) {
//     console.log("Error connecting to server/db(academy):", err);
// });
// conn1.on('open', function () {
//     console.log("Connected to 'academy' DB.");
// });
// conn2.on('error', function (err) {
//     console.log("Error connecting to server/db(academylog):", err);
// });
// conn2.on('open', function () {
//     console.log("Connected to 'academylog' DB.");
// });

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
app.use('/', recipeRoutes);

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