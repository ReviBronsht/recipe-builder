import Recipe from "./Components/Recipe";
import '../../../Assets/Styles/style.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import React, { useRef } from 'react';
import { useReactToPrint } from 'react-to-print';

function RecipePage({builtRecipe}) {
    const [recipe, setRecipe] = useState([])

    // get recipe
    var currPath = window.location.href;
    useEffect(() => {
        if(currPath.includes("recipe-builder")) {
            setRecipe(builtRecipe);
            console.log(builtRecipe);
        }
        else {
        axios.get(currPath)
            .then(response => {
                setRecipe(
                    {
                        name: response.data.recipe_title,
                        description:response.data.description,
                        img: response.data.image,
                        ingredients: response.data.ingredients,
                        directions: response.data.directions
                    }
                )
            })
            .catch(error => {
                console.log(error)
            });
        }
    },[])


    const componentRef = useRef();
  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
  });


    return(
        <>
        {currPath.includes("recipe-builder") ? 
        <button onClick={handlePrint}>Print your recipe!</button>
        : ""}
        <Recipe recipe = {recipe} ref={componentRef}/>
        </>
    )
}
export default RecipePage;
