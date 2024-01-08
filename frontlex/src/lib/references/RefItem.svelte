<script>
    export let action;
    export let text;
    let over;

</script>

<div class="item" on:mouseenter={() => {over=true}} on:mouseleave={() => over=false}>
    <div class="inner" on:click={action()} on:keyup={action()}>
        <slot hover={over}/>
        <div class="extension"> {text} </div>
    </div>
</div>


<style lang="scss">


    .item {
      height: 31px;
      width: 31px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 2px;
      position: relative;


      .inner {

        display: flex;
        align-items: center;
        justify-content: center;
        height: 20px;
        width: 20px;
        &:hover *{
          font-weight:600;
        }

      }



      .extension {
        position: absolute;
        right: 0;
        left: 33px;
        width: fit-content;
        white-space: nowrap;
        height: 35px;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
        background-color: var(--background);
        z-index: 1;
        box-shadow: 10px 10px 10px rgba(0, 0, 0, 0.2);
        flex-direction: row;
        justify-content: center;
        align-items: center;
        padding-left: 7px;
        padding-right: 10px;
        color: black;
        display: flex;
      }

    }
</style>