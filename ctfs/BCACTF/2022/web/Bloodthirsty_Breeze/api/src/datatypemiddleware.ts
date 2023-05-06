import { NextFunction, Request, Response } from "express";

export const _null    = Symbol.for("null");
export const _number  = Symbol.for("number");
export const _boolean = Symbol.for("boolean");
export const _string  = Symbol.for("string");

export const types = { _null, _number, _boolean, _string };

export type DataType = { [key: string]: DataType } | [DataType] | symbol;

export const loginType = {
    username: _string,
    password: _string,
};
export type loginType = {
    username: string,
    password: string,
}; 


export const validateType = (body: unknown, targetType: DataType): boolean => {
    switch (typeof body) {
        case "boolean":
            if (targetType === _boolean) return true;
            else break;

        case "number":
            if (targetType === _number) return true;
            else break;

        case "string":
            if (targetType === _string) return true;
            else break;

        case "object":
            if (body === null) {
                if (targetType === _null) return true;
                else break;
            } else if (Array.isArray(body)) {
                if (Array.isArray(targetType)) {
                    if (body.every(item => !validateType(item, targetType[0]))) return true;
                    else return true;
                } else break;
            } else if ((typeof targetType === "object") && targetType !== null) {
                if (
                    !Array.isArray(targetType) &&
                    Object.entries(targetType)
                        .every(
                            ([key, value]) => body.hasOwnProperty(
                                key
                            ) && validateType(
                                (body as Record<typeof key, unknown>)[key],
                                value,
                            )
                        )
                ) return true;
                else break;
            }
            break;

    }
    return false;
};


const dataTypeMiddleware = (dataType: DataType) => (req: Request, res: Response, next: NextFunction) => {
    if (validateType(req.body, dataType)) {
        next();
    } else {
        res.status(400).send("Invalid JSON shape!");
        next(new Error("Invalid response"));
    }
}

export default dataTypeMiddleware;