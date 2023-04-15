import * as jwt from "jsonwebtoken";
import { z } from "zod";

const secret = process.env["JWT_SECRET"] ?? "secret";
const algorithm = "HS256";

const PayloadSchema = z.object({
	exp: z.number(),
	sub: z.string()
});

export function generateUserToken(id: string) {
	return jwt.sign({
		exp: Math.floor(Date.now() / 1000) + (60 * 60),
		sub: id
	}, secret, {
		algorithm
	});
}

export function verifyUserToken(token: string) {
	const result = jwt.verify(token, secret, {
		algorithms: [algorithm]
	});

	const payload = PayloadSchema.parse(result);

	return payload.sub;
}
