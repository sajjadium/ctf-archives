import React from 'react';
import TestRenderer from 'react-test-renderer';
import { MockedProvider } from '@apollo/react-testing';

import { render, getByTestId } from '@testing-library/react';

import NewTicket from './NewTicket';

describe('NewTicket', () => {
    it('renders without error', () => {
        TestRenderer.create(
            <MockedProvider mocks={[]} addTypename={false}>
                <NewTicket />
            </MockedProvider>
        );
    });

    it('has the save button', () => {
        const component = TestRenderer.create(
            <MockedProvider mocks={[]} addTypename={false}>
                <NewTicket ticket={{ issue: '', id: ''}} />
            </MockedProvider>
        );

        const { container } = render(
            <MockedProvider mocks={[]} addTypename={false}>
                <NewTicket ticket={{ issue: '', id: ''}} />
            </MockedProvider>
        );
        const button = getByTestId(container, 'send');

        expect(button.textContent).toBe('Send');
    });
});
