import SearchForm from './Components/SearchForm';
import Recipes from './Components/Recipes';
import Pages from './Components/Pages';
import '../../Assets/Styles/style.css';
import axios from 'axios'
import { useState, useEffect } from 'react';

function App() {
  const [recipes, setRecipes] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchDiets, setSearchDiets] = useState([]);
  const [maxPage, setMaxPage] = useState();
  const [currPage, setCurrPage] = useState(1);

  useEffect(() => {
    axios.get('/recipe/all-recipes/')
        .then(response => {
            setRecipes(response.data.recipes);
            setMaxPage(response.data.max_page);
        })
        .catch(error => {
            console.log(error)
        });
}, []);
  var avaliableDiets = [
    {
      value:1,
      label:"gluten free"
    },
    {
      value:2,
      label:"low-calorie"
    },
    {
      value:3,
      label:"low-cholesterol"
    },
    {
      value:4,
      label:"low-sodium"
    },
    {
      value:5,
      label:"whole30"
    },
    {
      value:6,
      label:"diabetic"
    },
    {
      value:7,
      label:"keto"
    },
    {
      value:8,
      label:"low-carb"
    },
    {
      value:9,
      label:"low-fat"
    }
  ]

  // const setRecipes = (recipes) => {
  //   setRecipes(recipes);
  // }

   //set recipe type
   const setSearch = (query,diets) => {
     setSearchQuery(query);
     setSearchDiets(diets);
  }


  return (
    <div style={{position:"relative"}}>
      <h1 className="text-center">All-Recipes</h1>
          <SearchForm setSearch={setSearch} avaliableDiets={avaliableDiets} setRecipes={setRecipes} setMaxPage={setMaxPage} setCurrPage={setCurrPage}/>
          <Recipes recipes={recipes} />
          <Pages currPage={currPage} setCurrPage={setCurrPage} maxPage={maxPage} setRecipes={setRecipes} searchQuery={searchQuery} searchDiets={searchDiets}/>
    </div>
  );
}

export default App;
