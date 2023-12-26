<script lang="ts">
    import type { TextSegment } from "$lib/segment";
    import SegmentRenderer from "$lib/lawRendering/SegmentRenderer.svelte";

    export let segment: TextSegment;
    export let selected = false;
    if (!segment.title) {
        console.warn("No title for segment", segment);
    }

    export let id;
    export let myid = id;
    if (segment.ordinal) {
        myid += "-Area" + segment.ordinal;
    } else {
        myid += "-Area" + segment.title;
    }
    export let onNew;
</script>

<div class="Area" id={myid}>
    {#if segment.ordinal}
        <h5 class="areatitle">{segment.ordinal}<br>{segment.title}</h5>
    {:else}
        <h5 class="title serif">{segment.title}</h5>
    {/if}

    <p class="content">
        <SegmentRenderer segments={segment.content} {selected} id={id} onNew={onNew}/>
    </p>
</div>

<style lang="scss">
  @import "../styles/main.scss";
  .areatitle {
    font-family: "EB Garamond", serif;
    font-weight: 200;
    line-height: 1.3;
    padding: 0;
    margin: 4rem 0 3rem;
    font-size: 1.3rem;
    text-align: center;
    text-decoration: underline;
    text-decoration-thickness: 0.08rem;
    .serif {
      font-family: "EB Garamond", serif;
    }
  }
  .content {
    margin-bottom: 15rem;
    margin: 2rem 0 3rem;
  }

  p {
    margin-bottom: 1rem;
    &.selected {
      background: var(--selected-background);
    }
  }

</style>
