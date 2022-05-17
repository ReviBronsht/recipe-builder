import axios from 'axios'
export default function Pages({currPage,setCurrPage,maxPage,setRecipes,searchQuery,searchDiets}) {

    function clickPrev (e) {
        e.preventDefault();
        console.log("prev;" , currPage -1);
        setCurrPage(currPage -1);
        axios.post('/recipe/all-recipes',{title:searchQuery,diets:searchDiets,page:currPage -1})
        .then(response => {
          setRecipes(response.data.recipes);
        })
        .catch(error => {
          console.log(error)
        })
    }

    function clickNext (e) {
        e.preventDefault();
        console.log("next;" , currPage + 1);
        setCurrPage(currPage +1);
        axios.post('/recipe/all-recipes',{title:searchQuery,diets:searchDiets,page:currPage +1})
        .then(response => {
          setRecipes(response.data.recipes);
        })
        .catch(error => {
          console.log(error)
        })
    }

  return (
    <div>
      {currPage != 1 ? <button style={{fontSize:"20px"}} onClick={clickPrev}>🠸</button> : ""}
      &nbsp;{currPage}&nbsp; / {maxPage}
      {currPage != maxPage ? <button style={{fontSize:"20px"}} onClick={clickNext}>🠺</button> : ""}
    </div>
  )
}
