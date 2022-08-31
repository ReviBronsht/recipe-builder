import React from 'react'
import { Link } from "react-router-dom";
import noImg from '../../../Assets/Images/no-img.jpg';

export default function Recipes({ recipes }) {
    return (
        // recipes display of each page
        <div className="container">
            <div className='row'>
                {recipes !== null ? recipes.map((key, i) => (
                    <div className="col-md-4" key={i}>
                        <div className="">
                            <img src={key.image !== "NaN" ? key.image : noImg} className="recipe-image"/>
                            <div className="caption">
                                <h4>{key.recipe_title}</h4>
                                {key.description}
                                <br/>
                                <Link to={"/recipe/" + key._id}><button>Read more</button></Link>
                            </div>
                        </div>
                    </div>
                )) : ""}
            </div>
        </div>
    )
}
