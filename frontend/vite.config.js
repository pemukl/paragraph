import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite'

export default defineConfig(({ command }) => {
    return {
        plugins: [sveltekit()],
        test: {
            include: ['src/**/*.{test,spec}.{js,ts}']
        },
        server: {
            port: 80,
            strictPort: true,
            host: "0.0.0.0",
            //https: {
            //    key: fs.readFileSync(`/etc/letsencrypt/live/shnei.de/privkey.pem`),
            //    cert: fs.readFileSync(`/etc/letsencrypt/live/shnei.de/cert.pem`)
            //}
        }
    }
})