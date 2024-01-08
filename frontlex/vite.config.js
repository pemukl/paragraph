import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite'
import fs from 'fs';

/** @type {import('vite').UserConfig} */

export default defineConfig(({ command }) => {
    if (command === 'serve') {
        return {
            plugins: [sveltekit()],
            test: {
                include: ['src/**/*.{test,spec}.{js,ts}']
            }
        }
    } else {
        // command === 'build'
        return {
            plugins: [sveltekit()],
            test: {
                include: ['src/**/*.{test,spec}.{js,ts}']
            },
            server: {
                strictPort: true,
                https: {
                    key: fs.readFileSync(`/etc/letsencrypt/live/shnei.de/privkey.pem`),
                    cert: fs.readFileSync(`/etc/letsencrypt/live/shnei.de/cert.pem`)
                }
            }
        }
    }
})