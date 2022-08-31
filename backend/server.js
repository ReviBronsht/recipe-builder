const express = require('express');
const urlencodedParser = express.urlencoded({ extended: false });
const app = express();
const recipeRoutes = require('./routes/recipeRouter');
mongoose = require('mongoose');

//Running in JSON mode
app.use(express.json());

//Enable URLparser(express)
app.use(urlencodedParser);

//DB Connection
mongoose.connect('mongodb://localhost:27017/precent_recipeDB', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(()=>{
  console.log("DB connected");
}).catch(err=>{
  console.log("Database not connected"+err)
});

//Mounting the server (router) on /recipe
app.use('/recipe', recipeRoutes);

//Serves static files, e.g. css files
app.use('/public',express.static('public'));

//Server initialization
const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });