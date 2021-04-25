import { BrowserRouter, Route, Switch } from 'react-router-dom';

import './App.css';
import Search from './pages/Search';


const App = () => {
    return (
        <BrowserRouter>
          <Switch>
            <Route path="/" component={Search} />
          </Switch>
        </BrowserRouter>
  );
};

export default App;
