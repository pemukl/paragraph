<script>
  import Main from "$lib/Main.svelte";
</script>

<Main>
  <slot />
</Main>

<style lang="scss">
    @import "src/lib/styles/main.scss";
  nav {
    margin-bottom: 12rem;
  }
</style>
