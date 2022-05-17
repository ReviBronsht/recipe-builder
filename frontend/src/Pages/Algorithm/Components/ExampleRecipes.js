import React from 'react'

export default function ExampleRecipes({exampleRecipes}) {
  return (
    <div style={{"width":200, "borderStyle":"double","backgroundColor":"lightgray", "float":"right"}}>
      Example Recipes
      <hr/>
      <div>
      {exampleRecipes.map((key, i) => (
        <div key={i} >
          <ul style={{"backgroundColor":"lightgray"}}>
            <li>Recipe #{i+1}</li>
            <li>Ingredients: {key[i][0].ingredients.map((ingredient,index)=><ul key={Object.keys(ingredient)}><li>{'\u2022'}{Object.values(ingredient)}% {Object.keys(ingredient)}</li></ul>)}</li>
            <li>Directions: {key[i][1].directions.map((direction,index)=><span key={direction}>{index === key[i][1].directions.length-1 ?direction: direction + ", "}</span>)}</li>
          </ul>
          <hr/>
        </div>
      ))}
      </div>
    </div>
  )
}
