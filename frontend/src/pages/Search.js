import Header from '../components/Header';


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
                <form className="space-y-3 mx-auto">
                    <input className="block bg-gray-100 placeholder-gray-400
                    border-2 border-transparent focus:outline-none focus:border-gray-300 rounded-md
                    font-semibold text-center h-11 w-11/12 mx-auto py-2 px-3
                    sm:inline-block sm:w-1/2 sm:mr-3"
                    type="text" placeholder="Escribe tu búsqueda. Ej: oxígeno" autoFocus />
                    <select className="block bg-gray-100 placeholder-gray-400
                    border-2 border-transparent focus:outline-none focus:border-gray-300 rounded-md
                    font-semibold text-center h-11 mx-auto py-2 px-3 appearance-none sm:inline-block">
                        <option className="bg-white" value="10">10 tweets</option>
                        <option className="bg-white" value="50">50 tweets</option>
                        <option className="bg-white" value="100">100 tweets</option>
                        <option className="bg-white" value="1000" selected>1000 tweets</option>
                    </select>
                    <button className="block bg-yellow-400 h-11 mx-auto py-2 px-3 rounded-md 
                    focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50
                    hover:bg-yellow-500 hover:opacity-100 font-semibold text-white"
                    type="submit">
                        Recolectar y clasificar
                    </button>
                </form>
            </main>
        </div>
    );
};

export default Search;
