import React from 'react';
import TestRenderer from 'react-test-renderer';
import { MockedProvider } from '@apollo/react-testing';
import { MemoryRouter } from 'react-router-dom';

import { render, getByTestId } from '@testing-library/react';

import NotesList from './NotesList';

const mocks = [{ id: 0, title: 'mock note', body: 'Lorem ipsun' }];
describe('Note list', () => {
    it('renders without error', () => {
        TestRenderer.create(
            <MockedProvider mocks={[]} addTypename={false}>
                <MemoryRouter>
                    <NotesList notes={mocks} />
                </MemoryRouter>
            </MockedProvider>
        );
    });

    it('sets the correct title on the note list item', () => {
        const { container } = render(
            <MockedProvider mocks={[]} addTypename={false}>
                <MemoryRouter>
                    <NotesList notes={mocks} />
                </MemoryRouter>
            </MockedProvider>
        );
        const noteItem = getByTestId(container, 'noteItem');

        expect(noteItem.textContent).toBe('mock note');
    });
});
