import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import cssInjectedByJsPlugin from 'vite-plugin-css-injected-by-js';

export default defineConfig({
    plugins: [
        react(),
        cssInjectedByJsPlugin(), // Injects all CSS directly into the JS file
    ],
    build: {
        outDir: 'dist',
        cssCodeSplit: false, // Prevents CSS from being split into multiple files
        rollupOptions: {
            output: {
                // Forces the output file to have a consistent name instead of a random hash
                entryFileNames: 'bulkhead-widget.js',
                assetFileNames: 'bulkhead-widget.[ext]',
                // Disables code splitting so everything stays in one file
                manualChunks: undefined,
            },
        },
    },
    // Ensures the widget doesn't clash with the host website's environment
    define: {
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
    },
});