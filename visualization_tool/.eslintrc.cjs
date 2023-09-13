module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["@typescript-eslint", "react"],
  rules: {
    "@typescript-eslint/naming-convention": [
        "error",
        {
            "selector": ["variable", "function", "parameter"],
            "format": ["camelCase", "PascalCase"],
        },
        {
            "selector": "typeLike",
            "format": ["PascalCase"],
        }
    ],
  },
};
