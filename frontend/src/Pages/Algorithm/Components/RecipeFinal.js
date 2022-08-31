import SearchList from './SearchList'
import RecipeScore from './RecipeScore'
import SyncLoader from "react-spinners/SyncLoader";

export default function RecipeFinal({displayIngredients, setStage, recipeName, recipeType, servingSize,  recipeIngredients, recipeDirections, ingredients, directions, addIngredient, addDirection, changeAmount,measurements,changeMeasurement,deleteIngredient,deleteDirection,score,estimateScore,ingredientRecs,directionRecs,amountRecs,getRecs}) {
  
  function handleBuild(e) {
    e.preventDefault();

    getRecs();
}

async function finishBuild() {
  const response = await displayIngredients();
  console.log("response recieved");

  const processedResponse = await setStage(4);
  console.log("finished");
}
// displays user's recipe and allows user to adjust - delete ingredients/directions, change amounts, add more ingredients/directions and re-run recommendation algorithm to rebuild recipe

  return (
    <div style={{textAlign:"center", alignItems:"center", margin:"auto"}}>
      {ingredientRecs.length !== 0 ?  <>

        <h5 style={{marginRight:"18%",fontWeight:"bold"}}>"{recipeName}"</h5>
      <span style={{marginRight:"18%"}}>{recipeType} Recipe </span>
      <br/>
        {servingSize[0]} servings
        <RecipeScore score={score} estimateScore={estimateScore}/>
        <br/>
      <br/>
      <span style={{fontWeight:"bold"}}>Ingredients:</span>
      {recipeIngredients.length > 0 ? <table style={{marginLeft:"30%"}}><tbody>{recipeIngredients.map((ingredient, index) =><tr key={ingredient[0]} style={{backgroundColor: ingredientRecs.includes(ingredient) ? "gray" : ""}}><td>{ingredient[0]}</td><td><input type="number" placeholder="type amount..." style={{"width" : "80px",backgroundColor:amountRecs.includes(ingredient) ? "lightgray" : ""}} value={ingredient[1]} onChange={(e) => changeAmount(e.target.value,index)}></input></td><td><select value={ingredient[2]} style={{backgroundColor:amountRecs.includes(ingredient) ? "lightgray" : ""}} onChange={(e) => changeMeasurement(e.target.value,index)}>{measurements.map((measurement) => <option key={measurement} value={measurement}>{measurement}</option>)}</select></td><td><button className='x-btn' onClick={() => {deleteIngredient(ingredient);}}>X</button></td></tr>)}</tbody></table>: <p>No ingredients yet!</p>}
      <br/>
      <span style={{marginRight:"18%", fontWeight:"bold"}}>Directions:</span>
      {recipeDirections.length > 0 ? <p>{recipeDirections.map((direction, index) =><span key={index} style={{backgroundColor: directionRecs.includes(direction) ? "gray" : ""}}> {direction} <button className='x-btn' onClick={() => deleteDirection(direction)}>X</button> {index !== recipeDirections.length - 1 ?",": ""}</span>)}</p>: <p>No directions yet!</p>}
      <br/>
      {console.log(recipeIngredients)}
      {console.log(ingredientRecs)}
      <br/>
      <hr/>
      <h5>Adjust recipe:</h5>
      <div style={{"display":"flex", "flexDirection":"row",  marginLeft:"29%"}}>
      <SearchList data={ingredients} add={addIngredient} title="Add ingredients..." placeholder="type ingredient..."/>
      <SearchList data={directions}  add={addDirection} title="Add directions..." placeholder="type direction..."/>
      </div>

        <hr/>
      <button onClick={(e) => handleBuild(e)}>Re-build my recipe!</button>
      {!score ? estimateScore() : ""}
      <br/>
      <hr/>
      <h5>Finish building recipe...</h5> {/** in the end, can send finished recipe to recipe-page to display it finally */}
      <button  style={{width:"40%"}}onClick={() => {console.log("Ingredients ",recipeIngredients, "direcions", recipeDirections); finishBuild();}}>finish building recipe</button>
      </> :  <SyncLoader color="white" size={10} speedMultiplier={0.5} />}
      
    </div>
  )
}
