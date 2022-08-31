import { Link } from "react-router-dom";
import logo from '../../Assets/Images/logo-white.png';

function LandingPage() {
    return (
        <div className="text-center">
            <img src={logo} alt="Recipe Builder" /><br />
            <p>
                Text about our website and database <br />
                Explain that the user can see all the recipes <br />
                or choose to use the algorithm <br />
                Ask the user to choose if he wants to see <br />
                all recipes or use the algorithm <br />
            </p>
            <p>
                <Link to="/all-recipes" className="btn btn-outline-light m-2">All recipes</Link>
                <Link to="/recipe-builder" className="btn btn-outline-light m-2">Use the algorithm</Link>
            </p>
        </div>
    );
}

export default LandingPage;