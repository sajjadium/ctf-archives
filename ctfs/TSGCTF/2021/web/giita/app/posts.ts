import {Drash} from 'https://deno.land/x/drash@v1.5.1/mod.ts';
import * as qs from 'https://deno.land/std@0.37.0/node/querystring.ts';
import {Posts} from './mongo.ts';

export class PostsResource extends Drash.Http.Resource {
	static paths = ['/:id'];

	public async GET() {
		const id = this.request.getPathParam('id')!.toString();
		const post = await Posts.findOne({id});

		if (!post) {
			return this.response.redirect(301, '/');
		}

		this.response.body = await this.response.render('post', {
			theme: `/public/themes/${post.theme}.css`,
			title: post.title,
			body: post.body,
		});

		return this.response;
	}

	public async POST() {
		const id = this.request.getPathParam('id')!.toString();
		const post = await Posts.findOne({id});

		if (!post) {
			return this.response.redirect(301, '/');
		}

		const res = await fetch('http://reporter:8080/report', {
			method: 'POST',
			headers: {
				'content-type': 'application/x-www-form-urlencoded',
			},
			body: qs.encode({
				url: new URL(`/${id}`, Deno.env.get('BASE_URL')).toString(),
			}),
		});

		this.response.body = await res.text();

		return this.response;
	}
}
