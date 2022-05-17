import SearchList from './SearchList'
import RecipeScore from './RecipeScore'
import Recommendation from './Recommendation'
import ExampleRecipes from './ExampleRecipes'

export default function Recipe({recipeName, recipeType, recipeIngredients, recipeDirections, ingredients, directions, addIngredient, addDirection, changeAmount,measurements,changeMeasurement,deleteIngredient,deleteDirection,score,estimateScore,ingredientRecs,directionRecs,amountRecs,removeIRec,removeDRec,getRecs,changeShowRecs,showRecs,removeARec,exampleRecipes}) {
  return (
    <div>
       <ExampleRecipes exampleRecipes={exampleRecipes}/>
      "{recipeName}"
      <br/>
      <hr/>
      {recipeType} Recipe
      <br/>
      <br/>
      Ingredients:
      {recipeIngredients.length > 0 ? <table><tbody>{recipeIngredients.map((ingredient, index) =><tr key={ingredient[0]}><td>{ingredient[0]}</td><td><input type="number" placeholder="type amount..." style={{"width" : "40px"}} value={ingredient[1]} onChange={(e) => changeAmount(e.target.value,index)}></input></td><td><select value={ingredient[2]} onChange={(e) => changeMeasurement(e.target.value,index)}>{measurements.map((measurement) => <option key={measurement} value={measurement}>{measurement}</option>)}</select></td><td><button onClick={() => {deleteIngredient(ingredient);}}>X</button></td></tr>)}</tbody></table>: <p>No ingredients yet!</p>}
      <br/>
      Directions:
      {recipeDirections.length > 0 ? <table><tbody>{recipeDirections.map((direction) =><tr key={direction}><td>{direction}</td><td><button onClick={() => deleteDirection(direction)}>X</button></td></tr>)}</tbody></table>: <p>No directions yet!</p>}
      <br/>
      <RecipeScore score={score} estimateScore={estimateScore}/>
      <br/>
      <button onClick={() => console.log("Ingredients ",recipeIngredients, "direcions", recipeDirections)}>print recipe</button>
      <hr/>
      <div style={{"display":"flex", "flexDirection":"row"}}>
      <SearchList data={ingredients} add={addIngredient} title="Add ingredients..." placeholder="type ingredient..."/>
      <SearchList data={directions}  add={addDirection} title="Add directions..." placeholder="type direction..."/>
      </div>
      <br/>
      <hr/>
      <Recommendation ingredientRecs={ingredientRecs} directionRecs={directionRecs} amountRecs={amountRecs} addIngredient={addIngredient} addDirection={addDirection} changeAmount={changeAmount} removeIRec={removeIRec} removeDRec={removeDRec} removeARec={removeARec}  getRecs={getRecs} recipeIngredients={recipeIngredients} recipeDirections={recipeDirections} changeShowRecs={changeShowRecs} showRecs={showRecs}/>
      <br/>
    </div>
  )
}
