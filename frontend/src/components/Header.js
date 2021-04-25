import { Link } from 'react-router-dom';

import logo from '../logo.png';


const Header = () => {
    return (
        <header className="space-y-5 sm:grid sm:grid-cols-3 sm:space-y-0">
            <div className="sm:col-start-2">
                <Link to="/">
                    <img src={logo} className="h-24 m-auto" alt="logo" />
                </Link>
            </div>
            <nav className="sm:col-start-3 sm:self-center">
                <ul className="space-x-8 text-center">
                    <li className="inline">
                        <Link to="/" className="text-blue-900 font-bold hover:underline">
                            Últimas búsquedas
                        </Link>
                    </li>
                    <li className="inline">
                        <Link to="/" className="text-blue-900 font-bold hover:underline">
                            Acerca de
                        </Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
