import React from 'react'

export default function RecipeScore({score,estimateScore}) {
  return (
    <div>     
      {score ? <div>Your estimated recipe score is: {score} <p></p> <button onClick={() => estimateScore()}>Re-estimate score...</button> </div>: <button onClick={() => estimateScore()}>Estimate score...</button>}
    </div>
  )
}
