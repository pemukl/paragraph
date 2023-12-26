<script lang="ts">
    import type { TextSegment } from "$lib/segment";
    import GenericRenderer from "./SegmentRenderer.svelte";
    import Popup from "$lib/references/ReferenceRenderer.svelte";

    export let segment: TextSegment;
    export let selected: boolean = false;
    export let popupActive: boolean = false;

    function onEnter() {
      selected = true;
      popupActive = true;
    }
    function onLeave() {
      selected = false;
      popupActive = false;
    }



    export let id;
    //export let label = String.fromCharCode(96 + Number(segment.ordinal));

    id += "-Lit" + segment.ordinal;
    export let onNew;
</script>

<div class="lit" class:selected id={id}>
  <span class="ordinal" on:mouseenter={onEnter} on:mouseleave={onLeave}>
    {segment.ordinal}
    {#if popupActive}
      <Popup references= {segment.references} id="{id}" onNew={onNew} />
    {/if}
  </span>&emsp;
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
  .lit {
    margin-bottom: 0.2rem;
    margin-top: 0.6rem;
    display: flex;
    flex-direction: row;
    &.selected {
      background: var(--selected-background);
    }
  }
</style>
