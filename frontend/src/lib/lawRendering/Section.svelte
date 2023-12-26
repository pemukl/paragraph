<script lang="ts">
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import { nanoid } from "$lib/utils/nanoid";
  import type { TextSegment } from "$lib/segment";
  import GenericRenderer from "./SegmentRenderer.svelte";
  import Popup from "$lib/references/ReferenceRenderer.svelte";

  export let selected = false;
  export let segment: TextSegment;

  let popupActive = false;

  let uid: string;

  onMount(async () => {
    if (browser) {
      uid = nanoid(8);
    }
  });
  function onEnter() {
    selected = popupActive = true;
  }
  function onLeave() {
    selected = popupActive = false;
  }
  export let id;
  if (segment.ordinal) {
    id += "-Sec" + segment.ordinal;
  } else {
    id += "-Sec" + segment.title;
  }
  export let onNew;
</script>

<div class="Section" id={id}>
  <p class:selected>
    <span><span
      class="ordinal"
      id={`${id}ordinal`}
      on:mouseenter={onEnter}
      on:mouseleave={onLeave}
    >
      {#if segment.ordinal}
        ({segment.ordinal})
      {/if}      
      {#if popupActive}
        <Popup references= {segment.references} id="{id}" />
      {/if}
    </span></span>
    <GenericRenderer segments={segment.content} {selected} id={id} onNew={onNew}/>
  </p>
</div>


<style lang="scss">
  @import "../styles/main.scss";
  .ordinal {
    @extend clickable;
    margin-right: 0.2rem;
    position: relative;
    display: inline-block;
  }
  p {
    margin-bottom: 1rem;
    &.selected {
      background: var(--selected-background);
    }
  }
</style>
