import axios from 'axios';


const FirstSetUp = () => {

    const djangoAdminURL = `${axios.defaults.baseURL}/admin/`;

    return (
        <main className="flex h-screen mx-10">
            <div className="m-auto md:w-1/2 bg-green-300 px-6 py-5 rounded-md border-2 border-green-500">
                <p className="text-green-900 font-semibold text-center">
                    No has configurado tu aplicación aún. Para hacerlo, dirígete 
                    a <a className="underline" href={djangoAdminURL} target="blank">
                        {djangoAdminURL}
                    </a> y crea una nueva instancia del modelo <i>App</i>.
                </p>
                <br />
                <p className="text-green-900 font-semibold text-center">
                    Usa las siguientes credenciales y no olvides cambiarlas en el futuro:
                </p>
                <p className="text-green-900 font-semibold text-center"><i>usuario: admin</i></p>
                <p className="text-green-900 font-semibold text-center"><i>contraseña: admin</i></p>
            </div>
        </main>
    );
};

export default FirstSetUp;
