import Header from '../Layouts/Header';
import Footer from '../Layouts/Footer';
import PrivacyPolicy from '../Pages/Privacy-policy/PrivacyPolicy';
import AboutUs from '../Pages/About-us/AboutUs';
import Home from '../Pages/Home/Home'
import Algorithm from '../Pages/Algorithm/algorithm'
import AllRecipes from '../Pages/All-recipes/AllRecipes'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import useFetch from '../useFetch';

function Routes() {
  //const [data, setData] = useState(null);

  const { error, isPending, data} = useFetch("/recipe/api");

  return (
    <Router>
      <div className='px-5'>
      <Header />
      <div className="App">
        <Switch>
          <Route exact path="/recipe">
            <div className="Home">
              { error && <div>{ error }</div> }
              { isPending && <div>Loading...</div> }
              { !error && data }
              <Home />
            </div>
          </Route>
          <Route path="/recipe/recipe-builder">
            <Algorithm />
          </Route>
          <Route path="/recipe/all-recipes">
            <AllRecipes />
          </Route>
          <Route path="/recipe/privacy-policy">
            <PrivacyPolicy />
          </Route>
          <Route path="/recipe/about-us">
            <AboutUs />
          </Route>
        </Switch>
      </div>
      </div>
    </Router>
  );
}

export default Routes;
