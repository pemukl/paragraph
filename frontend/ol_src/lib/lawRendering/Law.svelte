<script lang="ts">
    import type { TextSegment } from "$lib/segment";
    import SegmentRenderer from "$lib/lawRendering/SegmentRenderer.svelte";

    export let segment: TextSegment;
    export let selected = false;

    function onEnter() {
        selected = true;
    }
    function onLeave() {
        selected = false;
    }
    export let id;
    id += "-" + segment.abbreviation;
    export let onNew;
</script>
<div class="Law" id={id}>
  <h4 class="serif center">
    {segment.title} ({segment.abbreviation})
  </h4>
  <SegmentRenderer segments={segment.content} {selected} id={id} onNew={onNew}/>
</div>

<style lang="scss">
  @import "../styles/main.scss";
</style>
