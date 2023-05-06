import { promisify } from 'util'
import { exec } from 'child_process'

export function base64decode(payload: string): string {
    const buf = new Buffer(payload, 'base64')
    return buf.toString('utf-8')
}

const execAsync = promisify(exec)
let cache = new Map<string, string>()

export async function ipToCountryCode(ip: string): Promise<string> {
    const hit = cache.get(ip)

    if (hit) {
        return hit
    }

    console.log('requesting_whois', ip)

    try {
        const response = await execAsync(`whois ${ip} | grep -i country | head -n1`)

        const country = response.stdout.split(':')[1].trim()
        cache.set(ip, country)

        return country
    } catch (e) {
        return 'de'
    }
}
