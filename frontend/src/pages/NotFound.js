import { Link } from "react-router-dom";
import Header from "../components/Header";


const NotFound = () => {
    return (
        <div className="m-5">
            <Header />
            <main className="mt-16 mx-auto text-center md:w-3/4 lg:w-1/2">
                <p className="text-2xl font-semibold">¡The page you were looking for does not exist!</p>
                <p className="text-2xl font-semibold">:(</p>
                <br />
                <Link className="text-2xl font-semibold text-blue-900 hover:underline" to="/">
                    Got back to home
                </Link>
            </main>
        </div>
    );
};

export default NotFound;
