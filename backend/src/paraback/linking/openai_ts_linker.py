from paraback.linking.textspan_linker import TextspanLinker


class OpenAITSLinker(TextspanLinker):
    calls = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def extract_shortlinks(self):
        OpenAITSLinker.calls += 1
        #print(f"{self.calls} OpenAI call: {self.textspan.text}")
        return []

