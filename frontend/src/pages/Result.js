import React, { useEffect, useState } from 'react';

import { Link, useHistory, useParams } from 'react-router-dom';
import { Tweet } from 'react-twitter-widgets';
import axios from 'axios';

import { Clipboard, copyToClipboard } from '../utils/Clipboard';
import EmailForm from '../components/EmailForm';
import Header from '../components/Header';
import { API, HelpType } from '../utils/Constants';

import spinner from '../spinner.svg';


const Result = () => {

    const [tweets, setTweets] = useState({});
    const [searchTerm, setSearchTerm] = useState('');
    const [activeTab, setActiveTab] = useState(HelpType.helpOffered);
    const [isEmptySearch, setIsEmptySearch] = useState(false);
    const [linkCopied, setLinkCopied] = useState(false);
    const [loading, setLoading] = useState(true);

    const { searchId } = useParams();
    const history = useHistory();

    useEffect(() => {
        axios.post(API.result, {search_id: searchId}).then(response => {
            setTimeout(() => {
                setSearchTerm(response.data.search_term);
                if(response.data.processing === undefined) {
                    setTweets(response.data);
                } else if (!response.data.processing) { // Empty search
                    setIsEmptySearch(true);
                }
                setLoading(false);
            }, 500);
        }).catch(() => {
            setTimeout(() => {
                history.push('/404');
                setLoading(false);
            }, 500);
        });
    }, []);

    const copyLink = () => {
        copyToClipboard();
        setLinkCopied(true);
    };

    const activeTabCSSClasses = `inline-block bg-gray-200 px-3 py-2 rounded-md text-gray-500`;
    const inactiveTabCSSClasses = `inline-block hover:bg-gray-100 px-3 py-2 rounded-md text-gray-600`;

    return (
        <div className="m-5">
            <Header />
            { loading ? <img className="mx-auto mt-16 h-10" src={spinner} /> :
            isEmptySearch ?
                <main className="mt-16 mx-auto text-center md:w-3/4 lg:w-1/2">
                    <p className="text-2xl font-semibold">
                        Unfortunately, the search <i>{ searchTerm }</i> has no results!
                    </p>
                    <p className="text-2xl font-semibold">:(</p>
                    <br />
                    <a className="text-2xl font-semibold text-blue-900 hover:underline" href="/">
                        Go back to home
                    </a>
                </main> :
            Object.keys(tweets).length === 0 ?
                <main className="mt-16 mx-auto text-center md:w-3/4 lg:w-1/2">
                    <p>We are collecting and classifying tweets, this may take several minutes.</p>
                    { linkCopied ? <p className="text-green-400 font-semibold">Link copied!</p> :
                        <p>
                            <button type="button" className="text-blue-900 font-bold hover:underline" 
                            onClick={copyLink}>Copy the link</button> and come back later.
                        </p>
                    }
                    <p>Yo can also drop your name and your email, and we will notify you when everything is ready.</p>
                    <p>
                        Meanwhile, you can check 
                        the <Link to="/" className="text-blue-900 font-bold hover:underline">searches</Link> other 
                        people have done previously.
                    </p>
                    <EmailForm />
                    <Clipboard copy={document.location.href} />
                </main> :
                <main className="mt-16 mx-auto text-center lg:w-3/4">
                    <ul className="space-x-4">
                        <li className={activeTab === HelpType.helpOffered ? activeTabCSSClasses : inactiveTabCSSClasses}>
                            <button className="focus:outline-none font-semibold"
                            onClick={() => setActiveTab(HelpType.helpOffered)}>
                                Help offer
                            </button>
                        </li>
                        <li className={activeTab === HelpType.helpWanted ? activeTabCSSClasses : inactiveTabCSSClasses}>
                            <button className="focus:outline-none font-semibold"
                            onClick={() => setActiveTab(HelpType.helpWanted)}>
                                Help wanted
                            </button>
                        </li>
                    </ul>
                    <div className="mt-16 mx-auto text-center grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                        { tweets[activeTab].map(id => <Tweet key={id} tweetId={id} />) }
                    </div>
                </main>
            }
        </div>
    );
};

export default Result;
