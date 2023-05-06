import {Drash} from 'https://deno.land/x/drash@v1.5.1/mod.ts';
import {nanoid} from 'https://deno.land/x/nanoid@v3.0.0/mod.ts';
import {Posts} from './mongo.ts';

export class RootResource extends Drash.Http.Resource {
	static paths = ['/'];

	private validateFilename(input: string) {
		let isInvalid = false;
		for (const char of Array.from(input)) {
			if (!char.match(/[\w\s.]/)) {
				if (isInvalid) {
					return false;
				}
				isInvalid = true;
			}
		}
		return true;
	}

	private getParam(name: string) {
		const value = this.request.getBodyParam(name)!.toString();
		return decodeURIComponent(value.replace(/\+/g, ' '));
	}

	public async GET() {
		this.response.body = await this.response.render('root', {
			title: 'Home',
			samples: await Posts.find({isSample: true}).toArray(),
			themes: [
				'default',
				'base16.default.dark',
				'base16.default.light',
				'base16.solarized.dark',
				'base16.solarized.light',
				'base16.monokai',
			],
		});

		return this.response;
	}

	public async POST() {
		const theme = this.getParam('theme');
		const title = this.getParam('title');
		const body = this.getParam('body');
		const id = nanoid();

		if (!theme || !title || !body || !this.validateFilename(theme)) {
			this.response.status_code = 400;
			this.response.body = 'Bad Request';
			return this.response;
		}

		await Posts.insertOne({theme, title, body, id, isSample: false});

		return this.response.redirect(301, `/${id}`);
	}
}
