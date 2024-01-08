<script>
    export let copied;
    export let hover;
    export let color = "var(--primary)";
    $: if(copied){
        color = "var(--primary)";
    } else {
        color = "#545454";
    }
    export let filter;
    $: if(!hover){
        filter = "grayscale(1) opacity(0.6)";
    } else {
        filter = "grayscale(0);";
    }

</script>

<svg filter="{filter}" width="100%" height="100%" viewBox="0 0 473 473" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;"><g><g><path d="M377.953,126.523c-0,-17.68 -14.355,-32.035 -32.035,-32.035l-313.883,0c-17.681,0 -32.035,14.355 -32.035,32.035l-0,313.883c-0,17.68 14.354,32.035 32.035,32.035l313.883,-0c17.68,-0 32.035,-14.355 32.035,-32.035l-0,-313.883Z" style="fill:{color};"/></g><path d="M409.444,346.469l-0.002,31.484l30.964,-0c17.68,-0 32.035,-14.355 32.035,-32.035l-0,-313.883c-0,-17.681 -14.355,-32.035 -32.035,-32.035l-313.883,0c-17.68,0 -32.035,14.354 -32.035,32.035l0,30.97l31.623,-0l0,-4.103c0,-14.684 11.922,-26.606 26.606,-26.606l260.684,0c14.684,0 26.605,11.922 26.605,26.606l0,260.962c0,14.684 -11.921,26.605 -26.605,26.605l-3.957,0Z" style="fill:#{color};"/></g></svg>


<style lang="scss">
  @import "../styles/main.scss";

</style>
