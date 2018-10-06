import * as React from 'react';
import { Menu, Segment, Sidebar } from 'semantic-ui-react';

interface MainSidebarProps {
    children: JSX.Element | JSX.Element[];
}

export class MainSidebar extends React.Component<MainSidebarProps> {
    render(): JSX.Element {
        return (
            <Sidebar.Pushable as={Segment} className="sidebar-container">
                <Sidebar as={Menu} animation="push" icon="labeled" inverted vertical visible={true} width="thin">
                    <Menu.Item as="a">Home</Menu.Item>
                </Sidebar>

                <Sidebar.Pusher>
                    <Segment basic>{this.props.children}</Segment>
                </Sidebar.Pusher>
            </Sidebar.Pushable>
        );
    }
}
