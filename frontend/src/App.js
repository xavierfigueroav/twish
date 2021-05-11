import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';

import { Helmet, HelmetProvider } from 'react-helmet-async';

import './App.css';
import settings from './admin/settings.json';
import Search from './pages/Search';
import Result from './pages/Result';
import NotFound from './pages/NotFound';
import SearchHistory from './pages/SearchHistory';


const App = () => {
    return (
        <HelmetProvider>
            <Helmet>
                <title>{settings.name}</title>
                <meta name="description" content={settings.description}/>
            </Helmet>
            <BrowserRouter>
                <Switch>
                    <Route exact path="/" component={Search} />
                    <Route exact path="/history" component={SearchHistory} />
                    <Route path="/search/:searchId" component={Result} />
                    <Route path="/404" component={NotFound} />
                    <Redirect to="/404" />
                </Switch>
            </BrowserRouter>
        </HelmetProvider>
  );
};

export default App;
