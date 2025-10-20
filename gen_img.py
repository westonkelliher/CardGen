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
        self.element = element
        self.sub_element = sub_element
        self.animal1 = animal1
        self.animal2 = animal2
        self.adjective = adjective
        self.evolve_form = evolve_form
        self.general_description = None
        self.evo1_description = None
        self.evo2_description = None
        self.evo3_description = None

    def draw_me_prompt(self):
        full_element = self.element
        if self.sub_element != None:
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
        power_addon = ""
        if self.evolve_form == "apprentice":
            power_addon = "(this is a weak creature with a very simple design)"
            environment_type = "natural environment with a "+full_element+" theme"
        elif self.evolve_form == "journeyman":
            power_addon = "(this is a fairly simple creature)"
            environment_type = "natural environment with a "+full_element+" theme"
        elif self.evolve_form == "expert":
            power_addon = "(this is a decently strong creature)"
            environment_type = " a "+full_element+" environment"                     
        elif self.evolve_form == "final form":
            # power_addon = "(this is a powerful creature)"
            environment_type = " a "+full_element+" environment"            
        
        # full prompt
        return (
            "Creature description: A creature with the body of a "+self.animal1+", but with a head that's inspired by a "+self.animal2+".  " +
            "Descriptive adjective: " +self.adjective+".  " +
            "With power level: " +self.evolve_form+" "+power_addon+".  " +
            "Create character art for the creature in a pokemon-windwaker style.  " +
            "The background should be a non-distracting "+environment_type+".  " +
            "Produce only the image without adornment."
            )
    
    def describe_me_prompt(self):
        full_element = self.element
        if self.sub_element != None:
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
        power_addon = ""
        if self.evolve_form == "apprentice":
            power_addon = "(this is a weak creature with a very simple design)"
            environment_type = "natural environment with a "+full_element+" theme"
        elif self.evolve_form == "journeyman":
            power_addon = "(this is a fairly simple creature)"
            environment_type = "natural environment with a "+full_element+" theme"
        elif self.evolve_form == "expert":
            power_addon = "(this is a decently strong creature)"
            environment_type = " a "+full_element+" environment"                     
        elif self.evolve_form == "final form":
            # power_addon = "(this is a powerful creature)"
            environment_type = " a "+full_element+" environment"            
        
        # full prompt
        return (
            "Your task is to describe the physical characteristics of a creature and its three evolutions. The creature's inspirations are:\n"
            "General body inspired by: "+self.animal1+".\n" +
            "Characterizing features inspired by: "+self.animal2+".\n" +
            "Descriptive adjective (can be used for patterns or features or vibe or just discarded): " +self.adjective+".\n" +
            "Elemental type of the creature: "+full_element+".\n" +
            "Describe the shape of the creature / parts of the creatures body. Describe its physically defining characteristic(s). Define the surface features of its body.\n" +
            "You will do this three times, producing three different descriptions that are very similar to each other. "+
            "The first description should be of the pre-evolved, weak form of the creature. This should be a slightly more mundane description. "+
            "The second description should be of the creature after its first evolution. This should be a medium power creature with more prominent defining features. "+
            "The third description should be final form of the creature. This should be a powerful creature with very prominent defining features. "+
            "All threee forms should be roughly similar size.\n"+
            "Each description should be two sentences long and they should be separated by two newlines."
            "Avoid any embelishment and avoid any adjectives that are unrelated to the creature's physical appearance.\n" +
            "Output only the descriptions and nothing else."
            )

    def build_general_description(self):
        describe_prompt = self.describe_me_prompt()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=describe_prompt
        )
        self.general_description = response.text
        

    def build_evo_descriptions(self):
        if self.general_description is None:
            self.build_general_description()
        general = self.general_description
        pre_evo_prompt0 = (
            "Your task is to modify the description of a creature. " +
            "Given that the creature's orignal description is: "+general+"\n" +
            "We need to modify the description to describe the pre-evolved form of this creature. It should be weaker and simpler with more generic features but overall very similar to the original description.\n" +
            "Output only the modified description and nothing else."
        )
        post_evo_prompt0 = (
            "Your task is to describe a the physical characteristics of an preevolved creature in two sentences. " +
            "Given that the creature's general description is: "+general+"\n" +
            "What would the evolved form of this creature look like? It should be stronger with more pronounced features but overall very similar to the general description.\n" +
            "Describe the shape of the creature / parts of the creatures body. Describe its physical defining characteristic(s). Define the surface features of its body.\n" +
            "Avoid any embelishment and avoid any adjectives that are unrelated to the creature's physical appearance.\n" +
            "Output only the description and nothing else."
        )
        pre_evo_prompt = (
            "Your task is to modify a creature description slightly to make it more weak and mundane.\n"+
            "For example the following description:\n"+
            '"This creature possesses a slender, bird-like body with broad, dark wings and a heavy, ursine head. Its dense, shadowed fur is interspersed with a mottling of ash-grey, giving its ancient form a texture like weathered stone."\n'+
            "Would be modified to:\n"+
            '"This creature possesses a somewhat slender, bird-like body with broad, dark wings and a vaguely ursine head. Its dark fur is interspersed with a mottling of ash-grey, giving its form a somewhat stony texture."\n'+
            "Now that you have an example please update the following description:\n"+
            general+"\n"+
            "Output only the modified description and nothing else."
        )
        post_evo_prompt = (
            "Your task is to modify a creature description slightly to make it stronger, more elemental, and more exagerated.\n"+
            "For example the following description:\n"+
            '"This creature possesses a slender, bird-like body with broad, dark wings and a heavy, ursine head. Its dense, shadowed fur is interspersed with a mottling of ash-grey, giving its ancient form a texture like weathered stone."\n'+
            "Would be modified to:\n"+
            '"This creature possesses a very slender, bird-like body with broad, shadow-wrought wings and a heavy, ursine head. Its body is covered in ash-ridden, petrified fur giving its ancient form a texture like weathered stone."\n'+
            "Now that you have an example please update the following description:\n"+
            general+"\n"+
            "Do not go overboard with adjecetives. Output only the modified description and nothing else."
        )
        pre_evo_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pre_evo_prompt
        )
        post_evo_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=post_evo_prompt
        )
        self.evo1_description = pre_evo_response.text
        self.evo2_description = general
        self.evo3_description = post_evo_response.text


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
spec.build_general_description()
print(spec.general_description)
# spec.build_evo_descriptions()
# print(spec.evo1_description+"\n\n")
# print(spec.evo2_description+"\n\n")
# print(spec.evo3_description+"\n\n")
# print(spec.get_general_description())
# print(spec.get_general_description())
# spec.evolve_form = "expert"
# print(spec.get_prompt())
# create_evolution_image_set(spec)