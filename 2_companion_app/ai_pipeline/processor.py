class AIPipeline:
    def process(self, frame):
        # Pre-process frame for Gemini inference
        return frame.resize((640, 480)).grayscale()
