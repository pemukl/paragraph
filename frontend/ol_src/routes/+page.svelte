<script>
    export let data;
</script>
<h1>Laws</h1>
{#each data.laws as law}
    <li><a href="/DE/{law}">{law}</a></li>
{/each}
