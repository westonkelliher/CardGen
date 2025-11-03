import random
from categories import base_aspects, sub_aspects, animals
from categories import insp_templates, adjectives, pieces, multitudes, body_parts




def insp_phrase():
    # uses adjectives, pieces, multitudes
    template = random.choice(insp_templates)
    template = template.replace("<pieces>", random.choice(pieces))
    template = template.replace("<body-part>", random.choice(body_parts), 1)
    template = template.replace("<body-part>", random.choice(body_parts), 1)    
    template = template.replace("<multitudes>", random.choice(multitudes))
    template = template.replace("<adjectives>", random.choice(adjectives))
    return template




if __name__ == "__main__":
    for i in range(10):
        print(insp_phrase())
