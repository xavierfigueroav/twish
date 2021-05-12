import { Link } from 'react-router-dom';

import logo from '../logo.png';


const Header = () => {
    return (
        <header className="space-y-5 lg:grid lg:grid-cols-3 lg:space-y-0">
            <div className="lg:col-start-2">
                <Link to="/">
                    <img src={logo} className="h-20 m-auto" alt="logo" />
                </Link>
            </div>
            <nav className="lg:col-start-3 lg:self-center">
                <ul className="space-x-8 text-center">
                    <li className="inline">
                        <Link to="/history" className="text-blue-900 font-bold hover:underline">
                            Latest searches
                        </Link>
                    </li>
                    <li className="inline">
                        <Link to="/" className="text-blue-900 font-bold hover:underline">
                            About
                        </Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
