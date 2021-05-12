import axios from 'axios';

import settings from '../admin/settings.json';


const FirstSetUp = () => {

    const djangoAdminURL = `${axios.defaults.baseURL}/admin/`;

    return (
        <main className="flex h-screen mx-10">
            <div className="m-auto md:w-1/2 bg-green-300 px-6 py-5 rounded-md border-2 border-green-500">
                { settings.predictor.labels.length < 2 ?
                    <div>
                        <p className="text-green-900 font-semibold text-center">
                            We have found you application configuration, but you still need to 
                            set at least two <i>PredictorLabels</i> for your default predictor. To do it, go  
                            to <a className="underline" href={djangoAdminURL} target="blank">
                                {djangoAdminURL}
                            </a>.
                        </p>
                    </div> :
                    <div>
                        <p className="text-green-900 font-semibold text-center">
                            You have not configured your application yet. To do it, go  
                            to <a className="underline" href={djangoAdminURL} target="blank">
                                {djangoAdminURL}
                            </a> and create a new instance of <i>App</i>.
                        </p>
                        <br />
                        <p className="text-green-900 font-semibold text-center">
                            Use the following credentials and do not forget to change it later:
                        </p>
                        <p className="text-green-900 font-semibold text-center"><i>user: admin</i></p>
                        <p className="text-green-900 font-semibold text-center"><i>password: admin</i></p>
                    </div>
                }
            </div>
        </main>
    );
};

export default FirstSetUp;
