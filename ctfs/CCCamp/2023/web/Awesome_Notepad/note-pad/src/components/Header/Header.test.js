import React from 'react';
import { shallow } from 'enzyme';
import Header from './Header';
import AppBar from '@material-ui/core/AppBar';
import Link from '@material-ui/core/Link';

describe('Header', () => {
    it('renders', () => {
        shallow(<Header />);
    });

    it('It has only one Appbar', () => {
        const wrapper = shallow(<Header />);

        expect(wrapper.find(AppBar)).toHaveLength(1);
    });

    it('It contain 2 links', () => {
        const wrapper = shallow(<Header />);
        expect(wrapper.find(Link)).toHaveLength(2);
    });
});
