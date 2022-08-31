import SyncLoader from "react-spinners/SyncLoader";

export default function ExampleRecipes({exampleRecipes, recipeType}) {
  return (
    // Show recipes that considered as good depend on the type choice as a result from clustering
    <div style={{"width":200,color:"black", "borderStyle":"double","backgroundColor":"#f2f2f2", "float":"right"}}>
      💡 Tip!
      <hr/>
      {exampleRecipes.length !== 0 ? <div>
        The best {recipeType} recipes have:
        {exampleRecipes.map((key, i) => (
        <div key={i} >
          <ul style={{"backgroundColor":"#f2f2f2"}}>
            <li>{key[i][0].ingredients.map((ingredient,index)=><ul key={Object.keys(ingredient)}><li>{'\u2022'} {Object.keys(ingredient)}</li></ul>)}</li>
          </ul>
          {i !== exampleRecipes.length -1 ? "or:" : ""}
        </div>
      ))}
      <hr/>
      And are made by:
      {exampleRecipes.map((key, i) => (
        <div key={i} >
          <ul style={{"backgroundColor":"#f2f2f2"}}>
            <li>{key[i][1].directions.map((direction,index)=><span key={direction}>{index === key[i][1].directions.length-1 ?direction: direction + ", "}</span>)}</li>
          </ul>
          {i !== exampleRecipes.length -1 ? "or:" : ""}
        </div>
      ))}
      </div>
      : <SyncLoader color="white" size={10} speedMultiplier={0.5} />}
    </div>
  )
}
