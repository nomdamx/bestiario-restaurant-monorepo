const { defineConfig } = require("eslint/config");
const expoConfig = require("eslint-config-expo/flat");
const prettierPlugin = require("eslint-plugin-prettier");
const prettierConfig = require("eslint-config-prettier");

module.exports = defineConfig([
    expoConfig,

    prettierConfig,

    {
        ignores: ["dist/*"],

        plugins: {
            prettier: prettierPlugin,
        },

        rules: {
            "prettier/prettier": "error",
        },
    },
]);
