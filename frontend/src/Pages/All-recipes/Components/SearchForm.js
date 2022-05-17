import { useState } from 'react';
import Select from 'react-select';
import axios from 'axios'

export default function SearchForm({ setSearch, setRecipes, avaliableDiets, setCurrPage, setMaxPage }) {
    const [searchQuery, setSearchQuery] = useState("");
    var [searchDiets, setSearchDiets] = useState();

    function submitHandler(e) {
        e.preventDefault();
        setSearch(searchQuery, searchDiets)
        console.log(searchQuery, searchDiets);
        axios.post('/recipe/all-recipes',{title:searchQuery,diets:searchDiets})
        .then(response => {
            setRecipes(response.data.recipes);
            setMaxPage(response.data.max_page);
            setCurrPage(1);
        })
        .catch(error => {
          console.log(error)
        })
    }

    var handleChangeDiets = (e) => {
        setSearchDiets(Array.isArray(e) ? e.map(x => x.label) : []);
    }

    return (
        <div>
            <form onSubmit={submitHandler}>
                <div className='container'>
                    <div className='row'>
                        <div className='col'>
                            <label>Recipe name: </label><br />
                            <input className="form-control mr-sm-2" type="text" placeholder="search" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                        </div>
                        <div className='col'>
                            <label>Diet: </label>
                            <Select className='bg-transparent' isMulti options={avaliableDiets} onChange={handleChangeDiets} placeholder="search"></Select>
                        </div>
                        <div className='col'>
                            <input className='btn btn-outline-light mt-4' type="submit" value="Search" />
                        </div>
                    </div>
                </div>
            </form>
            <br />


        </div>
    )
}
