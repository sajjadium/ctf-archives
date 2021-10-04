import {Drash} from 'https://deno.land/x/drash@v1.5.1/mod.ts';
import {Tengine} from 'https://deno.land/x/drash_middleware@v0.7.9/tengine/mod.ts';
import * as Eta from 'https://deno.land/x/eta@v1.12.3/mod.ts';

import {RootResource} from './root.ts';
import {PostsResource} from './posts.ts';

Eta.configure({views: 'views'});
const __dirname = new URL('.', import.meta.url).pathname;

const server = new Drash.Http.Server({
	directory: __dirname,
	static_paths: ['/public'],
	resources: [
		RootResource,
		PostsResource,
	],
	middleware: {
		after_resource: [
			Tengine({
				render(name: unknown, data: any) {
					return Eta.renderFile(name as string, data)!;
				},
			}),
		],
	},
});

server.run({
	hostname: '0.0.0.0',
	port: 56521,
});

console.log(`Server running at ${server.hostname}:${server.port}`);
