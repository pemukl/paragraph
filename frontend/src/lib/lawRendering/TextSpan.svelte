<script>
    import ReferenceRenderer from "$lib/references/ReferenceRenderer.svelte";
    import Reference from "$lib/lawRendering/Reference.svelte";

    export let selected = false;
    export let segment;

    export let text;
    export let onNew;

    if(segment.text){
        text = segment.text
    } else {
        text = segment.content
    }



    // iterate over all links in segment.links
    let plains = []
    export let links = segment.links
    let lastend = 0
    let texts = []
    let urls = []


    for (let ind in links){
        let link = links[ind]
        plains.push(text.slice(lastend,link.start_idx))
        texts.push(text.slice(link.start_idx,link.stop_idx))
        urls.push(link.url)
        lastend = link.stop_idx
    }
    plains.push(text.slice(lastend,text.length))
</script>

<span class="textspan">
    {#each plains as plain, i}
        {#if i>0}
            <Reference text={texts[i-1]} url={urls[i-1]} onNew={onNew}></Reference>
        {/if}
        {@html plain}
    {/each}
</span>


<style>
    .textspan {
        display: inline;
    }
</style>
