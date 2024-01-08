<script>
    export let data;
</script>
<h1>Laws</h1>
<li><a href="/test">test</a></li>
{#each data.laws as law}
    <li><a href="/DE/{law}">{law}</a></li>
{/each}
