import RecipeType from './Components/RecipeType'
import Recipe from './Components/Recipe'
import { useState , useEffect} from 'react'
import axios from 'axios'

function Algorithm() {
  
  const [recipeName, setRecipeName] = useState("");
  const [recipeType, setRecipeType] = useState("");
  const [recipeIngredients, setRecipeIngredients] = useState([]);
  const [recipeDirections, setRecipeDirections] = useState([]);
  const [changeType, setChangeType] = useState(true);
  const [showRecs, setShowRecs] = useState(false);
  const [ingredients, setIngredients] = useState(null);
  const [directions, setDirections] = useState(null);
  const [measurements, setMeasurements] = useState(["tbsp","tsp","oz","ounce","fl","qt","pt","gal","lb","ml","kg","cup","gram","liter"]);
  const [score, setScore] = useState("");
  const [ingredientRecs, setIRecs] = useState([]);
  const [directionRecs, setDRecs] = useState([]);
  const [amountRecs, setARecs] = useState([]);
  const [exampleRecipes, setExampleRecipes] = useState([]);

  useEffect(() => {
    axios.get('/recipe/recipe-builder')
        .then(response => {
            var i_array = [];
            var d_array = [];

            var ingredients_res = response.data.ingredients;
            ingredients_res.forEach(i => {
              i_array.push(i.ingredient_name);
            });
            var directions_res = response.data.directions;
            directions_res.forEach(d => {
              d_array.push(d.keyword);
            });

            setIngredients(i_array);
            setDirections(d_array);
        })
        .catch(error => {
            console.log(error)
        });
}, []);

  //set recipe type
  const changeRecipe = (name,type) => {
    setRecipeName(name);
    setRecipeType(type);
    setChangeType(!changeType);
  }
  //change show recs
  const changeShowRecs = (value) => {
    setShowRecs(value);
  }
  //add ingredient to recipe
  const addIngredient = (ingredient) => {
    for (var i = 0; i< recipeIngredients.length;i++) {
      if(recipeIngredients[i][0] === ingredient[0]) {
         let newArr = [...recipeIngredients];
          newArr[i] = [newArr[i][0],newArr[i][1] + 1,newArr[i][2]];
         setRecipeIngredients(newArr);
        return
      }
    }
   setRecipeIngredients([...recipeIngredients,ingredient]);
  }

 //add direction to recipe
  const addDirection = (direction) => {
    for (var i = 0; i< recipeDirections.length;i++) {
      if(recipeDirections[i] === direction) {
        return
      }
    }
   setRecipeDirections([...recipeDirections,direction]);
  }

  //change ingredient amount
  const changeAmount = (amount,index) => {
    let newArr = [...recipeIngredients];
    newArr[index] = [newArr[index][0],amount,newArr[index][2]];
    setRecipeIngredients(newArr);
  }

   //change ingredient measurement
   const changeMeasurement = (measurement,index) => {
    let newArr = [...recipeIngredients];
    newArr[index] = [newArr[index][0],newArr[index][1],measurement];
    setRecipeIngredients(newArr);
  }
  
  //delete ingredient
  const deleteIngredient = (ingredient) => {
     const newList = recipeIngredients.filter((item) => item !== ingredient);
     setRecipeIngredients(newList);
     removeARec(ingredient[0])
  }

    //delete direction
    const deleteDirection = (direction) => {
      const newList = recipeDirections.filter((item) => item !== direction);
      setRecipeDirections(newList);
   }

   //get recommendations 
   const getRecs = () => {
    axios.post('/recipe/recipe-builder',{algorithm:"recommendation",name:recipeName,type:recipeType,recipe_ingredients:recipeIngredients,recipe_directions:recipeDirections})
    .then(response => {
      var result = response.data;
      result = result.replaceAll("'", '"');
      result = JSON.parse(result);
      console.log(result);
      setDRecs(result.improved_directions);
      var temp_is = result.new_ingredients;
      temp_is.forEach(i => i.push("tbs"));
      setIRecs(temp_is);
      var temp_as = result.improved_ingredients;
      temp_as.forEach(a => a.push("tbs"));
      setARecs(temp_as);
    })
    .catch(error => {
      console.log(error)
    })
   }

   
   //remove ingredient rec
   const removeIRec = (ingredient) => {
    const newList = ingredientRecs.filter((item) => item !== ingredient);
    setIRecs(newList);
 }

    //remove direction rec
    const removeDRec = (direcion) => {
      const newList = directionRecs.filter((item) => item !== direcion);
      setDRecs(newList);
   }

   //remove amount rec
   const removeARec = (ingredientName) => {
    const newList = amountRecs.filter((item) => item[0] !== ingredientName);
    setARecs(newList);
 }

   //estimate score
   const estimateScore = () => {
    axios.post('/recipe/recipe-builder',{algorithm:"regression",name:recipeName,type:recipeType,recipe_ingredients:recipeIngredients,recipe_directions:recipeDirections})
    .then(response => {
      if(recipeIngredients.length === 0 || recipeDirections.length === 0 ) {
        alert("Please add ingredients and directions!");
      }
      else{let s = Math.floor(Math.random() * 5);
       setScore(response.data);}
     
    })
    .catch(error => {
      console.log(error)
    })
   }

  return (
    <div className="container">
      {changeType ? <RecipeType setExampleRecipes={setExampleRecipes} changeRecipe={changeRecipe}/> : <button  onClick={() => setChangeType(!changeType)}> Change Recipe </button>}
      <br/>
      {!changeType ? <Recipe  recipeName={recipeName} recipeType={recipeType} recipeIngredients={recipeIngredients} recipeDirections={recipeDirections} addIngredient={addIngredient} addDirection={addDirection} ingredients={ingredients} directions={directions} changeAmount={changeAmount} measurements={measurements} changeMeasurement={changeMeasurement} deleteIngredient={deleteIngredient} deleteDirection={deleteDirection} score={score} estimateScore={estimateScore} ingredientRecs={ingredientRecs} directionRecs={directionRecs} amountRecs={amountRecs} removeIRec={removeIRec} removeDRec={removeDRec} removeARec={removeARec} getRecs={getRecs} changeShowRecs={changeShowRecs} showRecs={showRecs} exampleRecipes={exampleRecipes}/> : "Please enter a recipe!"}
    </div>
  );
}

export default Algorithm;
