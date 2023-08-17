import React from 'react';
import TestRenderer from 'react-test-renderer';
import { MockedProvider } from '@apollo/react-testing';

import { render, getByTestId } from '@testing-library/react';

import NewNote from './NewNote';

describe('NewNote', () => {
    it('renders without error', () => {
        TestRenderer.create(
            <MockedProvider mocks={[]} addTypename={false}>
                <NewNote />
            </MockedProvider>
        );
    });

    it('has the save button', () => {
        const component = TestRenderer.create(
            <MockedProvider mocks={[]} addTypename={false}>
                <NewNote note={{ title: '', id: '', body: '' }} />
            </MockedProvider>
        );

        const { container } = render(
            <MockedProvider mocks={[]} addTypename={false}>
                <NewNote note={{ title: '', id: '', body: '' }} />
            </MockedProvider>
        );
        const button = getByTestId(container, 'save');

        expect(button.textContent).toBe('Save');
    });
});
