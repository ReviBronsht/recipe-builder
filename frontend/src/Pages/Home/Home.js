import img1 from '../../Assets/Images/1.jpg'
import axios from 'axios'
import { useState, useEffect } from 'react';

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
        <div className="">
            <h1 className="text-center">Welcome</h1>
            <p className="pb-5">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>

            <h1 className="text-center">How it works?</h1>
            <p className="pb-5">
                Id volutpat lacus laoreet non curabitur. In massa tempor nec feugiat nisl pretium fusce. Facilisis mauris sit amet massa vitae tortor condimentum lacinia. In fermentum et sollicitudin ac orci phasellus egestas. Facilisi nullam vehicula ipsum a arcu cursus. Lectus magna fringilla urna porttitor rhoncus dolor purus non enim. Nisi porta lorem mollis aliquam ut porttitor leo. Ultrices sagittis orci a scelerisque purus semper eget duis at. Nulla porttitor massa id neque aliquam vestibulum morbi blandit cursus. Vestibulum lectus mauris ultrices eros in. Lacus suspendisse faucibus interdum posuere lorem. Et malesuada fames ac turpis.
            </p>

            <h1 className="text-center">Top 5</h1>
            {recipes !== null ? recipes.map((key, i) => (
                <div key={i} >

                    <table className='mr-5 ml-3'>
                        <tbody>
                        <tr>
                            <td className='caveat-list pr-5'>{i+1}</td>
                            <td><img src={key.image} className="recipe-image d-inline" /></td>
                            <td>
                                <h4>{key.recipe_title}</h4>
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
