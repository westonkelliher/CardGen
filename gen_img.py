from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import random
import os # Nick added 10/26 - env variable access 
#
from categories import power_levels, base_aspects, sub_aspects, animals, adjectives
from build_phrases import insp_phrase

# Nick added 10/26 - API key from env variable
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

gemini_language_model = "gemini-2.5-flash"  # Changed to lite

test_prompt = (
    "Creature description: An eel-like moose-inspired animal with a fire/lava aspect. " +
    "With power level: elite. " +
    "Create character art for the creature in a pokemon-windwaker style." +
    "The background should be a non-distracting fire/lava environment. " +
    "Produce only the image without adornment."
)

class creature_spec:
    def __init__(self, element: str, sub_element: str, animal1: str, animal2: str, special_feature: str, evolve_form: str):
        self.element = element
        self.sub_element = sub_element
        self.animal1 = animal1
        self.animal2 = animal2
        self.special_feature = special_feature
        self.evolve_form = evolve_form
        self.general_description = None
        self.evo1_description = None
        self.evo2_description = None
        self.evo3_description = None
        self.evo1_stats = None # Nick added 10/26
        self.evo2_stats = None # Nick added 10/26 
        self.evo3_stats = None # Nick added 10/26

    def print_me(self):
        print("---")
        print(self.element + " " + str(self.sub_element))
        print(self.animal1 + " " + self.animal2)
        print(self.special_feature)
        print("---")
        
        
    def draw_me_prompt(self, evo=0):
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
        but_version = ""
        if self.evolve_form == "apprentice":
            power_addon = "(this is an adolescent version of the creature described)"
            but_version = "but make it an adolescent and more mundane than the original description"
            environment_type = "natural environment with a "+full_element+" theme"
        elif self.evolve_form == "journeyman":
            power_addon = "(this is a medium strength version of the creature described)"
            but_version = ""
            environment_type = "natural environment with a "+full_element+" theme"
        elif self.evolve_form == "expert":
            power_addon = "(this is a powerful form of the creature described)"
            but_version = "but make it more evolved, exagerated, and powerful than the original description"
            environment_type = " a "+full_element+" environment"                     
        elif self.evolve_form == "final form":
            # power_addon = "(this is a powerful creature)"
            environment_type = " a "+full_element+" environment"         
        ####    
        description = self.general_description
        if evo == 1:
            description = self.evo1_description
        elif evo == 2:
            description = self.evo2_description
        elif evo == 3:
            description = self.evo3_description
        # full prompt
        return (
            "Creature description: "+description+".  " +
            "With power level: " +self.evolve_form+" "+power_addon+".  " +
            "Create character art for the creature in a pokemon-windwaker style with a simple design ("+but_version+").  " +
            "The background should be a non-distracting "+environment_type+".  " +
            "Produce only the image without adornment."
            )

    

    def draw_three_prompt(self):
        full_element = self.element
        if self.sub_element != None:
            full_element += "/"+self.sub_element
        # environment description
        environment_type = "natural environment"
        description = self.general_description
        # full prompt
        return (
            "Creature description: "+description+".  \n" +
            #"Creature description: \n"+#description+".  " +
            #"General body inspired by: "+self.animal1+".\n" +
            #"Characterizing features inspired by: "+self.animal2+".\n" +
            #"special feature: " +self.special_feature+".\n" +
            #"Elemental type of the creature: "+full_element+".\n" +
            #" --- \n" + 
            "Create character art for the creature in a pokemon-windwaker style. " +
            "The character art should be the three different creatures representing the three pokemon evolutions. " +
            "The first creature should be in the top left and face slightly left: a weak adolescent. " +
            "The second creature should be in the top right and face slightly right: an evolved juvenile. " +
            "The third creature should be in the bottom middle and face forward: an epic final evolution with exagerated features. " +
            #"The top left evolution should be a weaker adolescent. The bottom right evolution should be medium strength. The bottom evolution should be powerful with exagerated features and more complexity." +
            "Each of the three should be visually distinct. NEVER repeat the same creature. " +
            "Keep the color pallete consistent. " + 
            "The background should be transparent. " +
            "Draw only the creatures without text or adornment."
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
        description = self.general_description
        # full prompt
        return (
            "Your task is to describe the physical characteristics of a creature. The creature's inspirations are:\n"
            "General body inspired by: "+self.animal1+".\n" +
            "Characterizing features inspired by: "+self.animal2+".\n" +
            "special feature: " +self.special_feature+".\n" +
            "Elemental type of the creature: "+full_element+".\n" +
            "Describe the shape of the creature / parts of the creatures body. Describe its physically defining characteristic(s). Define the surface texture/features of its body.\n" +
            "The description should be two sentences long. Avoid embellishments and and adjectives unrelated to the physical characteristics of the body."
            "Output only the description and nothing else."
            )

    def describe_evos_prompt(self):
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
            "The second description should be of the creature after its first evolution. This should be a medium power version of the creature with its defining features now more prominent. "+
            "The third description should be final form of the creature. This should be a powerful version of the creature. "+
            "Each description should be completely independent (one description should never reference the others or mention evolving or evolutions). All three forms should be roughly similar size. "+
            "Make sure the three descriptions describe roughly the same creature just at different power levels.\n"+
            "Each description should be two sentences long and they should be separated by two newlines."
            "Output only the descriptions and nothing else."
            )


    def build_description(self):
        describe_prompt = self.describe_me_prompt()
        response = client.models.generate_content(
            model=gemini_language_model,
            contents=describe_prompt
        )
        self.general_description = response.text
        


    def build_evo_descriptions(self):
        describe_prompt = self.describe_evos_prompt()
        response = client.models.generate_content(
            model=gemini_language_model,
            contents=describe_prompt
        )
        self.general_description = response.text

        parts = response.text.split("\n\n")   

        self.evo1_description = parts[0].strip()
        self.evo2_description = parts[1].strip()
        self.evo3_description = parts[2].strip()


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
    #adjective = random.choice(adjectives)
    special_feature = insp_phrase()
    evolve_form = "base"

    spec =  creature_spec(element, sub_element, animal1, animal2, special_feature, evolve_form)
    spec.print_me()
    return spec


