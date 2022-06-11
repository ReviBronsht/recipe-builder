import SearchList from './SearchList'
import ExampleRecipes from './ExampleRecipes'
import SyncLoader from "react-spinners/SyncLoader";

export default function RecipeMid({setStage, recipeName, recipeType, servingSize, setServingSize, recipeIngredients, recipeDirections, ingredients, directions, addIngredient, addDirection, changeAmount,measurements,changeMeasurement,deleteIngredient,deleteDirection,getRecs,exampleRecipes}) {
  
    function handleBuild(e) {
        e.preventDefault();

        if(servingSize === 0) {
            alert("Please pick a serving size");
            return;
        }

        if(recipeIngredients.length === 0) {
            alert("Please pick at least one ingredient!");
            return;
        }

        getRecs();
        setStage(3);
    }
  
    return (
    <div>
        <ExampleRecipes exampleRecipes={exampleRecipes} recipeType={recipeType}/>
      <h5>"{recipeName}"</h5>
      {recipeType} Recipe
      <br/>
      <br/>
      <hr />
      Pick a serving size:
      <br/>
      <br />
      {exampleRecipes.length !== 0 ? <>{exampleRecipes.map((recipe, index) => <button key={index} style={{backgroundColor:servingSize[1] === Number(recipe[index][3].total_tbs) ? "gray" : ""}} onClick={() => setServingSize([recipe[index][2].serving_size, Number(recipe[index][3].total_tbs)])}>{recipe[index][2].serving_size}</button>)}</> : <SyncLoader color="white" size={10} speedMultiplier={0.5} />}
      <br/>
      <br/>
      <hr />
      <div style={{"display":"flex", "flexDirection":"row"}}>
      <SearchList data={ingredients} add={addIngredient} title="Add ingredients..." placeholder="type ingredient..."/>
      <SearchList data={directions}  add={addDirection} title="Add directions..." placeholder="type direction..."/>
      </div>
      <table>
        <tbody>
            <tr>
                <td>
                Ingredients:
                </td>
                <td>
                Directions:
                </td>
            </tr>
            <tr>
                <td>
                {recipeIngredients.length > 0 ? <table><tbody>{recipeIngredients.map((ingredient, index) =><tr key={ingredient[0]}><td>{ingredient[0]}</td><td><input type="number" placeholder="type amount..." style={{"width" : "40px"}} value={ingredient[1]} onChange={(e) => changeAmount(e.target.value,index)}></input></td><td><select value={ingredient[2]} onChange={(e) => changeMeasurement(e.target.value,index)}>{measurements.map((measurement) => <option key={measurement} value={measurement}>{measurement}</option>)}</select></td><td><button onClick={() => {deleteIngredient(ingredient);}}>X</button></td></tr>)}</tbody></table>: <p>No ingredients yet!</p>}
                </td>
                <td>
                {recipeDirections.length > 0 ? <table><tbody>{recipeDirections.map((direction) =><tr key={direction}><td>{direction}</td><td><button onClick={() => deleteDirection(direction)}>X</button></td></tr>)}</tbody></table>: <p>No directions yet!</p>}
                </td>
            </tr>
        </tbody>
      </table>
      <hr />
      <button onClick={(e) => handleBuild(e)}>Build my recipe!</button>
    </div>
  )
}
