import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Route, BrowserRouter } from 'react-router-dom';
import { Home } from './home';
import './main.css';
import { MainSidebar } from './components/main-sidebar';

class App extends React.Component {
    render(): JSX.Element {
        return (
            <BrowserRouter>
                <MainSidebar>
                    <Route exact path="/" component={Home} />
                </MainSidebar>
            </BrowserRouter>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
