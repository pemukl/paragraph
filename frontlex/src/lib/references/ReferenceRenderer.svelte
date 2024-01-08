<script lang="ts">
    import { TextSegmentType, TextSegment } from "$lib/segment";
    import type {Reference} from "$lib/references/references";
    import Bafin from "$lib/references/Bafin.svelte";
    import Bundesadler from "$lib/references/Bundesadler.svelte";
    import Copy from "$lib/references/Copy.svelte";
    import Drucksache from "$lib/references/Drucksache.svelte";
    import Eba from "$lib/references/EBA.svelte";
    import Ministerium from "$lib/references/Ministerium.svelte";
    import Rechtsprechung from "$lib/references/Rechtsprechung.svelte";
    import Synopse from "$lib/references/Synopse.svelte";
    import EBA from "$lib/references/EBA.svelte";
    import Verweis from "$lib/references/Verweis.svelte";
    import RefItem from "$lib/references/RefItem.svelte";

    export let active = true;
    export let references: Reference[];
    export let id;

    let parts = id.split("-");
    export let link = parts[parts.length-1];
    let translated = [];
    for (let idx in parts){
        let part = parts[idx];
        //if(part.startsWith("Area")){translated.push("Abschnitt\u00A0" + part.substring(4));} else
        if(part.startsWith("Par")){
            translated.push("§\u00A0" + part.substring(3));
        }else if(part.startsWith("Sec")){
            translated.push("Abs.\u00A0" + part.substring(3));
        }else if(part.startsWith("Sent")){
            translated.push("Satz\u00A0" + part.substring(4));
        }else if(part.startsWith("Enum")){
            translated.push("Nr.\u00A0" + part.substring(4));
        }else if(part.startsWith("Lit")){
            translated.push("lit.\u00A0"+part.substring(3));
        }
    }
    translated.push(parts[2])
    export let idstring = translated.join(" ");
    export let copied = false;

    function copyToClip(content) {
        console.log("copying to clipboard: "+content);
        const blobInput = new Blob([content], { type: 'text/html' });
        const clipboardItemInput = new ClipboardItem({ 'text/html': blobInput });
        navigator.clipboard.write([clipboardItemInput]);
        copied = true;
    }

    function shortenLink(link){
        if(!link.startsWith("https")){
            let splits = link.split("-");
            splits.shift();
            link = splits.join("-");
        }
        console.log("created link: "+link);
        return link
    }

</script>


<div class="popup">
    <RefItem let:hover action={() => copyToClip(idstring)} text={idstring}>
        <Copy copied={copied} hover={hover}/>
    </RefItem>

    {#each references as reference}
        <RefItem let:hover text={reference.text} action={() => window.open(shortenLink(reference.url))} >
            {#if reference.url.startsWith("BTDRS")}
                <Bundesadler  ref={reference} hover={hover}/>
            {:else if reference.url.startsWith("BRDRS")}
                <Drucksache  ref={reference} hover={hover}/>
            {:else}
                <Ministerium  ref={reference} hover={hover}/>
            {/if}
        </RefItem>

    {/each}
</div>


<style lang="scss">


  .popup {
    position: absolute;
    top: -35px;
    left: 0;
    width: 35px;
    border-radius: 4px;
    background-color: var(--background);
    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    transition: all ease 100ms;
    border-top-right-radius: 0;
    font-family: "Mulish", serif;

    .item {
      height: 31px;
      width: 31px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 2px;
      position: relative;


      .inner {

        display: flex;
        align-items: center;
        justify-content: center;
        height: 20px;
        width: 20px;
        &:hover *{
          font-weight:600;
        }

        }



      .extension {
        position: absolute;
        right: 0;
        left: 33px;
        width: fit-content;
        white-space: nowrap;
        height: 35px;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
        background-color: var(--background);
        z-index: 1;
        box-shadow: 10px 10px 10px rgba(0, 0, 0, 0.2);
        flex-direction: row;
        justify-content: center;
        align-items: center;
        padding-left: 7px;
        padding-right: 10px;
        color: black;
        display: flex;
      }

    }
    display: block;
    cursor: pointer;

  }
</style>
