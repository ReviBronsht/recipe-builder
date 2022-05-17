
import { useState } from 'react'
import SearchIcon from '@mui/icons-material/Search';
import './SearchBar.css';

export default function SearchList({ data, add, title, placeholder }) {
  const [filteredData, setFilteredData] = useState([]);

  const handleFilter = (e) => {
    const searchWord = e.target.value
    if (searchWord === "") {
      setFilteredData([]);
    }
    else {
      const newFilter = data.filter((value) => {
        return value.toLowerCase().includes(searchWord.toLowerCase());
      })
      setFilteredData(newFilter);
    }
  }



  function clickHandler(e) {
    e.preventDefault()
    if (title === "Add ingredients...") { add([e.target.value, 1, "tbs"]); }
    else if (title === "Add directions...") { add(e.target.value); }
  }


  return (
    <div>
      {title}
      <div className='search'>
        <div className="searchInput">

          <SearchIcon />
          <input type="text" placeholder={placeholder} onChange={handleFilter} />

        </div>
        {filteredData.length !== 0 ?
          <div className='dataResult'>
            {filteredData.slice(0, 15).map((ingredient) => <p key={ingredient} className="dataItem">  <button onClick={clickHandler} value={ingredient} > {ingredient}
            </button></p>)}
          </div> : ""}
      </div>
    </div>
  )
}
