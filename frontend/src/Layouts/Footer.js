import Menu from './Menu';
function Footer() {
    return (
        <div className="center">
            <footer>
                <Menu isHeader={false} />
                <p class="text-center text-muted">&copy; Copyright 2021 - 2022 Recipe Builder</p>
            </footer>
        </div >
    );
}

export default Footer;