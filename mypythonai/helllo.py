import speech_recognition as sr
import pyttsx3
import datetime
import random
import pygame
import threading
import sys

class EmotionalAIFace:
    def __init__(self):
        # 🎤 Speech setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 🔊 Voice setup
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)

        # 😊 Emotion system
        self.mood = "happy"
        self.energy = 50

        # 🎮 Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((450, 550))
        pygame.display.set_caption("Anime AI Assistant")
        self.clock = pygame.time.Clock()
        self.running = True

        # 🖼️ Load anime faces
        self.faces = {
            "happy": pygame.image.load("anime_happy.png"),
            "sad": pygame.image.load("anime_sad.png"),
            "angry": pygame.image.load("anime_angry.png"),
            "surprised": pygame.image.load("anime_surprised.png")
        }

        for key in self.faces:
            self.faces[key] = pygame.transform.scale(self.faces[key], (450, 550))

        print("🤖 Anime AI Ready!")
        self.speak("Hello! I am your anime AI assistant!")

    # 🔊 Speak
    def speak(self, text):
        print("AI:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    # 🎤 Listen
    def listen(self):
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=3)

            query = self.recognizer.recognize_google(audio).lower()
            print("You:", query)
            return query

        except:
            return ""

    # 😊 Mood detection
    def update_mood(self, text):
        if any(word in text for word in ["happy", "good", "love"]):
            self.mood = "happy"
        elif any(word in text for word in ["sad", "bad", "cry"]):
            self.mood = "sad"
        elif any(word in text for word in ["angry", "mad", "hate"]):
            self.mood = "angry"
        elif any(word in text for word in ["wow", "really"]):
            self.mood = "surprised"

    # 🧠 Command processing
    def process_command(self, query):
        self.update_mood(query)

        if "time" in query:
            return datetime.datetime.now().strftime("%I:%M %p")

        if "date" in query:
            return datetime.datetime.now().strftime("%B %d, %Y")

        if "joke" in query:
            return random.choice([
                "Why did the computer get cold? Because it forgot to close windows!",
                "I would tell you a joke about AI… but you might not get it 😄"
            ])

        if "bye" in query:
            self.running = False
            return "Goodbye!"

        return random.choice([
            "That's interesting!",
            "Tell me more!",
            "I like talking to you 😊"
        ])

    # 🎮 Face display
    def animate_face(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Show current emotion face
            face = self.faces.get(self.mood, self.faces["happy"])
            self.screen.blit(face, (0, 0))

            pygame.display.update()
            self.clock.tick(30)

    # 🚀 Run system
    def run(self):
        threading.Thread(target=self.animate_face, daemon=True).start()

        while self.running:
            query = self.listen()
            if not query:
                continue

            response = self.process_command(query)
            self.speak(response)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ai = EmotionalAIFace()
    ai.run()
