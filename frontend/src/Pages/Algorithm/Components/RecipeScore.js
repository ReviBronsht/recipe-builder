import SyncLoader from "react-spinners/SyncLoader";

export default function RecipeScore({score,estimateScore}) {
  return ( //results of classification - estimated if the user's recipe is good or not
    <div style={{"width":200,color:"black", "borderStyle":"double","backgroundColor":"#f2f2f2", "float":"right"}}>     
      {score == 1 || score == 0 ? <div><span style={{fontWeight:"bold"}}>We estimated that your recipe is...: </span> <hr />{score === 1 ? "good!" : "bad :("} <p></p> <button onClick={() => estimateScore()}>Re-estimate score...</button> </div>: <>Estimating score... <hr/> <SyncLoader color="white" size={10} speedMultiplier={0.5} /></>}
    </div>
  )
}
