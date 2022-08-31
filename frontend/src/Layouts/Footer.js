import { Link } from "react-router-dom";
import MailchimpSubscribe from "react-mailchimp-subscribe";

const url = "https://gmail.us14.list-manage.com/subscribe/post?u=835e11ee47735b035a9d04ee7&amp;id=f15162d51d";
//Form for newsletter registration
const SimpleForm = () => <MailchimpSubscribe url={url} />
const newsletter_title = () => <span>Sign up for our newsletter!</span>;

//display footer menu, letter registration and copyrights
function Footer() {
    return (
        <div className="center">
            <footer>
                <div className="row ">
                    <nav className="navbar navbar-expand-lg navbar-dark">
                        <ul className="navbar-nav pl-4">
                            <li className="nav-item">
                                <Link className="nav-link" to="/home">Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/about-us">About us</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/privacy-policy">Privacy Policy</Link>
                            </li>                            
                        </ul>
                    </nav>
                    <div>
                        {newsletter_title()}
                        {SimpleForm()}
                    </div>
                </div>
                <p class="text-center text-muted">&copy; Copyright 2021 - 2022 Recipe Builder</p>
            </footer>
        </div >
    );
}

export default Footer;