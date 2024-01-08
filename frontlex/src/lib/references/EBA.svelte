<script>
	export let ref;
	export let onNew;
</script>

{#if ref.content}
	<span class="eu" on:click={() => onNew(ref.url)} on:keyup={() => onNew(ref.url)}>
		{ref.content}
	</span>
{:else}
	<svg
			width="100%"
			height="100%"
			viewBox="0 0 473 473"
			version="1.1"
			xmlns="http://www.w3.org/2000/svg"
			xml:space="preserve"
			style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;"
	><g
		><rect x="345.593" y="0" width="17.748" height="472.516" style="fill:#ef9b38;" /><rect
			x="363.341"
			y="0"
			width="109.099"
			height="472.516"
			style="fill:#517993;"
	/><rect x="0" y="0" width="345.593" height="472.516" style="fill:url(#_Linear1);" /><g
	><path
				d="M237.428,389.658l26.324,-18.678l15.347,47.059l-41.671,-28.381Zm-40.563,28.381l15.34,-47.066l-39.408,-29.962l49.504,0.25l41.451,29.719l-26.324,18.678l-40.563,28.381Zm41.127,-123.731l15.691,46.952l49.505,-0.249l-39.427,29.962l-41.46,-29.713l15.691,-46.952Z"
				style="fill:#fff;"
			/><path
			d="M107.037,265.928l26.324,-18.679l15.347,47.059l-41.671,-28.38Zm-40.563,28.38l15.34,-47.065l-39.408,-29.963l49.504,0.25l41.451,29.719l-26.324,18.679l-40.563,28.38Zm41.127,-123.731l15.691,46.952l49.505,-0.249l-39.427,29.963l-41.46,-29.714l15.691,-46.952Z"
			style="fill:#fff;"
	/></g
	></g
	><defs
	><linearGradient
			id="_Linear1"
			x1="0"
			y1="0"
			x2="1"
			y2="0"
			gradientUnits="userSpaceOnUse"
			gradientTransform="matrix(345.593,0,0,386.194,-3.63798e-12,236.258)"
			><stop offset="0" style="stop-color:#5a8595;stop-opacity:1" /><stop
			offset="0.5"
			style="stop-color:#82a7b1;stop-opacity:1"
	/><stop offset="1" style="stop-color:#d4b3a4;stop-opacity:1" /></linearGradient
		></defs
	></svg
	>
{/if}

<style lang="scss">
	@import "../styles/main.scss";
</style>