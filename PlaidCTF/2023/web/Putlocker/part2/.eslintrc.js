module.exports = {
	"extends": [
		"plugin:@typescript-eslint/recommended",
		"plugin:@typescript-eslint/recommended-requiring-type-checking"
	],
	"parser": "@typescript-eslint/parser",
	"parserOptions": {
		"tsconfigRootDir": __dirname,
		"project": ["./packages/*/tsconfig.json", "./packages/*/test/tsconfig.json"],
		"sourceType": "module"
	},
	"plugins": [
		"@typescript-eslint",
		"simple-import-sort",
	],
	"ignorePatterns": [
		".eslintrc.js",
		"webpack.config.js"
	],
	"rules": {
		"max-len": [
			"error",
			{ code: 120 }
		],
		"no-console": "warn",
		"@typescript-eslint/ban-types": [
			"error",
			{
				"extendDefaults": false,
				"types": {
					"Object": {
						"message": "Avoid using the `Object` type. Did you mean `object`?"
					},
					"Function": {
						"message": "Avoid using the `Function` type. Prefer a specific function type, like `() => void`."
					},
					"Boolean": {
						"message": "Avoid using the `Boolean` type. Did you mean `boolean`?"
					},
					"Number": {
						"message": "Avoid using the `Number` type. Did you mean `number`?"
					},
					"String": {
						"message": "Avoid using the `String` type. Did you mean `string`?"
					},
					"Symbol": {
						"message": "Avoid using the `Symbol` type. Did you mean `symbol`?"
					}
				}
			}
		],
        "@typescript-eslint/no-unused-vars": [
            "error",
            {
                "varsIgnorePattern": "^_",
                "argsIgnorePattern": "^_",
            }
        ],
		"@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-non-null-assertion": "off",
        "@typescript-eslint/no-namespace": "off",
        "@typescript-eslint/no-empty-interface": "off",
        "@typescript-eslint/no-floating-promises": "off",
        "@typescript-eslint/no-misused-promises": "off",
        "@typescript-eslint/explicit-module-boundary-types": "off",
        "@typescript-eslint/semi": [
            "error",
            "always"
        ],
		"simple-import-sort/imports": [
			"error",
			{
				"groups": [
					["^\\u0000.*(?<!\\.s?css)$"], // Side effect imports (but not css)
					["^(@(?!davy\\/))?\\w"], // node builtins and external packages
					["^@davy\\/"], // internal packaages
					["^(?!(\\.|@\\/))"], // anything that's not a relative import
					["^@\\/"], // absolute imports
					["^\\."], // relative imports
					["\\.s?css$"] // style imports
				]
			}
		],
		"simple-import-sort/exports": "error"
	}
};
