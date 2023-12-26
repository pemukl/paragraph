<script lang="ts">
  import ScreenSection from "$lib/navigation/ScreenSection.svelte";
  import SegmentRenderer from "$lib/lawRendering/SegmentRenderer.svelte";
  import {onMount} from "svelte";
  import {browser} from "$app/environment";
  import Spinner from "$lib/navigation/Spinner.svelte";

  let resizer: HTMLDivElement;
  export const active: boolean = true;
  export let content: string = "Tab content";
  export let tabTarget: string;

  // found on https://stackoverflow.com/questions/72579031/how-to-fetch-data-inside-sveltekit-component-that-is-not-a-page
  let tags = tabTarget.split("-");
  export let tabId = tags.shift();
  export let id = tabId;
  tabId += "-DE"
  tags.shift()
  export let filename = tags[0]
  $: lawPromise = (async function getLawById(aircraftID: string) {
    const res = await fetch('/api/?lawID=' + filename);
    return await res.json();
  })(tabTarget)

  let target = tags.join("-");
  target = tabTarget;


  export let width = 600;
  export let newWidth = width;

  onMount(() => {
    const left = resizer.previousElementSibling;
    const right = resizer.nextElementSibling;

    let x = 0;

    const mouseMoveHandler = function (e) {
      // How far the mouse has been moved
      const dx = e.clientX - x;


      if((width + dx) > 350) {
        newWidth = (width + dx);
      }


      left.style.userSelect = 'none';
      left.style.pointerEvents = 'none';
      if(right){
        right.style.userSelect = 'none';
        right.style.pointerEvents = 'none';
      }
    };
    const mouseUpHandler = function () {
      width = newWidth;
      document.body.style.removeProperty('cursor');

      left.style.removeProperty('user-select');
      left.style.removeProperty('pointer-events');
      if(right){
        right.style.removeProperty('user-select');
        right.style.removeProperty('pointer-events');
      }


      // Remove the handlers of `mousemove` and `mouseup`
      document.removeEventListener('mousemove', mouseMoveHandler);
      document.removeEventListener('mouseup', mouseUpHandler);

    };

    const mouseDownHandler = function (e) {
      // Get the current mouse position
      x = e.clientX;

      document.addEventListener('mousemove', mouseMoveHandler);
      document.addEventListener('mouseup', mouseUpHandler);
    };

    resizer.addEventListener('mousedown', mouseDownHandler);

  });

  function scrollToTargetAdjusted(tabElement,element){

    const offsetx = 90;
    const bodyRectx = document.body.getBoundingClientRect().left;
    const elementRectx = tabElement.getBoundingClientRect().left;
    const elementPositionx = elementRectx - bodyRectx;
    const offsetPositionx = elementPositionx - offsetx;
    window.scrollTo({
      left: offsetPositionx,
      behavior: 'smooth'
    });

    const offset = 90;
    const bodyRect = document.body.getBoundingClientRect().top;
    const elementRect = element.getBoundingClientRect().top;
    const elementPosition = elementRect - bodyRect;
    const offsetPosition = elementPosition - offset;
    tabElement.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });

  }

  function scroll(node) {
    const { hash } = document.location;
    //const code = hash.slice(1)
    const code = target;
    const scrollTo = ('#'+code) && document.getElementById(code);
    const tabElement = ('#'+id) && document.getElementById(id);
    if (scrollTo){
      //scrollTo.scrollIntoView({ behavior: 'smooth', block: 'center' });
      scrollToTargetAdjusted(tabElement, scrollTo);
    }
    return {
      destroy() {
        console.log("destroying Tab: "+id);
      }
    };
  }

  export let onClose;
  export let onNew;

</script>

<div class="tab" id={id} style="width: {newWidth}px">

    {#await lawPromise }
        <Spinner/>
    {:then lawData}
      <div class="header" id="myHeader">
        <h2 class="title">{lawData.title} ({tags[0]})</h2>
        <button class="but" on:click={onClose}>X</button>
      </div>
      <ScreenSection >

      <div use:scroll>  </div>
      <SegmentRenderer segments={lawData} id={tabId} onNew={onNew}/>
      </ScreenSection>
    {:catch error}
      <p style="color: red">{error.message +" ("+ filename+")"}</p>
    {/await}

</div>

<div class="resizer" bind:this={resizer}></div>

<style lang="scss">
  @import "../styles/_variables.scss";
  .tab {
    height: 100%;
    flex-grow: 1;
    overflow-y: auto;
    overflow-x: hidden;
    border-radius: $border-radius;

    .header {
      position: sticky;
      width: auto;
      height: 2rem;
      border-radius: $border-radius;
      text-align: center;
      background-color: var(--primary);
      top: 0;
      z-index:1000;
      .title{
        text-align: center;
        color: white;
        font-size: 1rem;
        height: 2rem;
        line-height: 2rem;
        margin: 0;
        font-weight: 600;
        font-family: "Mulish", serif;
        padding: 0;
      }
      .but{
        position: absolute;
        right: 0;
        top: 0;
        height: 2rem;
        width: 2rem;
        background-color: var(--primary);
        border: none;
        color: white;
        font-size: 1rem;
        border-radius: 0 0 $border-radius 0;
        &:hover{
          background-color: var(--off-black);
        }

      }
    }
  }
  .resizer {
    position: relative;
    width: 4px;
    background: black;
    top: 0;
    bottom: 0;
    min-height: 80vh;
    cursor: col-resize;
  }

</style>
