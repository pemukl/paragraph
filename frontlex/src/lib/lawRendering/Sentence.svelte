<script lang="ts">
  import {onMount} from "svelte";
  import {browser} from "$app/environment";
  import {nanoid} from "$lib/utils/nanoid";
  import type {TextSegment} from "$lib/segment";
  import {textSegmentFromJson, TextSegmentType} from "$lib/segment";
  import SegmentRenderer from "./SegmentRenderer.svelte";
  import Popup from "$lib/references/ReferenceRenderer.svelte";
  import TextSpan from "$lib/lawRendering/TextSpan.svelte";

  export let selected = false;
  export let segment: TextSegment;

  let popupActive = false;

  function onEnter() {
    selected = popupActive = true;
  }
  function onLeave() {
    selected = popupActive = false;
  }

  if(typeof segment.content === "string"){
    let text = segment.content;
    segment.content = textSegmentFromJson({content: text, type: TextSegmentType.TextSpan});
    }

  export let path;
  path += "-Sent"+segment.ordinal
  export let id;
  id += "-Sent" + segment.ordinal;
  export let onNew;
</script>

<span class="sentence" id={id} class:selected>
  <span
    class="ordinal"
    id={`${id}ordinal`}
    on:mouseenter={onEnter}
    on:mouseleave={onLeave}
    >
    <span class="char">{segment.ordinal}</span>
    <span class="pipe">&nbsp;&nbsp;|</span>
    {#if popupActive}
      <Popup references= {segment.references} id={id} />
    {/if}
  </span>

  <SegmentRenderer {selected} segments={segment.content} id={id} onNew={onNew}/>

</span>

<style lang="scss">
  @import "../styles/main.scss";
  .sentence {
    &::after {
      content: " ";
    }
    &.selected {
      background: var(--selected-background);
    }
  }

  .ordinal {
    @extend clickable;
    position: relative;
    padding-left: 0.1rem;
    padding-right: 0.1rem;
    @include desktop {
      padding-bottom: 1.5px;
    }

    color: #ad003d;
    .char {
      font-size: 12px;
      position: absolute;
      top: 0.05rem;
      left: 0.18rem;
    }
  }
</style>
