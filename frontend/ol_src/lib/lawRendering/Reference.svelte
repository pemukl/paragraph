<script lang="ts">
    import type { TextSegment } from "$lib/segment";
    import {Reference} from "$lib/references/references";
    import Bafin from "$lib/references/Bafin.svelte";
    import Bundesadler from "$lib/references/Bundesadler.svelte";
    import EBA from "$lib/references/EBA.svelte";
    import Drucksache from "$lib/references/Drucksache.svelte";
    import Ministerium from "$lib/references/Ministerium.svelte";
    import Verweis from "$lib/references/Verweis.svelte";
    import Rechtsprechung from "$lib/references/Rechtsprechung.svelte";
    import Weblink from "$lib/references/Weblink.svelte";

    export let reference = null;
    export let url = null;
    export let text;

    if(!url){
        if(reference.text){
            text = reference.text
        } else {
            text = reference.content
        }
        url = reference.url
    }

    export let onNew;
    export let type;
    export let link = url
    if(url.startsWith("https")) {
        type = "weblink"
    } else {
        let parts = url.split("-")
        let tag = parts.shift()
        if(tag == "DE") {
            type = "ref"
        } else if(tag == "EU") {
            type = "eu"
        } else if(tag == "DEF") {
            type = "def"
        } else {
            console.log("unknown reference type: " + tag)
        }

        if(parts[0].startsWith("https")){
            link = parts.join("-")
        }
    }
    export let action
    if(link.startsWith("https")){
        action = window.open
    } else {
        action = onNew
    }

</script>

<span class={type} on:click={() => action(link)}>
    {text}
</span>



<style lang="scss">
  @import "../styles/main.scss";
</style>