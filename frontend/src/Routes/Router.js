import Header from '../Layouts/Header';
import Footer from '../Layouts/Footer';
import PrivacyPolicy from '../Pages/Privacy-policy/PrivacyPolicy';
import AboutUs from '../Pages/About-us/AboutUs';
import Home from '../Pages/Home/Home';
import Algorithm from '../Pages/Algorithm/algorithm';
import AllRecipes from '../Pages/All-recipes/AllRecipes';
import LandingPage from '../Pages/Landing/Landing';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import useFetch from '../useFetch';
import RecipePage from '../Pages/Recipe-page/Recipe-page';

function Routes() {
  //const [data, setData] = useState(null);

  const { error, isPending, data} = useFetch("/recipe/api");
  


  return (
      <Router>
      <div className="App">
        <Switch>
          <Route exact path="/">
            <div className="Landing-page">
              <LandingPage />
            </div>
          </Route>
          <div>
            <Header />
            <Route path="/home">
              <div className="Home">
               
                { isPending && <div>Loading...</div> }
                { !error  }
                <Home />
              </div>
            </Route>
            <Route path="/recipe-builder">
              <Algorithm />
            </Route>
            <Route path="/all-recipes">
              <AllRecipes />
            </Route>
            <Route path="/privacy-policy">
              <PrivacyPolicy />
            </Route>
            <Route path="/recipe/:recipe_id">
              <RecipePage />
            </Route>
            <Route path="/about-us">
              <AboutUs />
            </Route>
            <Footer />
          </div>
        </Switch>
      </div>
    </Router>
  );
}

export default Routes;
