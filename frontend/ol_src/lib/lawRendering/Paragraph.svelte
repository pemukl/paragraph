<script lang="ts">
  import type { TextSegment } from "$lib/segment";
  import SegmentRenderer from "$lib/lawRendering/SegmentRenderer.svelte";

  export let segment: TextSegment;
  export let selected = false;
  if (!segment.title) {
    console.warn("No title for segment", segment);
  }

  export let id;
  if (segment.ordinal) {
    id += "-Par" + segment.ordinal;
  } else {
    id += "-Par" + segment.title;
  }
  export let onNew;
</script>

<div class="Paragraph" id={id}>
  {#if segment.ordinal}
    <h5 class="title serif">§ {segment.ordinal} {segment.title}</h5>
  {:else}
    <h5 class="title serif">{segment.title}</h5>
  {/if}

  <p class="content">
    <SegmentRenderer segments={segment.content} {selected} id={id} onNew={onNew}/>
  </p>
</div>

<style lang="scss">
  @import "../styles/main.scss";
  .title {
    text-align: center;
    font-weight: 650px;
    display: block;
  }
  .content {
    margin: 0 0 3rem;
  }

  p {
    margin-bottom: 1rem;
    &.selected {
      background: var(--selected-background);
    }
  }
</style>
