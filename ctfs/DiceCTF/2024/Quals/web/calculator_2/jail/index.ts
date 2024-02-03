import { ResourceCluster } from './queue'
import { sanitize } from './sanitize'
import ivm from 'isolated-vm'

const queue = new ResourceCluster<ivm.Isolate>(
    Array.from({ length: 16 }, () => new ivm.Isolate({ memoryLimit: 8 }))
)

type RunTypes = {
    'string': string,
    'number': number,
}

type RunResult<T extends keyof RunTypes> = {
    success: true,
    value: RunTypes[T],
} | {
    success: false,
    errors: string[],
}

export const run = async <T extends keyof RunTypes>(
    code: string,
    timeout: number,
    type: T,
): Promise<RunResult<T>> => {
    const result = await sanitize(type, code)
    if (result.success === false) return result
    return await queue.queue<RunResult<T>>(async (isolate) => {
        const context = await isolate.createContext()
        return Promise.race([
            context.eval(result.output).then((output): RunResult<T> => ({
                success: true,
                value: output,
            })),
            new Promise<RunResult<T>>((resolve) => {
                setTimeout(() => {
                    context.release()
                    resolve({
                        success: false,
                        errors: ['evaluation timed out!'],
                    })
                }, timeout)
            })
        ])
    })
}
