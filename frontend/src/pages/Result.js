import React, { useEffect, useState } from 'react';

import { Link } from 'react-router-dom';
import { Tweet } from 'react-twitter-widgets';

import { Clipboard, copyToClipboard } from '../utils/Clipboard';
import EmailAlertForm from '../components/EmailAlertForm';
import Header from '../components/Header';
import { HelpType } from '../utils/Constants';


const Result = () => {

    const [tweets, setTweets] = useState({});
    const [activeTab, setActiveTab] = useState(HelpType.helpOffered);
    const [linkCopied, setLinkCopied] = useState(false);

    useEffect(() => {
        // Call API to get tweets
        setTweets({});
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
            { Object.keys(tweets).length === 0 ?
                <main className="mt-16 mx-auto text-center md:w-3/4 lg:w-1/2">
                    <p>Estamos recolectando y clasificando los tweets, esto puede tardar varios minutos.</p>
                    { linkCopied ? <p className="text-green-400 font-semibold">¡Enlace copiado!</p> :
                        <p>
                            <button type="button" className="text-blue-900 font-bold hover:underline" 
                            onClick={copyLink}>Copia el enlace</button> y regresa luego.
                        </p>
                    }
                    <p>También puedes dejarnos tu nombre y tu correo, y te avisaremos cuando todo esté listo.</p>
                    <p>
                        Mientras tanto, puedes revisar 
                        las <Link to="/" className="text-blue-900 font-bold hover:underline">búsquedas</Link> que 
                        otras personas han hecho en el pasado.
                    </p>
                    <EmailAlertForm />
                    <Clipboard copy={document.location.href} />
                </main> :
                <main className="mt-16 mx-auto text-center lg:w-3/4">
                    <ul className="space-x-4">
                        <li className={activeTab === HelpType.helpOffered ? activeTabCSSClasses : inactiveTabCSSClasses}>
                            <button className="focus:outline-none font-semibold"
                            onClick={() => setActiveTab(HelpType.helpOffered)}>
                                Oferta de ayuda
                            </button>
                        </li>
                        <li className={activeTab === HelpType.helpWanted ? activeTabCSSClasses : inactiveTabCSSClasses}>
                            <button className="focus:outline-none font-semibold"
                            onClick={() => setActiveTab(HelpType.helpWanted)}>
                                Pedido de ayuda
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
