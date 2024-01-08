<script>
	export let ref;
	export let onNew;
	export let hover;
	export let filter;
	$: if(!hover){
		filter = "grayscale(1) opacity(0.6)";
	} else {
		filter = "grayscale(0);";
	}
</script>

{#if ref.content}
	<span class="ref" on:click={() => onNew(ref.url)}>
		{ref.content}
	</span>
{:else}
	<svg
			filter={filter}
			width="100%"
			height="100%"
			viewBox="0 0 473 473"
			version="1.1"
			xmlns="http://www.w3.org/2000/svg"
			xmlns:xlink="http://www.w3.org/1999/xlink"
			xml:space="preserve"
			xmlns:serif="http://www.serif.com/"
			style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;"
	><g
		><rect x="-0" y="0" width="472.441" height="472.441" style="fill:#545454;" /><path
			d="M206.154,472.346l25.225,-62.773l-0.16,-42.157l-33.609,-22.881l-81.324,-0.063l10.898,-17.77l21.759,-8.843l137.628,0.539l-0,-14.946l-147.44,-0.54l-24.544,11.158l-25.226,40.787l-0.57,-60.521l11.749,-55.738l25.618,-34.37l43.419,-21.326l47.109,-10.303l133.398,0.238l67.457,7.42l54.885,14.431l0.015,277.753l-266.287,-0.095Zm74.462,-262.252l-43.61,0l-0,43.61l43.61,0l-0,-43.61Z"
			style="fill:#fcfafc;"
	/></g
	></svg
	>

{/if}

<style lang="scss">
	@import "../styles/main.scss";
</style>


