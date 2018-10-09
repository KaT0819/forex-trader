import * as React from 'react';
import { Container, Header, Segment } from 'semantic-ui-react';
import { Trader } from './trader';

export class TraderContainer extends React.Component {
    render(): JSX.Element {
        return (
            <Segment>
                <Header>Traders</Header>
                <Trader />
                <Trader />
                <Trader />
                <Trader />
            </Segment>
        );
    }
}
