package tenant

import "context"

type tenantCtxKey struct{}

var tenantCtxKeyInstance = &tenantCtxKey{}

func SetTenantID(ctx context.Context, tenantID string) context.Context {
	return context.WithValue(ctx, tenantCtxKeyInstance, tenantID)
}

func GetTenantID(ctx context.Context) string {
	return ctx.Value(tenantCtxKeyInstance).(string)
}
