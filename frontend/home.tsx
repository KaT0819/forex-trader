import * as React from 'react';
import { Trader } from './components/trader';

export class Home extends React.Component {
    render(): JSX.Element {
        return (
            <div>
                <Trader />
            </div>
        );
    }
}
