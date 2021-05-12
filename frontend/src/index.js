import React from 'react';
import ReactDOM from 'react-dom';

import axios from 'axios';

import './index.css';
import App from './App';
import settings from './admin/settings.json';
import reportWebVitals from './reportWebVitals';
import FirstSetUp from './pages/FirstSetUp';


axios.defaults.baseURL = process.env.REACT_APP_BACKEND_HOST;


if(settings.name === undefined || settings.predictor.labels.length < 2) {
    ReactDOM.render(
        <React.StrictMode>
          <FirstSetUp />
        </React.StrictMode>,
        document.getElementById('root')
    );
} else {
    ReactDOM.render(
        <React.StrictMode>
          <App />
        </React.StrictMode>,
        document.getElementById('root')
    );
}


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
