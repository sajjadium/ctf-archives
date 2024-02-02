import { ESLint } from 'eslint'
import fs from 'node:fs'
import path from 'node:path'
import {
    default as ts,
    CompilerHost,
    Program,
    SourceFile,
    ScriptTarget,
} from 'typescript'

type CompileResult =
    | { success: true, output: string }
    | { success: false, errors: string[] }

type LintResult = {
    errors: number
    messages: string[]
}

const cache = new Map<string, SourceFile>()
const getLibs = (name: string) => {
    if (cache.has(name)) return cache.get(name)

    const location = ts.getDefaultLibFilePath({
        target: ScriptTarget.Latest,
    })

    const directory = path.dirname(location)
    const file = path.join(directory, name)
    const data = fs.readFileSync(file).toString()
    const source = ts.createSourceFile(name, data, ScriptTarget.Latest)

    cache.set(name, source)
    return source
}

class SingleFileHost implements CompilerHost {
    file: SourceFile
    output: string = ''
    writeFile: ts.WriteFileCallback

    constructor(file: SourceFile) {
        this.file = file
        this.writeFile = (file: string, text: string) => {
            if (file.endsWith('.js')) {
                this.output = text
            }
        }
    }

    getSourceFile(name: string): SourceFile | undefined {
        if (name === this.file.fileName) return this.file
        if (path.dirname(name) === 'libs') {
            try {
                return getLibs(path.basename(name))
            } catch {}
        }
    }

    getDefaultLibFileName(): string {
        return 'libs/lib.d.ts'
    }

    getCurrentDirectory(): string {
        return ''
    }

    getCanonicalFileName(name: string): string {
        return name
    }

    useCaseSensitiveFileNames(): boolean {
        return true
    }

    getNewLine(): string {
        throw new Error('Method not implemented.')
    }

    fileExists(name: string): boolean {
        return name === this.file.fileName
    }

    readFile(name: string): string | undefined {
        return name === this.file.fileName ? this.file.text : undefined
    }
}

export class VirtualProject {
    filename: string
    content: string

    source: SourceFile
    host: SingleFileHost
    program: Program

    eslint: ESLint

