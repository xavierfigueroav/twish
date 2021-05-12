import { useState } from 'react';
import { useParams } from 'react-router-dom';

import axios from 'axios';

import { API } from '../utils/Constants';
import spinner from '../spinner.svg';


const EmailForm = () => {

    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [nameValid, setNameValid] = useState(true);
    const [emailValid, setEmailValid] = useState(true);

    const [emailSaved, setEmailSaved] = useState(false);
    const [emailError, setEmailError] = useState(false);

    const [loading, setLoading] = useState(false);

    const { searchId } = useParams();

    const validateName = (value) => {
        const validation = value != undefined && value.trim() !== '';
        setNameValid(validation);
        return validation;
    };

    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const validateEmail = (value) => {
        const validation = emailRegex.test(value);
        setEmailValid(validation);
        return validation;
    };

    const handleInputChange = (event) => {
        const value = event.target.value;
        if(event.target.name === 'name') {
            setName(value);
            validateName(value);
        } else if(event.target.name === 'email') {
            setEmail(value);
            validateEmail(value);
        }
    };

    const clearForm = () => {
        setName('');
        setEmail('');
    };

    const saveEmail = (event) => {
        event.preventDefault();
        setEmailSaved(false);
        setEmailError(false);
        const nameValidation = validateName(name);
        const emailValidation = validateEmail(email);
        if(nameValidation && emailValidation) {
            setLoading(true);
            const data = { name, email, search: searchId };
            axios.post(API.email, data).then(() => {
                setTimeout(() => {
                    setEmailSaved(true);
                    setEmailError(false);
                    clearForm();
                    setLoading(false);
                }, 1000);
            }).catch(error => {
                setTimeout(() => {
                    console.log(error);
                    setEmailSaved(false);
                    setEmailError(true);
                    setLoading(false);
                }, 1000);
            });
        }
    };

    const validInputCSSClasses = `block bg-gray-100 placeholder-gray-400
    border-2 border-transparent focus:outline-none focus:border-gray-300 rounded-md
    font-semibold text-center h-11 w-4/5 mx-auto py-2 px-3
    sm:inline-block sm:w-1/2 sm:mr-3`;

    const invalidInputCSSClasses = `block bg-white placeholder-red-400
    border-2 border-red-400 focus:outline-none rounded-md
    font-semibold text-red-400 text-center h-11 w-4/5 mx-auto py-2 px-3
    sm:inline-block sm:w-1/2 sm:mr-3`;

    return (
        <form className="space-y-3 mx-auto my-10" onSubmit={saveEmail}>
            <input className={nameValid ? validInputCSSClasses : invalidInputCSSClasses}
            type="text" name="name" placeholder="Your name" value={name} 
            onChange={handleInputChange} />
            { !nameValid ? <p className="text-red-400 font-semibold">
                This field cannot be left blank
            </p>: null }
            <input className={emailValid ? validInputCSSClasses : invalidInputCSSClasses}
            type="email" name="email" placeholder="Your email address" value={email} 
            onChange={handleInputChange} />
            { !emailValid ? <p className="text-red-400 font-semibold">
                Make sure you enter a valid email
            </p>: null }
            <button className="block bg-yellow-400 h-11 mx-auto py-2 px-3 rounded-md 
            focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50
            hover:bg-yellow-500 hover:opacity-100 font-semibold text-white"
            type="submit">
                Send
            </button>
            { loading ? <img className="mx-auto h-10" src={spinner} /> : null }
            { emailSaved ? 
                <p className="text-green-400 font-semibold">
                    We have saved your email!<br />We will notify you when the tweets 
                    collection and classification are ready.
                </p> : 
            emailError ? 
                <p className="text-red-400 font-semibold">
                    Something went wrong when storing your email!<br />
                    Try again, later.
                </p> : null
            }
        </form>
    );

};

export default EmailForm;