def create_image(spec, evo=0):
    prompt = spec.draw_me_prompt(evo)
    print(prompt+"\n=============\n")

    # Nick Added 10/26 TESTING FUNCTIONALITY
    creature_stats(spec, prompt) # TESTING TESTING TESTING ################################################


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

            
def create_triple_image(spec):
    spec.build_description()
    prompt = spec.draw_three_prompt()
    print(prompt+"\n=============\n")
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
    


def create_evolution_image_set(spec): # not used?
    spec.build_evo_descriptions()
    spec.evolve_form = "apprentice"
    create_image(spec, 1)
    #
    spec.evolve_form = "journeyman"
    create_image(spec, 2)
    #
    spec.evolve_form = "expert"
    create_image(spec, 3)
    #
    # spec.evolve_form = "final form"
    # create_image(spec)


def create_image_set(spec): 
    spec.build_description()
    print(spec.general_description)
    spec.evolve_form = "apprentice"
    create_image(spec)
    #
    spec.evolve_form = "journeyman"
    create_image(spec)
    #
    spec.evolve_form = "expert"
    create_image(spec)


#Nick added 10/26
def creature_stats(spec, prompt):

#todos:
    # RANDOM STAT
    # Create categories list of possible ability types to plug into prompt (damage,buff,debuff,summon,heal,control, etc)
    # random chance of having a trample, first strike, etc
    # progress stats with evolutions (keeping track of previous stats to build on)

    stat_prompt_test = (
        "From the given creature description below, create two abilities that fit the creature's theme and attributes, where each ability has a set mana cost (0-10). " +
        "The stronger the ability, the higher the mana cost." +
        "Set the creature's Health from (1-10), Mana Cost to activate (0-10), and Attack (1-10). " +
        "There is a chance the creature has a passive ability, if so include it, only if it makes logical sense. Possible passive abilities include: \n" +
        "Trample (extra damage leftover from an attack carries to next opponent), First Strike (attack first in combat), Regenerate (heals a small amount each turn), " +
        ",Swift (can attack twice in one turn), Flying (can only be attacked if another creature has flying)." +
        prompt #incorporate evo description into prompt
    )

    response = client.models.generate_content(
            model=gemini_language_model,
            contents=[stat_prompt_test]
        )
    
    response_text = None
     # Try direct text field first
    if getattr(response, "text", None):
        response_text = response.text

    # Otherwise, extract from content parts
    elif hasattr(response, "candidates") and response.candidates:
        parts = getattr(response.candidates[0].content, "parts", [])
        if parts:
            response_text = "".join([
                getattr(p, "text", "") or "" for p in parts
            ]).strip()
    


    # Populate evo stats
    if spec.evolve_form == "apprentice":
        spec.evo1_stats = response_text
        print("\nCreature Stats and Abilities:\n"+spec.evo1_stats+"\n=============\n")
    elif spec.evolve_form == "journeyman":
        spec.evo2_stats = response_text
        print("\nCreature Stats and Abilities:\n"+spec.evo2_stats+"\n=============\n")  
    elif spec.evolve_form == "expert":
        spec.evo3_stats = response_text
        print("\nCreature Stats and Abilities:\n"+spec.evo3_stats+"\n=============\n")





# main

spec = generate_base_creature_spec()
create_triple_image(spec)

# spec.build_evo_descriptions()
# print(spec.evo1_description + "\n---\n")
# print(spec.evo2_description + "\n---\n")
# print(spec.evo3_description + "\n---\n")
# spec.build_evo_descriptions()
# print(spec.evo1_description+"\n\n")
# print(spec.evo2_description+"\n\n")
# print(spec.evo3_description+"\n\n")
# print(spec.get_general_description())
# print(spec.get_general_description())
# spec.evolve_form = "expert"
# print(spec.get_prompt())
# create_evolution_image_set(spec)