    constructor(filename: string, content: string) {
        this.filename = filename
        this.content = content

        this.source = ts.createSourceFile(
            filename,
            content,
            ScriptTarget.Latest,
        )

        this.host = new SingleFileHost(this.source)

        this.program = ts.createProgram({
            rootNames: [filename],
            options: {
                strict: true,
                noImplicitAny: true,
                strictNullChecks: true,
                strictFunctionTypes: true,
                strictBindCallApply: true,
                strictPropertyInitialization: true,
                noImplicitThis: true,
                useUnknownInCatchVariables: true,
                alwaysStrict: true,
                exactOptionalPropertyTypes: true,
                noImplicitReturns: true,
                noFallthroughCasesInSwitch: true,
                noUncheckedIndexedAccess: true,
                noImplicitOverride: true,
                noPropertyAccessFromIndexSignature: true,

                noEmitOnError: true,
                target: ScriptTarget.Latest,
            },
            host: this.host,
        })

        const cached = this.program.getSourceFile
        this.program.getSourceFile = (name) => {
            const file = path.basename(name)
            if (file === filename) name = file
            return cached.call(this.program, name)
        }

        this.eslint = new ESLint({
            useEslintrc: false,
            overrideConfig: {
                parser: '@typescript-eslint/parser',
                parserOptions: {
                    programs: [this.program],
                },
                plugins: ['@typescript-eslint'],
                rules: {
                    '@typescript-eslint/await-thenable': 'error',
                    '@typescript-eslint/ban-ts-comment': 'error',
                    '@typescript-eslint/ban-tslint-comment': 'error',
                    '@typescript-eslint/ban-types': 'error',
                    'no-array-constructor': 'error',
                    '@typescript-eslint/no-array-constructor': 'error',
                    '@typescript-eslint/no-array-delete': 'error',
                    '@typescript-eslint/no-base-to-string': 'error',
                    '@typescript-eslint/no-confusing-void-expression': 'error',
                    '@typescript-eslint/no-duplicate-enum-values': 'error',
                    '@typescript-eslint/no-duplicate-type-constituents':
                        'error',
                    '@typescript-eslint/no-dynamic-delete': 'error',
                    '@typescript-eslint/no-explicit-any': 'error',
                    '@typescript-eslint/no-extra-non-null-assertion': 'error',
                    '@typescript-eslint/no-extraneous-class': 'error',
                    '@typescript-eslint/no-floating-promises': 'error',
                    '@typescript-eslint/no-for-in-array': 'error',
                    'no-implied-eval': 'error',
                    '@typescript-eslint/no-implied-eval': 'error',
                    '@typescript-eslint/no-invalid-void-type': 'error',
                    'no-loss-of-precision': 'off',
                    '@typescript-eslint/no-loss-of-precision': 'error',
                    '@typescript-eslint/no-meaningless-void-operator': 'error',
                    '@typescript-eslint/no-misused-new': 'error',
                    '@typescript-eslint/no-misused-promises': 'error',
                    '@typescript-eslint/no-mixed-enums': 'error',
                    '@typescript-eslint/no-namespace': 'error',
                    '@typescript-eslint/no-non-null-asserted-nullish-coalescing':
                        'error',
                    '@typescript-eslint/no-non-null-asserted-optional-chain':
                        'error',
                    '@typescript-eslint/no-non-null-assertion': 'error',
                    '@typescript-eslint/no-redundant-type-constituents':
                        'error',
                    '@typescript-eslint/no-this-alias': 'error',
                    'no-throw-literal': 'error',
                    '@typescript-eslint/no-throw-literal': 'error',
                    '@typescript-eslint/no-unnecessary-boolean-literal-compare':
                        'error',
                    '@typescript-eslint/no-unnecessary-condition': 'error',
                    '@typescript-eslint/no-unnecessary-type-arguments': 'error',
                    '@typescript-eslint/no-unnecessary-type-assertion': 'error',
                    '@typescript-eslint/no-unnecessary-type-constraint':
                        'error',
                    '@typescript-eslint/no-unsafe-argument': 'error',
                    '@typescript-eslint/no-unsafe-assignment': 'error',
                    '@typescript-eslint/no-unsafe-call': 'error',
                    '@typescript-eslint/no-unsafe-declaration-merging': 'error',
                    '@typescript-eslint/no-unsafe-enum-comparison': 'error',
                    '@typescript-eslint/no-unsafe-member-access': 'error',
                    '@typescript-eslint/no-unsafe-return': 'error',
                    'no-unused-vars': 'error',
                    '@typescript-eslint/no-unused-vars': 'error',
                    'no-useless-constructor': 'error',
                    '@typescript-eslint/no-useless-constructor': 'error',
                    '@typescript-eslint/no-useless-template-literals': 'error',
                    '@typescript-eslint/no-var-requires': 'error',
                    '@typescript-eslint/prefer-as-const': 'error',
                    '@typescript-eslint/prefer-includes': 'error',
                    '@typescript-eslint/prefer-literal-enum-member': 'error',
                    'prefer-promise-reject-errors': 'error',
                    '@typescript-eslint/prefer-promise-reject-errors': 'error',
                    '@typescript-eslint/prefer-reduce-type-parameter': 'error',
                    '@typescript-eslint/prefer-return-this-type': 'error',
                    '@typescript-eslint/prefer-ts-expect-error': 'error',
                    'require-await': 'error',
                    '@typescript-eslint/require-await': 'error',
                    '@typescript-eslint/restrict-plus-operands': 'error',
                    '@typescript-eslint/restrict-template-expressions': 'error',
                    '@typescript-eslint/triple-slash-reference': 'error',
                    '@typescript-eslint/unbound-method': 'error',
                    '@typescript-eslint/unified-signatures': 'error',
                    '@typescript-eslint/consistent-type-assertions': [
                        'error',
                        { assertionStyle: 'never' },
                    ],
                },
            },
        })
    }

    compile(): CompileResult {
        const { emitSkipped, diagnostics } = this.program.emit()
        if (emitSkipped || diagnostics.length > 0) {
            return {
                success: false,
                errors: diagnostics.map((d) => d.messageText.toString()),
            }
        }
        return {
            success: true,
            output: this.host.output,
        }
    }

    async lint(): Promise<LintResult> {
        const results = await this.eslint.lintText(this.content, {
            filePath: this.filename,
        })
        const messages = results
            .flatMap((r) => r.messages)
            .map((m) => m.message)

        const errors = results.reduce((acc, r) => acc + r.errorCount, 0)
        return {
            errors,
            messages,
        }
    }
}
