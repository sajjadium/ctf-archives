import { Link } from "react-router-dom";

function Navbar() {

    return <nav className="navbar navbar-expand navbar-dark bg-dark">
        <div className="container-fluid">
            <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                    <Link to="/" className="nav-link" >Home</Link>
                </li>
                <li className="nav-item">
                    <Link to="/document" className="nav-link" >My docs</Link>
                </li>
                <li className="nav-item">
                    <Link to="/document/last" className="nav-link" >Last</Link>
                </li>
                <li className="nav-item">
                    <Link to="/new" className="nav-link" >New</Link>
                </li>
            </ul>
            <ul className="navbar-nav ml-auto">
                <li className="nav-item">
                    <Link to="/login" className="nav-link" id="login" >Login</Link>
                </li>
                <li className="nav-item">
                    <Link to="/signup" className="nav-link" id="signup">Signup</Link>
                </li>
                <li className="nav-item">
                    <Link to="/logout" className="nav-link" id="logout">Logout</Link>
                </li>
            </ul>
        </div>
    </nav>
}

export { Navbar }