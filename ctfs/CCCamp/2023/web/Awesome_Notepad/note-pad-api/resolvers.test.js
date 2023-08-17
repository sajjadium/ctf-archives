const mockConsole = require('jest-mock-console').default;
const resolvers = require('./resolvers');

jest.mock('./db', () => ({
    push: () => '',
    get: () => '',
    delete: () => ''
}));

let restoreConsole;

describe('Resolvers', function() {
    beforeEach(() => {
        restoreConsole = mockConsole();
    });

    afterEach(() => {
        restoreConsole();
    });

    it('Resolvers should be an object', function() {
        expect(resolvers).toBeInstanceOf(Object);
    });

    describe('addNote', function() {
        it('should return a note', function() {
            const result = resolvers.Mutation.addNote('_', {
                title: 'foobar',
                body: 'erp derp'
            });

            expect(result.title).toEqual('foobar');
        });

        it('should create an id', function() {
            const result = resolvers.Mutation.addNote('_', {
                title: 'foobar',
                body: 'erp derp'
            });
            expect(result.id).toBeDefined();
        });

        it('should log when error saving notes', function() {
            const restoreConsole = mockConsole();
            resolvers.Mutation.saveNote();
            expect(console.log).toHaveBeenCalled();
            restoreConsole();
        });
    });
    describe('saveNote', function() {
        it('should return a note', function() {
            const result = resolvers.Mutation.saveNote('_', {
                id: '21893ua8dasj',
                title: 'foobar',
                body: 'erp derp'
            });

            expect(result.title).toEqual('foobar');
        });

        it('should log when error saving notes', function() {
            resolvers.Mutation.saveNote();
            expect(console.log).toHaveBeenCalled();
        });
    });

    describe('deleteNote', function() {
        it('should log when error deleting notes', function() {
            resolvers.Mutation.deleteNote();
            expect(console.log).toHaveBeenCalled();
        });

        it('should log when error deleting notes', function() {
            const result = resolvers.Mutation.deleteNote('_', '1');
            expect(result.status).toEqual('200');
            expect(result.message).toEqual('ok');
        });

        it('should return error when failing a delete', function() {
            const result = resolvers.Mutation.deleteNote();
            expect(result.status).toEqual('500');
            expect(result.message).toEqual('error');
        });
    });
});
