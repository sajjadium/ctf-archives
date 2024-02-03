import ts, { EmitHint, Node, ScriptTarget } from 'typescript'

import { VirtualProject } from './project'

type Result<T> =
    | { success: true; output: T }
    | { success: false; errors: string[] }

const parse = (text: string): Result<string> => {
    const file = ts.createSourceFile('file.ts', text, ScriptTarget.Latest)
    if (file.statements.length !== 1) {
        return {
            success: false,
            errors: ['expected a single statement'],
        }
    }

    const [statement] = file.statements
    if (!ts.isExpressionStatement(statement)) {
        return {
            success: false,
            errors: ['expected an expression statement'],
        }
    }

    const comments = (ts.getLeadingCommentRanges(text, 0) ?? [])
        .concat(ts.getTrailingCommentRanges(text, 0) ?? [])

    if (
        comments.length > 0
        || [
            '/*',
            '//',
            '#!',
            '<!--',
            '-->',
            'is',
            'as',
            'any',
            'unknown',
            'never',
        ].some((c) => text.includes(c))
    ) {
        return {
            success: false,
            errors: ['illegal syntax'],
        }
    }

    return {
        success: true,
        output: ts
            .createPrinter()
            .printNode(EmitHint.Expression, statement.expression, file),
    }
}

export const sanitize = async (
    type: string,
    input: string,
): Promise<Result<string>> => {
    if (/[^ -~]|;/.test(input)) {
        return {
            success: false,
            errors: ['only one expression is allowed'],
        }
    }

    const expression = parse(input)

    if (!expression.success) return expression

    const data = `((): ${type} => (${expression.output}))()`
    const project = new VirtualProject('file.ts', data)
    const { errors, messages } = await project.lint()

    if (errors > 0) {
        return { success: false, errors: messages }
    }

    return project.compile()
}
