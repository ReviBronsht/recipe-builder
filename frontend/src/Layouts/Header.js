import { Link } from "react-router-dom";
import logo from '../Assets/Images/logo-white.png'

//display header logo and menu
function Header() {
    return (
        <div className="text-center">
            <header>
                <div className="row ">
                    <nav className="navbar navbar-expand-lg navbar-dark">
                        <Link className="navbar-brand" to="/home"><img src={logo} style={{ width:  "150px"}} alt="Recipe Builder" /></Link>
                        <ul className="navbar-nav pl-4">
                            <li className="nav-item">
                                <Link className="nav-link" to="/home">Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/about-us">About us</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/recipe-builder">Recipe Builder</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/all-recipes">All Recipes</Link>
                            </li>                            
                        </ul>
                    </nav>
                </div>
            </header >
        </div >
    );
}

export default Header;
