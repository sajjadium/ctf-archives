package markup

import (
	"html"
	"regexp"
)

var (
	boldRe         = regexp.MustCompile(`\*.*?\*`)
	boldReplacer   = replacer("b")
	italicRe       = regexp.MustCompile(`\/.*?\/`)
	italicReplacer = replacer("i")
	codeRe         = regexp.MustCompile(`\x60.*?\x60`)
	codeReplacer   = replacer("pre")
)

// ToHTML formats markup as HTML.
func ToHTML(markup string) string {
	result := html.EscapeString(markup)
	result = italicRe.ReplaceAllStringFunc(result, italicReplacer)
	result = boldRe.ReplaceAllStringFunc(result, boldReplacer)
	result = codeRe.ReplaceAllStringFunc(result, codeReplacer)
	return result
}

func replacer(tag string) func(s string) string {
	return func(s string) string {
		return "<" + tag + ">" + s[1:len(s)-1] + "</" + tag + ">"
	}
}
