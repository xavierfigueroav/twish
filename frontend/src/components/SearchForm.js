import axios from 'axios';
import { useState } from 'react';
import { useHistory } from "react-router-dom";

import { API } from '../utils/Constants';
import spinner from '../spinner.svg';


const SearchForm = () => {

    const [searchTerm, setSearchTerm] = useState('');
    const [searchTermValid, setSearchTermValid] = useState(true);

    const [numberOfTweets, setNumberOfTweets] = useState(1000);

    const [seachError, setSearchError] = useState(false);

    const [loading, setLoading] = useState(false);

    const history = useHistory();

    const validateSearchTerm = (value) => {
        const validation = value != undefined && value.trim() !== '';
        setSearchTermValid(validation);
        return validation;
    };

    const handleInputChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        validateSearchTerm(value);
    };

    const handleSelectChange = (event) => {
        const value = event.target.value;
        setNumberOfTweets(value);
    }

    const search = (event) => {
        event.preventDefault();
        if(validateSearchTerm(searchTerm)){
            setSearchError(false);
            setLoading(true);
            const data = {
                search_term: searchTerm,
                number_of_tweets: numberOfTweets
            };
            axios.post(API.search, data).then(response => {
                const path = `search/${response.data.truncated_uuid}`;
                setTimeout(() => {
                    history.push(path);
                    setLoading(false);
                }, 1000);
            }).catch(() => {
                setTimeout(() => {
                    setSearchError(true);
                    setLoading(false);
                }, 1000);
            });
        }
    }

    const validInputCSSClasses = `block bg-gray-100 placeholder-gray-400
    border-2 border-transparent focus:outline-none focus:border-gray-300 rounded-md
    font-semibold text-center h-11 w-11/12 mx-auto py-2 px-3
    sm:inline-block sm:w-1/2 sm:mr-3`;

    const invalidInputCSSClasses = `block bg-white placeholder-red-400
    border-2 border-red-400 focus:outline-none rounded-md
    font-semibold text-red-400 text-center h-11 w-11/12 mx-auto py-2 px-3
    sm:inline-block sm:w-1/2 sm:mr-3`;

    return (
        <form className="space-y-3 mx-auto" onSubmit={search}>
            <input className={searchTermValid ? validInputCSSClasses : invalidInputCSSClasses}
            type="text" placeholder="Enter your search. Ex: oxigen" autoFocus 
            value={searchTerm} onChange={handleInputChange}/>
            <select className="block bg-gray-100 placeholder-gray-400
            border-2 border-transparent focus:outline-none focus:border-gray-300 rounded-md
            font-semibold text-center h-11 mx-auto py-2 px-3 appearance-none sm:inline-block"
            value={numberOfTweets} onChange={handleSelectChange}>
                <option className="bg-white" value="10">10 tweets</option>
                <option className="bg-white" value="50">50 tweets</option>
                <option className="bg-white" value="100">100 tweets</option>
                <option className="bg-white" value="1000">1000 tweets</option>
            </select>
            <button className="block bg-yellow-400 h-11 mx-auto py-2 px-3 rounded-md 
            focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50
            hover:bg-yellow-500 hover:opacity-100 font-semibold text-white"
            type="submit">
                Collect and classify
            </button>
            { loading ? <img className="mx-auto h-10" src={spinner} /> : null }
            { seachError ? 
                <p className="text-red-400 font-semibold">
                    Something went wrong when running your search!<br />
                    Try again, later.
                </p> : null
            }
        </form>
    );
};

export default SearchForm;
