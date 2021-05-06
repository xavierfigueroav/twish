import Header from "../components/Header";

const NotFound = () => {
    return (
        <div className="m-5">
            <Header />
            <main className="mt-16 mx-auto text-center md:w-3/4 lg:w-1/2">
                <p className="text-2xl font-semibold">¡La página que estabas buscando no existe!</p>
                <p className="text-2xl font-semibold">:(</p>
                <br />
                <a className="text-2xl font-semibold text-blue-900 hover:underline" href="/">
                    Regresa al inicio
                </a>
            </main>
        </div>
    );
};

export default NotFound;
