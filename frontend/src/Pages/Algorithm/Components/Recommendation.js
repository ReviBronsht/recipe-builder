

export default function Recommendation({ingredientRecs,directionRecs,amountRecs,addIngredient,addDirection,changeAmount,removeIRec,removeDRec,removeARec,getRecs,recipeIngredients, recipeDirections,changeShowRecs,showRecs}) {

  const findIngredient = (ingredient) => {
  var index = 0
  for (var i = 0; i< recipeIngredients.length;i++) {
    if (recipeIngredients[i][0] === ingredient) {
      index = i;
      break;
    }
  }
  return index;
}

  return (
    <div>
      Could be good to add to your recipe...
      <br/>
      <br/>
      <button onClick={() => { findIngredient("potato"); getRecs(); if(recipeIngredients.length > 0 && recipeDirections.length > 0){changeShowRecs(true);} else{alert("Please enter ingredients and directions");}}}>Get new recommendations</button>
      <br/>
      {showRecs?<table><tbody><tr><td><table><tbody><tr><td>Ingredients:</td></tr>{ingredientRecs.length>0?ingredientRecs.map((r)=><tr key={r[0]}style={{"backgroundColor":"lightgray"}}><td>{r[0]}, {r[1]}{r[2]}</td><td><button style={{"display":"inline"}}onClick={()=>{addIngredient(r);removeIRec(r);}}>add</button></td></tr>):<tr style={{"backgroundColor":"lightgray"}}><td>No ingredients recommended</td></tr>}</tbody></table></td><td><table><tbody><tr><td>Directions:</td></tr>{directionRecs.length>0?directionRecs.map((r,i)=><tr key={r+i}style={{"backgroundColor":"lightgray"}}><td>{r}</td><td><button style={{"display":"inline"}}onClick={()=>{addDirection(r);removeDRec(r);}}>add</button></td></tr>):<tr style={{"backgroundColor":"lightgray"}}><td>No directions recommended</td></tr>}</tbody></table></td><td><table><tbody><tr><td>Change ingredient amounts:</td></tr>{amountRecs.length>0?amountRecs.map((r,index)=><tr key={r[0]}style={{"backgroundColor":"lightgray"}}><td>{recipeIngredients[findIngredient(r[0])][1]}{recipeIngredients[findIngredient(r[0])][2]} {recipeIngredients[findIngredient(r[0])][0]} to {r[1]}{r[2]} {r[0]}</td><td><button style={{"display":"inline"}}onClick={()=>{changeAmount(r[1],findIngredient(r[0]));removeARec(r[0])}}>change</button></td></tr>):<tr style={{"backgroundColor":"lightgray"}}><td>No amounts recommended</td></tr>}</tbody></table></td></tr></tbody></table>: ""}
      <br/>
    </div>
  )
}
