
import axios from 'axios';
import { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import noImg from '../../Assets/Images/no-img.jpg';

function Home() {
    const [recipes, setRecipes] = useState(null)

    //var result
    useEffect(() => {
        axios.get('/recipe')
            .then(response => {
                setRecipes(response.data);
            })
            .catch(error => {
                console.log(error)
            });
    }, []);

    return (
        
        <div className="text-center">
            <h1>Welcome!</h1>
            <p>
                Welcome to Recipe Builder <br />
                Build a recipe using our algorithm <br />
                or choose view all recipes<br />
            </p>

            <h1>Top 5</h1>
            { /* Show top 5 DB recipes */}
            {recipes !== null ? recipes.map((key, i) => (
                <div key={i} >

                    <table className='mr-5 ml-3 text-left'>
                        <tbody>
                        <tr>
                            <td className='caveat-list pr-5'>{i+1}</td>
                            <td>
                                <img src={key.image !== "NaN" ? key.image : noImg} className="d-inline" style={{ width: "100px" }} />
                            </td>
                            <td className='align-top'>
                                <Link to={"/recipe/" + key._id} className="btn-link"><h4>{key.recipe_title}</h4></Link>
                                {key.description}                                
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            )) : "null"}
        </div>
    );
}

export default Home;
