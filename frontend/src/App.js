import { BrowserRouter, Route, Switch } from 'react-router-dom';

import './App.css';
import Search from './pages/Search';
import Result from './pages/Result';


const App = () => {
    return (
        <BrowserRouter>
          <Switch>
            <Route path="/search/:id" component={Result} />
            <Route path="/" component={Search} />
          </Switch>
        </BrowserRouter>
  );
};

export default App;
