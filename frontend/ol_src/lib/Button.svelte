<script>
	export let cta;
	export let href;
	export let big = false;
</script>

<a class="button" {href}>
	{cta}
</a>


<style lang="scss">
	.button {
		padding: 0.4rem 1.2rem;
		background: var(--primary);
		color: white;
		font-family: var(--sans-serif), sans-serif;
		text-decoration: none;
		text-transform: capitalize;
		transition: all 150ms ease;
		border-radius: 2rem;
		&:hover {
			background: rgb(112, 112, 236);
		}
		position: relative;
	}
</style>
