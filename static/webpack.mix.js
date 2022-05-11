const mix = require("laravel-mix");
const tailwindcss = require("tailwindcss");

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel applications. By default, we are compiling the CSS
 | file for the application as well as bundling up all the JS files.
 |
 */

mix.js("src/js/app.js", "dist/js")
    .js("src/js/ckeditor-classic.js", "dist/js")
    .js("src/js/ckeditor-inline.js", "dist/js")
    .js("src/js/ckeditor-balloon.js", "dist/js")
    .js("src/js/ckeditor-balloon-block.js", "dist/js")
    .js("src/js/ckeditor-document.js", "dist/js")
    .sass("src/sass/app.scss", "dist/css")
    .options({
        processCssUrls: false,
        postCss: [tailwindcss("./tailwind.config.js")],
    })
    .autoload({
        "cash-dom": ["cash"],
    })
    .copyDirectory("src/json", "dist/json")
    .copyDirectory("src/fonts", "dist/fonts")
    .copyDirectory("src/images", "dist/images")
    .browserSync({
        proxy: "icewall-html.test",
        files: ["src/**/*.*"],
    });
