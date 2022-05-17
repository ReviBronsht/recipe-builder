import Menu from './Menu';
import { Link } from "react-router-dom";
function Header() {
    return (
        <div className="text-center">
            <header>
                <div className="mx-auto">
                    <nav className="navbar navbar-expand-lg">
                        <ul className="navbar-nav mr-auto">
                            <li className="nav-item">
                                <a  className="fa fa-facebook nav-link" target="_blank" href="https://www.facebook.com/"></a>
                            </li>
                            <li className="nav-item">
                                <a className="fa fa-youtube nav-link" target="_blank" href="https://www.youtube.com/"></a>
                            </li>
                            <li className="nav-item">
                                <a className="fa fa-instagram nav-link" target="_blank" href="https://www.instagram.com/"></a>
                            </li>
                            <li className="nav-item">
                                <a className="fa fa-pinterest nav-link" target="_blank" href="https://www.pinterest.com/"></a>
                            </li>
                            <li className="nav-item">
                                <a className="fa fa-linkedin nav-link" target="_blank" href="https://www.linkedin.com/"></a>
                            </li>
                        </ul>
                    </nav>
                </div>
                <div className="row">
                    <Menu isHeader={true} />
                </div>
            </header >
        </div >
    );
}

export default Header;
