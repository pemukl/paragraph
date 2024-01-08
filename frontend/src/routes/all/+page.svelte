<script>
    import Tab from "$lib/navigation/Tab.svelte";
    import Arena from "$lib/navigation/Arena.svelte";
    let laws = ["KryptoFAV","eWpG","eWpRV"]
    let width = laws.length * 50 + "vw"
    export let data;
    console.log(data)

</script>

<Arena laws="{data.laws}" />
