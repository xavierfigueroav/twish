import { useState } from 'react';


const EmailAlertForm = () => {

    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [nameValid, setNameValid] = useState(true);
    const [emailValid, setEmailValid] = useState(true);

    const [emailSaved, setEmailSaved] = useState(false);
    const [emailError, setEmailError] = useState(false);

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
        const nameValidation = validateName(name);
        const emailValidation = validateEmail(email);
        if(nameValidation && emailValidation) {
            // The following lines are for the success scenario
            setEmailSaved(true);
            setEmailError(false);
            clearForm();
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
            type="text" name="name" placeholder="Tu nombre" value={name} 
            onChange={handleInputChange} />
            { !nameValid ? <p className="text-red-400 font-semibold">
                Este campo no puede quedar vacío
            </p>: null }
            <input className={emailValid ? validInputCSSClasses : invalidInputCSSClasses}
            type="email" name="email" placeholder="Tu correo electrónico" value={email} 
            onChange={handleInputChange} />
            { !emailValid ? <p className="text-red-400 font-semibold">
                Asegúrate ingresar un correo válido
            </p>: null }
            <button className="block bg-yellow-400 h-11 mx-auto py-2 px-3 rounded-md 
            focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50
            hover:bg-yellow-500 hover:opacity-100 font-semibold text-white"
            type="submit">
                Enviar
            </button>
            { emailSaved ? 
                <p className="text-green-400 font-semibold">
                    ¡Guardamos tu correo!<br />Te avisaremos cuando la 
                    recolección y clasificación estén listas.
                </p> : 
            emailError ? 
                <p className="text-red-400 font-semibold">
                    ¡Ocurrió un error al almacenar tu correo!<br />
                    Inténtalo de nuevo, más tarde.
                </p> : null
            }
        </form>
    );

};

export default EmailAlertForm;
