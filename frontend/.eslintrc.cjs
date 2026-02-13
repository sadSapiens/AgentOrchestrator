export default {
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:react-hooks/recommended',
        'prettier'
    ],
    plugins: ['react', 'react-hooks', 'prettier'],
    parserOptions: {
        ecmaVersion: 2022,
        sourceType: 'module',
        ecmaFeatures: {
            jsx: true
        }
    },
    env: {
        browser: true,
        es2022: true,
        node: true
    },
    settings: {
        react: {
            version: 'detect'
        }
    },
    rules: {
        'prettier/prettier': 'error',
        'react/react-in-jsx-scope': 'off',
        'react/prop-types': 'off'
    },
    ignorePatterns: ['dist', 'node_modules']
};
