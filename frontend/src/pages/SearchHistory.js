import { useEffect, useState } from 'react';

import axios from 'axios';

import { API } from '../utils/Constants';
import Header from '../components/Header';
import SearchCard from '../components/SearchCard';
import { Link } from 'react-router-dom';

import spinner from '../spinner.svg';


const SearchHistory = () => {

    const [searches, setSearches] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(API.searchHistory).then(response => {
            setTimeout(() => {
                setSearches(response.data);
                setLoading(false);
            }, 500);
        }).catch(console.log);
    }, []);

    return (
        <div className="m-5">
            <Header></Header>
            <main className="mt-16 mx-auto text-center sm:w-3/4">
                { loading ? <img className="mx-auto mt-16 h-10" src={spinner} /> :
                searches.length > 0 ?
                    <div className="mt-16 mx-auto text-center grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                        {searches.map(
                            search => <SearchCard key={search.truncated_uuid} searchTerm={search.search_term} 
                            date={search.date} numberOfTweets={search.number_of_tweets} 
                            href={`/search/${search.truncated_uuid}`}/>
                        )}
                    </div> :
                    <div>
                        <p className="text-2xl font-semibold">
                            There are not any searches with results yet!
                        </p>
                        <p className="text-2xl font-semibold">:(</p>
                        <br />
                        <Link className="text-2xl font-semibold text-blue-900 hover:underline" to="/">
                            Do your own search
                        </Link>
                    </div>
                }
            </main>
        </div>
    );
};

export default SearchHistory;
