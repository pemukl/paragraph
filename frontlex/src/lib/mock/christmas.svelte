<script>
	import Enumeration from '$lib/lawRendering/Enumeration.svelte';
	import Section from '$lib/lawRendering/Section.svelte';
	import Paragraph from '$lib/lawRendering/Paragraph.svelte';
	import Sentence from '$lib/lawRendering/Sentence.svelte';
	import ScreenSection from '$lib/navigation/ScreenSection.svelte';
</script>

<ScreenSection>
	<h4 class="serif center">
		Gesetz über die Verkündung von Gesetzen und Rechtsverordnungen und über Bekanntmachungen
		(Verkündungs- und Bekanntmachungsgesetz – VkBkmG)
	</h4>

	<h5 class="serif center">
		Abschnitt 1<br />
		Allgemeine Vorschriften
	</h5>

	<Paragraph title="§ 1 Verkündungs- und Bekanntmachungsorgane des Bundes">
		<Section ordinal="(1)">
			<Sentence ordinal="1">
				Das Bundesgesetzblatt ist das Verkündungsorgan des Bundes für Gesetze und
				Rechtsverordnungen.
			</Sentence>
			<Sentence ordinal="2">
				Das Bundesgesetzblatt ist außerdem das Bekanntmachungsorgan des Bundes, wenn durch
				Rechtsvorschrift die amtliche Bekanntmachung im Bundesgesetzblatt vorgeschrieben ist.
			</Sentence>
		</Section>
		<Section ordinal="(2)">
			<Sentence ordinal="1">Der Bundesanzeiger ist ein Bekanntmachungsorgan des Bundes.</Sentence>
			<Sentence ordinal="2">Er hat einen amtlichen Teil.</Sentence>
			<Sentence ordinal="3">
				Dieser ist bestimmt für
				<Enumeration --order={1} ordinal="1.">
					andere als die in <span class="ref">Absatz 1 Satz 2</span> genannten amtlichen Bekanntmachungen
					der Behörden des Bundes, einschließlich Ausschreibungen und Hinweise, und
				</Enumeration>
				<Enumeration --order={1} ordinal="2.">
					amtliche Bekanntmachungen der Behörden der Länder, sofern die Bekanntmachung im amtlichen
					Teil des <span class="def">Bundesanzeigers</span> durch Bundesgesetz oder Rechtsverordnung
					des Bundes vorgeschrieben ist.
				</Enumeration>
			</Sentence>
			<Sentence ordinal="4">
				Der <span class="def">Bundesanzeiger</span> kann weitere Teile für andere Bekanntmachungen enthalten.
			</Sentence>
		</Section>
		<Section ordinal="(3)">
			Das <span class="def">Bundesgesetzblatt</span> und der <span class="def">Bundesanzeiger</span>
			werden vom Bundesministerium der Justiz herausgegeben.
		</Section>
	</Paragraph>
	<Paragraph title="§ 2 Ausgabe und dauerhafte Bereithaltung im Internet">
		<Section ordinal="(1)">
			<Sentence ordinal="1">
				Das <span class="def">Bundesgesetzblatt</span> wird vom Bundesamt für Justiz auf der
				Internetseite <a href="https://www.recht.bund.de" target="_blank">www.recht.bund.de</a>
				ausgegeben.
			</Sentence>
			<Sentence ordinal="2">Es wird dort vollständig und dauerhaft bereitgehalten.</Sentence>
		</Section>
		<Section ordinal="(2)">
			<Sentence ordinal="1">
				Der <span class="def">Bundesanzeiger</span> wird vom Betreiber des
				<span class="def">Bundesanzeigers</span>
				auf der Internetseite
				<a href="https://www.bundesanzeiger.de" target="_blank">www.bundesanzeiger.de</a> ausgegeben.
			</Sentence>
			<Sentence ordinal="2">Er wird dort vollständig und dauerhaft bereitgehalten.</Sentence>
		</Section>
	</Paragraph>
	<Paragraph title="§ 3 Verkündung und amtliche Bekanntmachung">
		<Section ordinal="(1)">
			<Sentence ordinal="1">
				Die Verkündung von Gesetzen und Rechtsverordnungen erfolgt jeweils durch die Ausgabe einer
				Nummer des <span class="def">Bundesgesetzblatts</span>.
			</Sentence>
			<Sentence ordinal="2">
				Amtliche Bekanntmachungen im <span class="def">Bundesgesetzblatt</span> erfolgen jeweils
				durch die Ausgabe einer Nummer des <span class="def">Bundesgesetzblatts</span>.
			</Sentence>
			<Sentence ordinal="3">
				Jede Nummer des <span class="def">Bundesgesetzblatts</span> trägt das Datum ihrer Ausgabe.
			</Sentence>
		</Section>
		<Section ordinal="(2)">
			<Sentence ordinal="1">
				Die amtlichen Bekanntmachungen im <span class="def">Bundesanzeiger</span> erfolgen jeweils
				durch Ausgabe einer Nummer des amtlichen Teils des
				<span class="def">Bundesanzeigers</span>.</Sentence
			>
			<Sentence ordinal="2"><span class="ref">Absatz 1 Satz 3</span> gilt entsprechend.</Sentence>
		</Section>
	</Paragraph>
	<Paragraph title="§ 4 Freier Zugang">
		<Section ordinal="(1)">
			<Sentence ordinal="1"
				>Das <span class="def">Bundesgesetzblatt</span> ist jederzeit frei zugänglich.</Sentence
			>
			<Sentence ordinal="2">
				Es kann unentgeltlich gelesen, ausgedruckt, gespeichert und verwertet werden.
			</Sentence>
		</Section>
		<Section ordinal="(2)">
			<Sentence ordinal="1">
				Der amtliche Teil des <span class="def">Bundesanzeigers</span> ist jederzeit frei zugänglich.
			</Sentence>
			<Sentence ordinal="2">
				Er kann unentgeltlich gelesen, ausgedruckt und gespeichert werden.
			</Sentence>
		</Section>
	</Paragraph>
	<Paragraph title="§ 5 Benachrichtigungsdienste">
		<Sentence ordinal="1">
			Für das <span class="def">Bundesgesetzblatt</span> ist ein unentgeltlicher elektronischer Benachrichtigungsdienst
			bereitzustellen, der über jede Ausgabe einer neuen Nummer und deren Inhalt informiert.
		</Sentence>

		<Sentence ordinal="2"
			>Gleiches gilt für den amtlichen Teil des <span class="def">Bundesanzeigers</span>.</Sentence
		>
	</Paragraph>
	<Paragraph title="§ 6 Änderungsverbot; Löschung personenbezogener Daten; Berichtigungen">
		<Section ordinal="(1)">
			Änderungen des <span class="def">Bundesgesetzblatts</span> und des amtlichen Teils des
			<span class="def">Bundesanzeigers</span>
			sind vorbehaltlich des <span class="ref">Absatzes 2</span> unzulässig.
		</Section>
		<Section ordinal="(2)">
			Müssen personenbezogene Daten aus Gründen ihres Schutzes gelöscht werden, so werden in der
			betreffenden Nummer des <span class="def">Bundesgesetzblatts</span> oder des amtlichen Teils
			des <span class="def">Bundesanzeigers</span>
			diese Daten unkenntlich gemacht und wird ein Hinweis auf Datum und Grund der Löschung angebracht.
		</Section>

		<Section ordinal="(3)">
			<Sentence ordinal="1">
				Die Berichtigung von offenbaren Unrichtigkeiten im <span class="def">Bundesgesetzblatt</span
				> ist dort bekannt zu machen.
			</Sentence>
			<Sentence ordinal="2"
				><span class="ref">Satz 1</span> gilt für den <span class="def">Bundesanzeiger</span> entsprechend.</Sentence
			>
		</Section>
	</Paragraph>
	<Paragraph title="§ 7 Sicherung der Echtheit und Unverfälschtheit">
		<Section ordinal="(1)">
			Jede Nummer des <span class="def">Bundesgesetzblatts</span>, die nach
			<span class="ref">§ 3 Absatz 1</span>
			oder nach <span class="ref">§ 8 Absatz 1</span> ausgegeben wird, und jede Nummer des amtlichen
			Teils des <span class="def">Bundesanzeigers</span> trägt ein qualifiziertes elektronisches
			Siegel nach <span class="eu">Artikel 3 Nummer 27 der Verordnung (EU) Nr. 910/2014</span> des
			Europäischen Parlaments und des Rates vom 23. Juli 2014 über elektronische Identifizierung und
			Vertrauensdienste für elektronische Transaktionen im Binnenmarkt und zur Aufhebung der
			<span class="eu">Richtlinie 1999/93/EG</span> (<span class="abl"
				>ABl. L 257 vom 28.8.2014, S. 73</span
			>; <span class="abl">L 23 vom 29.1.2015, S. 19</span>;
			<span class="abl">L 155 vom 14.6.2016, S. 44</span>).
		</Section>
		<Section ordinal="(2)">
			<Sentence ordinal="1">
				Wird die Urschrift eines Gesetzes elektronisch zur Gegenzeichnung und Ausfertigung
				vorgelegt, so erfolgen diese jeweils durch qualifizierte elektronische Signatur nach
				<span class="eu">Artikel 3 Nummer 12 der Verordnung (EU) Nr. 910/2014</span>.
			</Sentence>
			<Sentence ordinal="2">
				Gleiches gilt auch für die Ausfertigung von Rechtsverordnungen und amtlichen
				Bekanntmachungen.
			</Sentence>
		</Section>
	</Paragraph>
</ScreenSection>
