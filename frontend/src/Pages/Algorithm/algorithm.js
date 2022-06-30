import RecipeType from './Components/RecipeType'
import RecipeMid from './Components/RecipeMid'
import RecipeFinal from './Components/RecipeFinal'
import RecipePage from '../Recipe-page/Recipe-page/Recipe-page'
import { useState , useEffect} from 'react'
import axios from 'axios'

function Algorithm() {
  const [stage, setStage] = useState(1);
  const [recipeName, setRecipeName] = useState("");
  const [recipeType, setRecipeType] = useState("");
  const [servingSize, setServingSize] = useState(0);
  const [recipeIngredients, setRecipeIngredients] = useState([]);
  const [recipeDirections, setRecipeDirections] = useState([]);
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
  }

    //delete direction
    const deleteDirection = (direction) => {
      const newList = recipeDirections.filter((item) => item !== direction);
      setRecipeDirections(newList);
   }

   //get recommendations 
   const getRecs = () => {
    axios.post('/recipe/recipe-builder',{algorithm:"recommendation",name:recipeName,type:recipeType,recipe_ingredients:recipeIngredients,recipe_directions:recipeDirections, serving_size:servingSize[1]})
    .then(response => {
      var result = response.data;
      result = result.replaceAll("'", '"');
      result = JSON.parse(result);
      console.log(result);

      var tempRecipe_is = recipeIngredients;
      
       var temp_as = result.improved_ingredients;
       setARecs(temp_as);
       var curr_is_names = [];
       for (let i = 0; i < tempRecipe_is.length; i++) {
             curr_is_names.push(tempRecipe_is[i][0])
        }
       for (let i = 0; i < temp_as.length; i++) {
         if (curr_is_names.includes(temp_as[i][0])) {
        tempRecipe_is[curr_is_names.indexOf(temp_as[i][0])] = temp_as[i];
        }
     }
      var temp_ds = result.improved_directions;
      setDRecs(temp_ds);
      var tempRecipe_ds = recipeDirections;
      tempRecipe_ds = tempRecipe_ds.concat(temp_ds);
      setRecipeDirections(tempRecipe_ds);
      var temp_is = result.new_ingredients;
      setIRecs(temp_is);
      
      tempRecipe_is = tempRecipe_is.concat(temp_is);
      setRecipeIngredients(tempRecipe_is);
    })
    .catch(error => {
      console.log(error)
    })
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

   // generate finalized ingredients for display 
   const displayIngredients = () => {
    var display_ingredients = [1, 2, 3];

    for(var i = 0; i < recipeIngredients.length; i++) {
      
      display_ingredients[i] = recipeIngredients[i][1] + " " + recipeIngredients[i][2] + " " + recipeIngredients[i][0];
    }
    console.log(recipeIngredients)
    setRecipeIngredients(display_ingredients); 
   }
  return (
    <div className="container">
      <table style={{width:"100%", backgroundColor:"gray"}}>
        <tbody>
          <tr>
            <td>
              Enter recipe name and type 
            </td>
            <td>
              Pick serving size & first few ingredients and directions 
            </td>
            <td>
              Adjust and finalize your recipe
            </td>
          </tr>
          <tr>
            <td style={{textAlign:"center"}}>
            <input type="radio"  value="" checked={stage >= 2 ? "checked" : ""} />
            </td>
            <td style={{textAlign:"center"}}>
            <input type="radio"  value="" checked={stage >= 3 ? "checked" : ""} />
            </td>
            <td style={{textAlign:"center"}}>
            <input type="radio"  value="" checked={stage >= 4 ? "checked" : ""} />
            </td>
          </tr>
        </tbody>
      </table>
      <hr />
      {stage === 1 ? <RecipeType setStage={setStage} setExampleRecipes={setExampleRecipes} changeRecipe={changeRecipe}/> : <button  onClick={() => {window.location.reload(false);}}> Change Recipe </button>}
      <br/>
      {stage === 2 ? <RecipeMid  setStage={setStage} recipeName={recipeName} recipeType={recipeType} servingSize={servingSize} setServingSize={setServingSize} recipeIngredients={recipeIngredients} recipeDirections={recipeDirections} addIngredient={addIngredient} addDirection={addDirection} ingredients={ingredients} directions={directions} changeAmount={changeAmount} measurements={measurements} changeMeasurement={changeMeasurement} deleteIngredient={deleteIngredient} deleteDirection={deleteDirection} ingredientRecs={ingredientRecs} directionRecs={directionRecs} amountRecs={amountRecs} getRecs={getRecs}  exampleRecipes={exampleRecipes}/> : ""}
      {stage === 3 ? <RecipeFinal displayIngredients={displayIngredients} setStage={setStage} recipeName={recipeName} recipeType={recipeType} servingSize={servingSize} recipeIngredients={recipeIngredients} recipeDirections={recipeDirections} addIngredient={addIngredient} addDirection={addDirection} ingredients={ingredients} directions={directions} changeAmount={changeAmount} measurements={measurements} changeMeasurement={changeMeasurement} deleteIngredient={deleteIngredient} deleteDirection={deleteDirection} score={score} estimateScore={estimateScore} ingredientRecs={ingredientRecs} directionRecs={directionRecs} amountRecs={amountRecs} getRecs={getRecs}  /> : ""}
    {stage === 4 ? <RecipePage builtRecipe={{name:recipeName,ingredients:recipeIngredients,directions:recipeDirections}} /> : "Please enter a recipe!"}
    </div>
  );
}

export default Algorithm;
