import React from 'react'

export default function Recipes({ recipes }) {
    return (
        <div className="container">
            <div className='row'>
                {recipes !== null ? recipes.map((key, i) => (
                    <div className="col-md-4" key={i}>
                        <div className="">
                            <img src={key.image} height="30%" width="30%"/>
                            <div className="caption">
                                <h4>{key.recipe_title}</h4>
                                {key.description}
                            </div>
                        </div>
                    </div>
                )) : ""}
            </div>
        </div>
    )
}
