import MailchimpSubscribe from "react-mailchimp-subscribe";
import { Link } from "react-router-dom";

const url = "https://gmail.us14.list-manage.com/subscribe/post?u=835e11ee47735b035a9d04ee7&amp;id=f15162d51d";
const SimpleForm = () => <MailchimpSubscribe url={url} />
const newsletter_title = () => <span>Sign up for our newsletter!</span>;
function Menu(props) {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark">
            <Link className="navbar-brand" to="/recipe"><img src="/RecipeBook.png" style={{ width: props.isHeader ? "100px" : "50px" }} alt="Recipe Builder" /></Link>
            <ul className="navbar-nav pl-4">
                <li className="nav-item">
                    <Link className="nav-link" to="/recipe">Home</Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link" to="/recipe/recipe-builder">Recipe Builder</Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link" to="/recipe/all-recipes">All Recipes</Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link" to="/recipe/privacy-policy">Privacy Policy</Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link" to="/recipe/about-us">About us</Link>
                </li>
                {!props.isHeader &&
                    <div>
                        {newsletter_title()}
                        {SimpleForm()}
                    </div>
                }
            </ul>
        </nav>
    );
}

export default Menu;