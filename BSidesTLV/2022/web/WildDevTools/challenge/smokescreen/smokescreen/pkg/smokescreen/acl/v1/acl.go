package acl

import (
	"fmt"
	"strings"

	"github.com/sirupsen/logrus"
)

type Decider interface {
	Decide(service, host string) (Decision, error)
}

type ACL struct {
	Rules            map[string]Rule
	DefaultRule      *Rule
	GlobalDenyList   []string
	GlobalAllowList  []string
	DisabledPolicies []EnforcementPolicy
	*logrus.Logger
}

type Rule struct {
	Project     string
	Policy      EnforcementPolicy
	DomainGlobs []string
}

type Decision struct {
	Reason  string
	Default bool
	Result  DecisionResult
	Project string
}

func New(logger *logrus.Logger, loader Loader, disabledActions []string) (*ACL, error) {
	acl, err := loader.Load()
	if err != nil {
		return nil, err
	}

	err = acl.DisablePolicies(disabledActions)
	if err != nil {
		return nil, err
	}

	err = acl.Validate()
	if err != nil {
		return nil, err
	}

	acl.Logger = logger

	if acl.DefaultRule == nil {
		acl.Warn("no default rule set. any services without a rule will be denied.")
	}
	return acl, nil
}

// Add associates a rule with the specified service after verifying the rule's
// policy and domains are valid. Add returns an error if the service rule
// already exists.
func (acl *ACL) Add(svc string, r Rule) error {
	err := acl.PolicyDisabled(svc, r.Policy)
	if err != nil {
		return err
	}

	err = acl.ValidateDomainGlobs(svc, r.DomainGlobs)
	if err != nil {
		return err
	}

	if _, ok := acl.Rules[svc]; ok {
		return fmt.Errorf("rule already exists for service %v", svc)
	}
	acl.Rules[svc] = r
	return nil
}

// Decide takes uses the rule configured for the given service to determine if
//   1. The host is in the rule's allowed domain
//   2. The host has been globally denied
//   3. The host has been globally allowed
//   4. There is a default rule for the ACL
func (acl *ACL) Decide(service, host string) (Decision, error) {
	var d Decision

	rule := acl.Rule(service)
	if rule == nil {
		d.Result = Deny
		d.Reason = "no rule matched"
		return d, nil
	}

	d.Project = rule.Project
	d.Default = rule == acl.DefaultRule

	// if the host matches any of the rule's allowed domains, allow
	for _, dg := range rule.DomainGlobs {
		if hostMatchesGlob(host, dg) {
			d.Result, d.Reason = Allow, "host matched allowed domain in rule"
			return d, nil
		}
	}

	// if the host matches any of the global deny list, deny
	for _, dg := range acl.GlobalDenyList {
		if hostMatchesGlob(host, dg) {
			d.Result, d.Reason = Deny, "host matched rule in global deny list"
			return d, nil
		}
	}

	// if the host matches any of the global allow list, allow
	for _, dg := range acl.GlobalAllowList {
		if hostMatchesGlob(host, dg) {
			d.Result, d.Reason = Allow, "host matched rule in global allow list"
			return d, nil
		}
	}

	var err error
	switch rule.Policy {
	case Report:
		d.Result, d.Reason = AllowAndReport, "rule has allow and report policy"
	case Enforce:
		d.Result, d.Reason = Deny, "rule has enforce policy"
	case Open:
		d.Result, d.Reason = Allow, "rule has open enforcement policy"
	default:
		d.Result, d.Reason = Deny, "unexpected policy value"
		err = fmt.Errorf("unexpected policy value for (%s -> %s): %d", service, host, rule.Policy)
	}

	if d.Default {
		d.Reason = "default rule policy used"
	}

	return d, err
}

// DisablePolicies takes a slice of actions (open, report, enforce), maps them
// to their corresponding EnforcementPolicy, and adds them to the global
// disabledPolicy slice.
func (acl *ACL) DisablePolicies(actions []string) error {
	for _, a := range actions {
		p, err := PolicyFromAction(a)
		if err != nil {
			return err
		}
		acl.DisabledPolicies = append(acl.DisabledPolicies, p)
	}
	return nil
}

// Validate checks that the ACL that every rule has a conformant domain glob
// and is not utilizing a disabled enforcement policy.
func (acl *ACL) Validate() error {
	for svc, r := range acl.Rules {
		err := acl.ValidateDomainGlobs(svc, r.DomainGlobs)
		if err != nil {
			return err
		}
		err = acl.PolicyDisabled(svc, r.Policy)
		if err != nil {
			return err
		}
	}
	return nil
}

// ValidateDomainGlobs takes a slice of domain globs and verifies they conform to smokescreen's
// domain glob policy.
//
// Wildcards are valid only at the beginning of a domain glob, and only a single wildcard per glob
// pattern is allowed. Globs must include text after a wildcard.
func (acl *ACL) ValidateDomainGlobs(svc string, globs []string) error {
	for _, glob := range globs {
		if glob == "" {
			return fmt.Errorf("glob cannot be empty")
		}

		if glob == "*" || glob == "*." {
			return fmt.Errorf("%v: %v: domain glob must not match everything", svc, glob)
		}

		if !strings.HasPrefix(glob, "*.") && strings.HasPrefix(glob, "*") {
			return fmt.Errorf("%v: %v: domain glob must represent a full prefix (sub)domain", svc, glob)
		}

		domainToCheck := strings.TrimPrefix(glob, "*")
		if strings.Contains(domainToCheck, "*") {
			return fmt.Errorf("%v: %v: domain globs are only supported as prefix", svc, glob)
		}
	}
	return nil
}

// PolicyDisabled checks if an EnforcementPolicy is disabled at the ACL level
func (acl *ACL) PolicyDisabled(svc string, p EnforcementPolicy) error {
	for _, dp := range acl.DisabledPolicies {
		if dp == p {
			return fmt.Errorf("rule for svc:%v utilizes a disabled policy:%v", svc, p)
		}
	}
	return nil
}

// Project returns the configured project for a service
func (acl *ACL) Project(service string) (string, error) {
	rule := acl.Rule(service)
	if rule == nil {
		return "", fmt.Errorf("no rule for service: %v", service)
	}
	return rule.Project, nil
}

// Rule returns the configured rule for a service, or the default rule if none
// is configured.
func (acl *ACL) Rule(service string) *Rule {
	if service, ok := acl.Rules[service]; ok {
		return &service
	}
	return acl.DefaultRule
}

// hostMatchesGlob matches a hostname string against a domain glob after
// converting both to a canonical form (lowercase with trailing dots removed).
//
// domainGlob should already have been passed through ACL.Validate().
func hostMatchesGlob(host string, domainGlob string) bool {
	if host == "" {
		return false
	}

	h := strings.TrimRight(strings.ToLower(host), ".")
	g := strings.TrimRight(strings.ToLower(domainGlob), ".")

	if strings.HasPrefix(g, "*.") {
		suffix := g[1:]
		if strings.HasSuffix(h, suffix) {
			return true
		}
	} else if g == h {
		return true
	}
	return false
}
