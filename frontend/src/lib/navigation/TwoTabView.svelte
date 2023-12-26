<script>
  import SegmentRenderer from "$lib/lawRendering/SegmentRenderer.svelte";
  import { christmas } from "$lib/mock/christmas";
  import { textSegmentFromJson } from "$lib/segment";
  import { onMount } from "svelte";
  import Tab from "./Tab.svelte";
  export let segments;

  onMount(() => {
    const resizer = document.getElementById('dragMe');
    const leftSide = resizer.previousElementSibling;
    const rightSide = resizer.nextElementSibling;

      let x = 0;
      let leftWidth = 0;
      let rightWidth = 0;

      const mouseMoveHandler = function (e) {
          // How far the mouse has been moved
          const dx = e.clientX - x;

          const newLeftWidthPx = (leftWidth + dx);
          const newRightWidthPx = (rightWidth - dx);

          if(newLeftWidthPx > 350 && newRightWidthPx > 350) {
              rightSide.style.width = newRightWidthPx + "px";
              leftSide.style.width = newLeftWidthPx + "px";
          }

          leftSide.style.userSelect = 'none';
          leftSide.style.pointerEvents = 'none';

          rightSide.style.userSelect = 'none';
          rightSide.style.pointerEvents = 'none';
      };
      const mouseUpHandler = function () {

          document.body.style.removeProperty('cursor');

          leftSide.style.removeProperty('user-select');
          leftSide.style.removeProperty('pointer-events');

          rightSide.style.removeProperty('user-select');
          rightSide.style.removeProperty('pointer-events');

          // Remove the handlers of `mousemove` and `mouseup`
          document.removeEventListener('mousemove', mouseMoveHandler);
          document.removeEventListener('mouseup', mouseUpHandler);
      };

      const mouseDownHandler = function (e) {
          // Get the current mouse position
          x = e.clientX;
          leftWidth = leftSide.getBoundingClientRect().width;
          rightWidth = rightSide.getBoundingClientRect().width;

          document.addEventListener('mousemove', mouseMoveHandler);
          document.addEventListener('mouseup', mouseUpHandler);
      };

      resizer.addEventListener('mousedown', mouseDownHandler);

  });
</script>

<div class="tabview">
        <Tab>
            <slot name="left" />
        </Tab>

    {#if $$slots.right}
        <div class="resizer" id="dragMe" />
        <Tab>
            <slot name="right" />
        </Tab>
    {/if}


</div>

<style lang="scss">
  .tabview {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    overflow: hidden;
    width: 100%;
    height: 90vh;
  }
  .resizer {
    position: relative;
    width: 4px;
    background: red;
    top: 0;
    bottom: 0;
    min-height: 80vh;
    cursor: col-resize;
  }

</style>
