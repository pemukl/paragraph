<div class="header">
	<slot />
</div>

<style>
	.header {
        width: 100%;
		margin: auto;
        padding: 1rem;
		position: fixed;
        top: 0;
		background-color: var(--primary);
        min-height: 2rem;
        box-shadow: 0 0 5px var(--foreground);
        z-index: 1000;
	}
</style>
