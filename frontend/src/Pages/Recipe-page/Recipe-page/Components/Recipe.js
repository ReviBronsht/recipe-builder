import React from "react";
import img1 from '../../../../Assets/Images/1.jpg'
import img2 from '../../../../Assets/Images/2.jpg'
import img3 from '../../../../Assets/Images/3.jpg'
import img4 from '../../../../Assets/Images/4.jpg'
import img5 from '../../../../Assets/Images/5.jpg'
import { useState } from "react";
import { forwardRef } from "react";

const Recipe = React.forwardRef(({ recipe }, ref) => {
    const [currImage, setCurrImage] = useState(img1);

    var currPath = window.location.href;
    var imgOptions = [img1, img2, img3, img4, img5]

    return (
        <div ref={ref} className="container" >
            <div className='row'>
                <div className="col">
                    <h2>{recipe.name} </h2>
                    <br/>
                    {currPath.includes("recipe-builder") ? 
                    <textarea style={{backgroundColor:"transparent", borderWidth:"0px"}} placeholder="Enter recipe description..." oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"' cols="65">
                    </textarea>
                    :recipe.description}
                    <br/>
                    <br/>
                    {currPath.includes("recipe-builder") ? 
                    <>
                    <img src={currImage} style={{width:"280px"}}/>
                    <br/>
                    {imgOptions.map ((option) => (
                        <button className="printHidden" key={option} onClick={() => setCurrImage(option)}>
                            <img src={option} style={{width:"20px", height:"20px"}}/>
                        </button>
                    ))}
                    </>
                    :
                    <img src={recipe.img} style={{width:"280px"}}/>
                    }
                </div>
                <div className="col">
                    <h4>Ingredients:</h4>
                    { recipe.ingredients ? 
                    recipe.ingredients.map((ing, index) => (
                        <div key={index} className="caption">
                                    {ing}    
                                </div>
                    )) : ""}
                </div>
            </div>
            <div className="row">
                <div className="col">
                    <h4>Directions:</h4>
                    { recipe.directions ? 
                     
                        recipe.directions.map((dir, index) => (
                            <div key={index} className="caption">
                                {dir}
                            </div>
                        ))                            
                    : ""}
                </div>
            </div>
        </div>
    )
})

export default Recipe;