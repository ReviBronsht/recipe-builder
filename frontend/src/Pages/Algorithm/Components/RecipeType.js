import { useState } from 'react'
import axios from 'axios'

    export default function RecipeType ({setStage, changeRecipe, setExampleRecipes}) {
      const [recipeName, setRecipeName] = useState("");
      const [recipeType, setRecipeType] = useState("");

      function submitHandler(e) { //clustering gets example recipes and possible serving sizes
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
    <form onSubmit={submitHandler}> {/** form - user can enter a recipe name and recipe type according to which clustering will run */}
      <h3 style={{marginLeft:"40%"}}>Build Recipe</h3>
      <br/>
      <div className='row'>
        <div className='col-4' style={{marginLeft:"20%"}}>Recipe Name: </div>
        <div className='col-4' style={{position:"absolute", right:"0px",marginRight:"20%"}}><input  type="text" placeholder="Recipe Name" value={recipeName}  onChange={(e) => setRecipeName(e.target.value)} /></div>
      </div>
      <div className='row'>
        <div className='col-4' style={{marginLeft:"20%"}}>Recipe Type: </div>
        <div className='col-4' style={{position:"absolute", right:"0px",marginRight:"20%"}}><input type="text" placeholder="Recipe Type" value={recipeType}  onChange={(e) => setRecipeType(e.target.value)} /> (ex. cake, soup, salad..)</div>
      </div>
      <br/>
      <br/>
        <input style={{width:"60%", marginLeft:"20%"}} type="submit" value="Start building recipe!"/>
    </form>
  )
}
