import * as React from 'react';
import { TraderContainer } from './trader/components/trader-container';
import { Account } from './account/components/account';

export class Home extends React.Component {
    render(): JSX.Element {
        return (
            <div>
                <Account />
                <TraderContainer />
            </div>
        );
    }
}
