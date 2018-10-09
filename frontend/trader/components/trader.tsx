import * as React from 'react';
import { Container, Header, Segment } from 'semantic-ui-react';

export class Trader extends React.Component {
    render(): JSX.Element {
        return (
            <Segment>
                <Header as="h3">Trader</Header>
            </Segment>
        );
    }
}
