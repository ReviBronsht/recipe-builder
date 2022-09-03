import { Link } from "react-router-dom";
import logo from '../../Assets/Images/logo-white.png';

function LandingPage() {
    return (
        <div className="text-center">
            <img src={logo} alt="Recipe Builder" /><br />
            <p>
               Welcome to Recipe Builder <br />
                Build a recipe using our algorithm <br />
                or choose view all recipes<br />
            </p>
            <p>
                <Link to="/all-recipes" className="btn btn-outline-light m-2">All recipes</Link>
                <Link to="/recipe-builder" className="btn btn-outline-light m-2">Use the algorithm</Link>
            </p>
        </div>
    );
}

export default LandingPage;
