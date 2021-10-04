import {MongoClient} from 'https://deno.land/x/mongo@v0.27.0/mod.ts';
import type {Bson} from 'https://deno.land/x/mongo@v0.27.0/mod.ts';

const client = new MongoClient();
await client.connect('mongodb://mongo:27017');

const mongo = client.database('giita');

export interface PostSchema {
	_id: Bson.ObjectId,
	id: string,
	body: string,
	title: string,
	theme: string,
	isSample: boolean,
}

export const Posts = mongo.collection<PostSchema>('posts');
