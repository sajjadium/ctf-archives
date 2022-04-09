module.exports = {
	"env": {
		"browser": true,
		"es6": true,
		"node": true
	},
	"extends": [
		"plugin:@typescript-eslint/recommended",
		"plugin:@typescript-eslint/recommended-requiring-type-checking"
	],
	"parser": "@typescript-eslint/parser",
	"parserOptions": {
		"tsconfigRootDir": __dirname,
		"project": [ "./packages/*/tsconfig.json" ],
		"sourceType": "module"
	},
	"plugins": [
		"@typescript-eslint",
		"eslint-comments",
		"eslint-plugin-import",
		"eslint-plugin-jsdoc",
		"eslint-plugin-prefer-arrow",
		"simple-import-sort",
	],
	"ignorePatterns": [ ".eslintrc.js", "dist", "vite.config.js" ],
	"rules": {
		"@typescript-eslint/adjacent-overload-signatures": "error",
		"@typescript-eslint/array-type": [
			"error",
			{
				"default": "array"
			}
		],
		"@typescript-eslint/ban-types": "error",
		"@typescript-eslint/consistent-type-assertions": "error",
		"@typescript-eslint/consistent-type-definitions": "off",
		"@typescript-eslint/dot-notation": "error",
		"@typescript-eslint/explicit-member-accessibility": [
			"error",
			{
				"accessibility": "explicit"
			}
		],
		"@typescript-eslint/indent": "off",
		"@typescript-eslint/member-delimiter-style": [
			"error",
			{
				"multiline": {
					"delimiter": "semi",
					"requireLast": true
				},
				"singleline": {
					"delimiter": "semi",
					"requireLast": false
				}
			}
		],
		"@typescript-eslint/member-ordering": "error",
		"@typescript-eslint/naming-convention": [
			"error",
			{
				selector: "default",
				format: ["camelCase"],
				leadingUnderscore: "allow",
				trailingUnderscore: "allow",
			},
			{
				selector: "enumMember",
				format: ["PascalCase", "UPPER_CASE"],
				leadingUnderscore: "allow",
				trailingUnderscore: "allow",
			},
			{
				selector: "variable",
				format: ["camelCase", "PascalCase", "UPPER_CASE"],
				leadingUnderscore: "allow",
				trailingUnderscore: "allow",
			},
			{
				selector: "parameter",
				format: ["camelCase", "PascalCase"],
				leadingUnderscore: "allow",
				trailingUnderscore: "allow",
			},
			{
				selector: ["typeAlias", "enum", "interface", "class", "typeParameter"],
				format: ["PascalCase"],
				leadingUnderscore: "allow",
				trailingUnderscore: "allow",
			},
			{
				selector: ["property", "typeProperty"],
				format: ["camelCase", "snake_case", "PascalCase"],
				leadingUnderscore: "allow",
				trailingUnderscore: "allow",
			}
		],
		"@typescript-eslint/no-empty-function": "error",
		"@typescript-eslint/no-empty-interface": "off",
		"@typescript-eslint/no-explicit-any": "off",
		"@typescript-eslint/no-misused-new": "error",
		"@typescript-eslint/no-misused-promises": [
			"error",
			{
				"checksVoidReturn": false
			}
		],
		"@typescript-eslint/no-namespace": "off",
		"@typescript-eslint/no-non-null-assertion": "off",
		"@typescript-eslint/no-parameter-properties": "off",
		"@typescript-eslint/no-unused-expressions": "error",
		"@typescript-eslint/no-use-before-define": "off",
		"@typescript-eslint/no-var-requires": "error",
		"@typescript-eslint/prefer-for-of": "error",
		"@typescript-eslint/prefer-function-type": "error",
		"@typescript-eslint/prefer-namespace-keyword": "error",
		"@typescript-eslint/quotes": [
			"error",
			"double",
			{
				"avoidEscape": true
			}
		],
		"@typescript-eslint/semi": [
			"error",
			"always"
		],
		"@typescript-eslint/triple-slash-reference": [
			"error",
			{
				"path": "always",
				"types": "prefer-import",
				"lib": "always"
			}
		],
		"@typescript-eslint/type-annotation-spacing": "error",
		"@typescript-eslint/unified-signatures": "error",
		"@typescript-eslint/no-floating-promises": "off",
		"@typescript-eslint/explicit-module-boundary-types": "off",
		"@typescript-eslint/no-shadow": [
			"error",
			{
				"allow": [
					"AsJson",
					"ConstructorArgs",
					"Marshaller"
				]
			}
		],
		"@typescript-eslint/no-unused-vars": [
			"error",
			{
				"varsIgnorePattern": "^_",
				"argsIgnorePattern": "^_",
			}
		],
		"@typescript-eslint/no-unsafe-member-access": "off",
		"@typescript-eslint/no-non-null-assertion": "off",
		"@typescript-eslint/unbound-method": [
			"error",
			{
				"ignoreStatic": true
			}
		],
		"arrow-body-style": "error",
		"arrow-parens": [
			"error",
			"always"
		],
		"brace-style": [
			"error",
			"1tbs"
		],
		"comma-dangle": "off",
		"comma-spacing": [
			"error",
			{
				"before": false,
				"after": true
			}
		],
		"complexity": "off",
		"constructor-super": "error",
		"curly": "error",
		"eol-last": "error",
		"eqeqeq": [
			"error",
			"smart"
		],
		"guard-for-in": "error",
		"id-blacklist": [
			"error",
			"any",
			"Number",
			"number",
			"String",
			"string",
			"Boolean",
			"boolean",
			"Undefined",
			"undefined"
		],
		"id-match": "error",
		"import/order": "off",
		"jsdoc/check-alignment": "error",
		"jsdoc/check-indentation": "error",
		"jsdoc/newline-after-description": "error",
		"max-classes-per-file": "off",
		"max-len": [
			"error",
			{
				"code": 120
			}
		],
		"new-parens": "error",
		"no-bitwise": "off",
		"no-caller": "error",
		"no-cond-assign": "error",
		"no-console": "error",
		"no-debugger": "error",
		"no-empty": "error",
		"no-eval": "error",
		"no-fallthrough": "off",
		"no-invalid-this": "off",
		"no-multiple-empty-lines": "off",
		"no-new-wrappers": "error",
		"no-shadow": "off",
		"no-throw-literal": "error",
		"no-trailing-spaces": "error",
		"no-undef-init": "error",
		"no-underscore-dangle": "error",
		"no-unsafe-finally": "error",
		"no-unused-labels": "error",
		"no-var": "error",
		"object-shorthand": "error",
		"one-var": [
			"error",
			"never"
		],
		"prefer-arrow/prefer-arrow-functions": "off",
		"prefer-const": "off",
		"quote-props": [
			"error",
			"consistent-as-needed"
		],
		"radix": "error",
		"space-before-function-paren": [
			"error",
			{
				"anonymous": "never",
				"asyncArrow": "always",
				"named": "never"
			}
		],
		"spaced-comment": [
			"error",
			"always",
			{
				"markers": [
					"/"
				]
			}
		],
		"use-isnan": "error",
		"valid-typeof": "off",
		"simple-import-sort/imports": [
			"error",
			{
				"groups": [
					["^(?!(\\.|\\/))"], // external packages
					["^@amongst/"], // internal packages
					["^\\/"], // absolute paths
					["^\\."], // relative paths
					["\\.s?css$"] // styles
				]
			}
		],
		"simple-import-sort/exports": "error",
		"eslint-comments/no-unused-disable": "error",
		"strict": [
			"error",
			"never"
		],
		"@typescript-eslint/require-await": "off"
	}
};
