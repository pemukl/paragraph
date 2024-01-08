<script lang="ts">
  import Enumeration from "./Enumeration.svelte";
  import Section from "./Section.svelte";
  import Sentence from "./Sentence.svelte";
  import Paragraph from "./Paragraph.svelte";
  import Law from "./Law.svelte";
  import {TextSegmentType, TextSegment, textSegmentFromJson} from "$lib/segment";

  import TextSpan from "$lib/lawRendering/TextSpan.svelte";
  import Area from "$lib/lawRendering/Area.svelte";
  import Litera from "$lib/lawRendering/Litera.svelte";
  import SubLitera from "$lib/lawRendering/SubLitera.svelte";
  import Reference from "$lib/lawRendering/Reference.svelte";
  export let segments: TextSegment | TextSegment[] | string;
  export let selected = false;
  export let id;
  export let onNew;
</script>


{#if segments.constructor === Object}
  <svelte:self segments={textSegmentFromJson(segments)} {selected} id={id} onNew={onNew}/>
{:else if segments.constructor === TextSegment}
  {#if segments.type === TextSegmentType.Law }
    <Law segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Area}
    <Area segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Paragraph}
    <Paragraph segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Section}
    <Section segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Sentence}
    <Sentence segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Enumeration}
    <Enumeration segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Litera}
    <Litera segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.SubLitera}
    <SubLitera segment={segments} {selected} id={id} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.TextSpan}
    <TextSpan segment={segments} {selected} onNew={onNew}/>
  {:else if segments.type === TextSegmentType.Reference}
    <Reference reference= {segments} {selected} onNew={onNew}/>
  {:else}
    <p style="color: red">#: cannot render segment type {segments.type}</p>
  {/if}

{:else if Array.isArray(segments)}
  {#each segments as segment}
    <svelte:self segments={segment} {selected} id={id} onNew={onNew}/>
  {/each}
{/if}
