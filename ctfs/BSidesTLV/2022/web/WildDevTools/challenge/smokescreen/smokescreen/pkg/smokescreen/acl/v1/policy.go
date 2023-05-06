package acl

import "fmt"

// DecisionResult represents the result of checking the ACL
type DecisionResult int

const (
	Allow DecisionResult = iota
	AllowAndReport
	Deny
)

func (d DecisionResult) String() string {
	return [...]string{"Allow", "AllowAndReport", "Deny"}[d]
}

// EnforcementPolicy represents what the policy is for a service
type EnforcementPolicy int

const (
	Unknown EnforcementPolicy = iota
	Open
	Report
	Enforce
)

var EnforcementPolicies = map[string]EnforcementPolicy{
	"open":    Open,
	"report":  Report,
	"enforce": Enforce,
}

func (p EnforcementPolicy) String() string {
	return [...]string{"Unknown", "Open", "Report", "Enforce"}[p]
}

func PolicyFromAction(action string) (EnforcementPolicy, error) {
	if v, ok := EnforcementPolicies[action]; ok {
		return v, nil
	}
	return Unknown, fmt.Errorf("unknown action %v", action)
}
