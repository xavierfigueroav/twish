import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';

import './App.css';
import Search from './pages/Search';
import Result from './pages/Result';
import NotFound from './pages/NotFound';


const App = () => {
    return (
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={Search} />
            <Route path="/search/:searchId" component={Result} />
            <Route path="/404" component={NotFound} />
            <Redirect to="/404" />
          </Switch>
        </BrowserRouter>
  );
};

export default App;
