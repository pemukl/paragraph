<script lang="ts">
  import type { TextSegment } from "$lib/segment";
  import GenericRenderer from "./SegmentRenderer.svelte";
  import Popup from "$lib/references/ReferenceRenderer.svelte";

  export let segment: TextSegment;
  export let selected: boolean = false;
  let popupActive = false;

  function onEnter() {
    selected = true;
    popupActive = true;
  }
  function onLeave() {
    selected = false;
    popupActive = false;
  }

  export let id;
  id += "-Enum" + segment.ordinal;
  export let onNew;
  </script>



<div class="enum" class:selected id={id}>

    <div class="ordinal" on:mouseenter={onEnter} on:mouseleave={onLeave}>
        <span >
            {segment.ordinal}.
            {#if popupActive}
                <Popup references= {segment.references} id="{id}" />
            {/if}
        </span>
  </div>
  <div>
    <GenericRenderer segments={segment.content} {selected} id={id} onNew={onNew}/>
  </div>
</div>

<style lang="scss">
  @import "../styles/main.scss";
  .ordinal {
    @extend clickable;
    position: relative;
    display: inline;
    margin-left: calc(1.7rem * var(--order));
    margin-right: 0.85rem;
  }
  .enum {
    margin-bottom: 0.2rem;
    margin-left: 2rem;
    margin-top: 0.6rem;
    display: flex;
    flex-direction: row;
    &.selected {
      background: var(--selected-background);
    }
  }
</style>
