<script>
    import Arena from "$lib/navigation/Arena.svelte";
    export let data;
</script>

<Arena laws="{['DE-'+data.slug]}" />

<style lang="scss">
  @import "src/lib/styles/main.scss";
</style>

