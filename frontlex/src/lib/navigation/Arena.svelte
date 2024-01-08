<script>

  import Tab from "./Tab.svelte";
  import {randid} from "$lib/utils/nanoid";
  export let laws = [];
  export let tabs = [];

  function closeTab(tabID) {
      tabs = tabs.filter((law) => law !== tabID);
  }

  function newTab(target="No target", afterId=null) {
      console.log("Opening new tab: "+target);
      console.log("current tabs: "+tabs);
      let targetId;
      if(afterId) {
        let index = tabs.indexOf(afterId);
        targetId = randid(8) + "-" + target;
        tabs.splice(index + 1, 0, targetId);
      } else {
          targetId = randid(8) + "-" + target;
          tabs.push(targetId);
      }
      tabs = tabs
  }

  for (let law of laws) {
    newTab(law);
  }

</script>
<svelte:head>
        <style>
            body {
                overflow-y: hidden;
                background-color: #999999;
            }
        </style>
</svelte:head>



<div class="arena-wrapper">
      <div class="arena">
            {#each tabs as tabId (tabId)}
              <Tab tabTarget={tabId} onClose= {() => closeTab(tabId)} onNew={(target) => newTab(target,tabId)} />
            {/each}
      </div>
</div>

<style lang="scss">
  .arena {
    position: absolute;
    height: 99%;
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    overflow-x: hidden;
    overflow-y: hidden;
  }
  .arena-wrapper{
    display:flex;
    width: 100%;
    height: 100vh;
    overflow-x: hidden;
    overflow-y: hidden;
  }

</style>
