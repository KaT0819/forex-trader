import * as React from 'react';
import { Menu, Segment, Sidebar } from 'semantic-ui-react';

export class AccountSidebar extends React.PureComponent {
    render(): JSX.Element {
        return (
            <Sidebar.Pushable as={Segment}>
                <Sidebar
                    as={Menu}
                    animation="scale down"
                    icon="labeled"
                    inverted
                    direction="top"
                    visible={true}
                    width="thin"
                >
                    <Menu.Item as="a">Home</Menu.Item>
                </Sidebar>

                <Sidebar.Pusher>
                    <Segment basic>{this.props.children}</Segment>
                </Sidebar.Pusher>
            </Sidebar.Pushable>
        );
    }
}
