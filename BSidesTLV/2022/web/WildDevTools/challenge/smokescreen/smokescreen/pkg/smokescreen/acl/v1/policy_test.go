package acl

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPolicyStrings(t *testing.T) {
	a := assert.New(t)

	// DecisionResults
	a.Equal("Allow", Allow.String())
	a.Equal("AllowAndReport", AllowAndReport.String())
	a.Equal("Deny", Deny.String())

	// EnforcementPolicies
	a.Equal("Unknown", Unknown.String())
	a.Equal("Open", Open.String())
	a.Equal("Report", Report.String())
	a.Equal("Enforce", Enforce.String())
}
