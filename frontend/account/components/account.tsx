import * as React from 'react';
import { Header, List, Segment } from 'semantic-ui-react';

interface AccountState {
    accountId: string;
}

export class Account extends React.PureComponent {
    state: AccountState;

    constructor(props) {
        super(props);
        this.state = {
            accountId: '1234',
        };
    }

    render(): JSX.Element {
        return (
            <Segment>
                <Header as="h3">Account</Header>
                <List>
                    <List.Item>
                        <List.Icon name="users" />
                        <List.Content>Account ID: {this.state.accountId}</List.Content>
                    </List.Item>
                </List>
            </Segment>
        );
    }
}
