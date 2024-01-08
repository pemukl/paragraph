<script lang="ts">
	import { browser } from '$app/environment';

	import { onMount } from 'svelte';
	import { nanoid } from './utils/nanoid';
	export let leftColor = '#165abd';
	export let rightColor = '#240062';
	let uid: string;
	onMount(async () => {
		if (browser) {
			uid = nanoid(8);
		}
	});
</script>

<svg
	width="100%"
	height="100%"
	viewBox="0 0 1182 1182"
	version="1.1"
	xmlns="http://www.w3.org/2000/svg"
	xmlns:xlink="http://www.w3.org/1999/xlink"
	xml:space="preserve"
	style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;"
	><rect x="0" y="0" width="1181.1" height="1181.1" style="fill:url(#{uid});" /><g
		><g
			><path
				d="M206.259,855.433l-0,-234.603l34.463,-0l-0,204.986l114.655,-0l0,29.617l-149.118,-0Z"
				style="fill:#fff;"
			/><path
				d="M719.608,798.93l-0,-178.1l32.279,-0l-0,234.603l-26.289,-0l-136.103,-178.951l-0,178.951l-32.279,-0l-0,-234.603l26.622,-0l135.77,178.1Z"
				style="fill:#fff;"
			/><path
				d="M882.04,734.289l126.452,121.144l-44.259,-0l-115.804,-109.482l0,109.482l-34.608,-0l0,-234.603l34.608,-0l0,105.488l108.483,-105.488l42.928,-0l-117.8,113.459Z"
				style="fill:#fff;"
			/><path
				d="M427.642,726.63l197.549,-298.283l-69.236,-102.677l40.616,-0l48.157,72.97l48.727,-72.97l40.045,-0l-68.947,102.644l87.334,131.997l-38.661,-0l-68.498,-102.206l-200.614,298.756l-0,98.572l-34.663,-0l0.055,-0.389l0.029,-98.171l-91.208,-136.043l39.932,-0l69.383,105.8Z"
				style="fill:#fff;"
			/><path
				d="M358.019,560.311l0,-234.603l145.58,-0l0,27.62l-113.754,-0l0,73.875l106.507,-0l-0,27.953l-106.507,-0l0,77.202l113.754,0l0,27.953l-145.58,-0Z"
				style="fill:#fff;"
			/><path
				d="M172.611,560.311l-0,-234.603l33.676,-0l0,204.986l112.04,0l-0,29.617l-145.716,-0Z"
				style="fill:#fff;"
			/></g
		></g
	><defs
		><linearGradient
			id={uid}
			x1="0"
			y1="0"
			x2="1"
			y2="0"
			gradientUnits="userSpaceOnUse"
			gradientTransform="matrix(1181.1,1181.1,-1181.1,1181.1,-3.41061e-13,0)"
			><stop offset="0" style="stop-color:{leftColor};stop-opacity:1" /><stop
				offset="1"
				style="stop-color:{rightColor};stop-opacity:1"
			/></linearGradient
		></defs
	></svg
>

<style>
	svg {
		height: 256px;
		width: 256px;
	}
</style>
