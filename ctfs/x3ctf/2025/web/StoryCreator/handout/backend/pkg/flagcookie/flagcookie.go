package flagcookie

import "context"

type flagcookieCtxKey struct{}

var flagcookieCtxKeyInstance = &flagcookieCtxKey{}

func SetFlagCookie(ctx context.Context, flagCookie string) context.Context {
	return context.WithValue(ctx, flagcookieCtxKeyInstance, flagCookie)
}

func GetFlagCookie(ctx context.Context) string {
	return ctx.Value(flagcookieCtxKeyInstance).(string)
}
