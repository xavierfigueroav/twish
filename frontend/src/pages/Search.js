import Header from '../components/Header';

import SearchForm from '../components/SearchForm';


const Search = () => {
    return (
        <div className="m-5">
            <Header></Header>
            <main className="mt-16 mx-auto text-center space-y-3 sm:w-3/4">
                <div className="space-x-3 space-y-3 mx-auto mb-10 md:w-3/4 lg:w-1/2">
                    <p>
                        Escribe un término de búsqueda y recolectaremos tweets asociados 
                        a él para luego mostrártelos clasificados en dos categorías:
                    </p>
                    <span className="inline-block bg-green-400 rounded-md py-1 px-3
                    font-semibold text-white text-sm">
                        Oferta de ayuda
                    </span>
                    <span className="inline-block bg-red-400 rounded-md py-1 px-3
                    font-semibold text-white text-sm">
                        Pedido de ayuda
                    </span>
                </div>
                <SearchForm></SearchForm>
            </main>
        </div>
    );
};

export default Search;
