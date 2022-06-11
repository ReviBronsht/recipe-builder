import SyncLoader from "react-spinners/SyncLoader";

export default function RecipeScore({score,estimateScore}) {
  return (
    <div style={{"width":200,color:"black", "borderStyle":"double","backgroundColor":"lightgray", "float":"right"}}>     
      {score ? <div>Your estimated recipe score is: <hr />{score} <p></p> <button onClick={() => estimateScore()}>Re-estimate score...</button> </div>: <>Estimating score... <hr/> <SyncLoader color="white" size={10} speedMultiplier={0.5} /></>}
    </div>
  )
}
