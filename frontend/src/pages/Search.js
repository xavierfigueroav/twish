import Header from '../components/Header';

import SearchForm from '../components/SearchForm';
import settings from '../admin/settings.json';


const Search = () => {
    return (
        <div className="m-5">
            <Header></Header>
            <main className="mt-16 mx-auto text-center space-y-3 sm:w-3/4">
                <div className="space-x-3 space-y-3 mx-auto mb-10 md:w-3/4 lg:w-1/2">
                    <p>
                        Enter a search term and we will collect tweets related to it 
                        and classify them into {settings.predictor.labels.length} categories:
                    </p>
                    <span className="inline-block bg-green-400 rounded-md py-1 px-3
                    font-semibold text-white text-sm">
                        Help Offer
                    </span>
                    <span className="inline-block bg-red-400 rounded-md py-1 px-3
                    font-semibold text-white text-sm">
                        Help wanted
                    </span>
                </div>
                <SearchForm></SearchForm>
            </main>
        </div>
    );
};

export default Search;
