import React from "react";
import { useState } from "react";
import { forwardRef } from "react";
import noImg from '../../../Assets/Images/no-img.jpg';

const Recipe = React.forwardRef(({ recipe, currPath }, ref) => {
    // fetch recipe details and display in the recipe page
    return (        
        <div ref={ref} className="container">
            <h1 className="text-center">{recipe.name} </h1><br/>
            
            <div className='row'>                
                <div className="col-4">
                    <img src={recipe.img !== "NaN" && !currPath.includes("recipe-builder") ? recipe.img : noImg} className="recipe-image"/>                    
                </div><br />
                <div className="col-4" style={{marginLeft:"10%"}}>
                    <h4>Ingredients:</h4>
                    { recipe.ingredients ? 
                    recipe.ingredients.map((ing, index) => (
                        <div key={index} className="caption">
                            {ing}    
                        </div>
                    )) : ""}
                </div>
            </div>
            <p className="text-center">
                <h4>Directions:</h4>
                { recipe.directions ? 
                    
                    recipe.directions.map((dir, index) => (
                        <div key={index} className="caption">
                            {dir}
                        </div>
                    ))                            
                : ""}
            </p>
        </div>
    )
})

export default Recipe;