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
            "Create character art for the creature in a 2d pokemon/rick-and-morty style. " +
            "The character art should be the three different creatures representing the three pokemon evolutions. " +
            "The first creature should be in the top left: the weak adolescent form. " +
            "The second creature should be in the top right: the basic adult form. " +
            "The third creature should be in the bottom middle: the epic final form. " +
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
            "The base description should be one to two sentences long. Then add one brief sentence to describe the additional feature or change for the 'final form' of the creature which should exagerate an existing theme (actually use the term 'final form' in this sentence). Avoid embellishments and and adjectives unrelated to the physical characteristics of the body. \n" +
            "Output only the description and nothing else."
            )


    def build_description(self):
        describe_prompt = self.describe_me_prompt()
        response = client.models.generate_content(
            model=gemini_language_model,
            contents=describe_prompt
        )
        self.general_description = response.text
        


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

spec.animal2 = random.choice(["castle", "barn", "hillock", "mimic", "bell", "lantern", "sword", "shield", "armor", "skeleton", "zombie"])
#spec.special_feature = "an extravagant bone mask that grows in the final form"

spec.print_me()

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
