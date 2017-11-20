import json

def readJson(filename):
    with open(filename, 'r') as f:
         config= json.load(f)
    return config

def is_quant(token):
    if u"CD" == token.pos:
        return True
    else:
        return False

def get_quantities(parse_obj):
    quant_tokens_list = []
    for i in range(len(parse_obj.sentences)):
        for j in range(len(parse_obj.sentences[i].tokens)):
            if is_quant(parse_obj.sentences[i].tokens[j]):
                quant_tokens_list.append(parse_obj.sentences[i].tokens[j])
    return quant_tokens_list

    
