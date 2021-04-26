import React from 'react';


const Clipboard = (props) => {
    return (
        <React.Fragment>
            <textarea id="clipboard" type="text" 
            className="fixed top-0 left-0 h-1 w-1 appearance-none border-0 outline-none focus:outline-none bg-transparent text-transparent" 
            value={props.copy} readOnly></textarea>
            <span className="fixed top-0 left-0 h-2 w-2 bg-white"></span>
        </React.Fragment>
    );
};

const copyToClipboard = () => {
    const clipboard = document.getElementById('clipboard');
    clipboard.focus();
    clipboard.select();
    return document.execCommand('copy');
};

export { Clipboard, copyToClipboard };
