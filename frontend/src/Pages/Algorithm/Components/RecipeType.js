import { useState } from 'react'
import axios from 'axios'

    export default function RecipeType ({setStage, changeRecipe, setExampleRecipes}) {
      const [recipeName, setRecipeName] = useState("");
      const [recipeType, setRecipeType] = useState("");

      function submitHandler(e) {
        e.preventDefault()
        if(recipeName === "" || recipeType === "") {
          alert("Please enter a recipe name and a recipe type")
        }
        else {
          changeRecipe(recipeName,recipeType)
          axios.post('/recipe/recipe-builder',{algorithm:"clustering",name:recipeName,type:recipeType})
          .then(response => {
            var result = response.data;
            result = result.replaceAll("'", '"');
            result = JSON.parse(result);
           setExampleRecipes(result);
          })
          .catch(error => {
            console.log(error)
          })
        }
        setStage(2);
      }
    
  return (
    <form onSubmit={submitHandler}>
      <div>
      <label>Recipe Name: </label>
      <input type="text" placeholder="Recipe Name" value={recipeName}  onChange={(e) => setRecipeName(e.target.value)} /> 
      <br/>
      <label>Recipe Type: </label>
      <input type="text" placeholder="Recipe Type" value={recipeType}  onChange={(e) => setRecipeType(e.target.value)} /> 
      <br/>
      <input type="submit" value="Start building recipe!" />
      </div>
    </form>
  )
}
