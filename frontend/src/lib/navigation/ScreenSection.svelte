<script>
</script>

<div class="ScreenSection">
	<slot />
</div>

<style lang="scss">
	@import "../styles/variables";
	.ScreenSection {
		border: 1px solid $off-black-color;
		min-height: 75vh;
		max-width: 1100px;
		overflow-y: auto;
		margin: auto;
        padding: 3rem;
		position: relative;
		background-color: var(--background);
	}
</style>
