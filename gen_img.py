from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import random
#
from categories import power_levels, base_aspects, sub_aspects, animals, adjectives

client = genai.Client()

test_prompt = (
    "Creature description: An eel-like moose-inspired animal with a fire/lava aspect. " +
    "With power level: elite. " +
    "Create character art for the creature in a pokemon-windwaker style." +
    "The background should be a non-distracting fire/lava environment. " +
    "Produce only the image without adornment."
)

class creature_spec:
    def __init__(self, element: str, sub_element: str, animal1: str, animal2: str, adjective: str, evolve_form: str):
        print('dsds')
        print(sub_element)
        self.element = element
        self.sub_element = sub_element
        print(self.sub_element)
        self.animal1 = animal1
        self.animal2 = animal2
        self.adjective = adjective
        self.evolve_form = evolve_form

    def get_prompt(self):
        full_element = self.element
        if self.sub_element != None:
            print(self.sub_element)
            full_element += "/"+self.sub_element
        # creature element string
        element_strength = ""
        if self.evolve_form == "apprentice":
            element_strength = "very slight "
        elif self.evolve_form == "journeyman":
            element_strength = "little bit of a "
        element_str = element_strength + full_element
        # environment description
        environment_type = "natural environment"
        if self.evolve_form == "apprentice":
            environment_type = "natural environment with slight "+full_element+" tones"
        elif self.evolve_form == "journeyman":
            environment_type = "natural environment with "+full_element+" tones"
        elif self.evolve_form == "expert":
            environment_type = "natural environment with a "+full_element+" theme"            
        elif self.evolve_form == "final form":
            environment_type = " a "+full_element+" environment"            
        
        # full prompt
        return (
            "Creature description: A "+self.animal1+"-like "+self.animal2+"-inspired animal with a "+element_str+" aspect.  " +
            "Descriptive adjective: " +self.adjective+".  " +
            "With power level: " +self.evolve_form+".  " +
            "Create character art for the creature in a pokemon-windwaker style.  " +
            "The background should be a non-distracting "+environment_type+".  " +
            "Produce only the image without adornment."
            )

    def get_name(self):
        elem = self.sub_element if self.sub_element != None else self.element
        level = "0"
        if self.evolve_form == "apprentice":
            level = "1"
        elif self.evolve_form == "journeyman":
            level = "2"
        elif self.evolve_form == "expert":
            level = "3"    
        elif self.evolve_form == "final form":
            level = "4"
        return elem+"_"+self.animal1[0:3]+"-"+self.animal2.split()[0]+"_"+level


def generate_base_creature_spec():
    element = random.choice(base_aspects)
    sub_element = None
    if random.random() > 0.5:
        sub_element = random.choice(sub_aspects.get(element))
    print(sub_element)
    animal1 = random.choice(animals)
    animal2 = random.choice(animals)
    adjective = random.choice(adjectives)
    evolve_form = "base"

    return creature_spec(element, sub_element, animal1, animal2, adjective, evolve_form)


def create_image(spec):
    prompt = spec.get_prompt()

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save("images/"+spec.get_name()+".png")



def create_evolution_image_set(spec):
    spec.evolve_form = "apprentice"
    create_image(spec)
    spec.evolve_form = "journeyman"
    create_image(spec)
    spec.evolve_form = "expert"
    create_image(spec)
    spec.evolve_form = "final form"
    create_image(spec)


# main

spec = generate_base_creature_spec()
spec.evolve_form = "expert"
print(spec.get_prompt())
create_evolution_image_set(spec)