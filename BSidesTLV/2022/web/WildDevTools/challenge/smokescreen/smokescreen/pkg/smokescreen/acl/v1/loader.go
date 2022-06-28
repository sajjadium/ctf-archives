package acl

// Loader is an interface used to return a parsed ACL from an abstract source
type Loader interface {
	Load() (*ACL, error)
}
