from os import listdir, system
from os.path import (
    join as path_join,
    isdir, isfile
)
import json

def debug_print(jsonObject: list | dict) -> None:
    print(json.dumps(jsonObject, indent=2, ensure_ascii=False))

base_path = lambda *path: path_join('.', 'base', *path)

create_base_path = base_path('create_base.json')
fabric_load_condition_path = base_path('fabric_load_condition.json')
forge_load_condition_path = base_path('forge_load_condition.json')
_base_path = base_path('_base.json')

def json_load(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as file:
        return json.load(file)

create_base = json_load(create_base_path)
fabric_load_condition = json_load(fabric_load_condition_path)
forge_load_condition = json_load(forge_load_condition_path)
_base = json_load(_base_path)

create_recipes_list = listdir(base_path('create'))

def dict_sort(dictObject: dict) -> dict:
    sort_keys = [
        "forge:conditions",
        "fabric:load_conditions",
        
        "type",
        "group",
        
        "ingredient",
        "ingredients",
        "pattern",
        "key",
        "transitionalItem",
        "sequence",
        
        "result",
        "results",
        
        "processingTime",
        "acceptMirrored",
        "loops",
        "headRequirement"
    ]
    return dict(sorted(dictObject.items(), key=lambda x: sort_keys.index(x[0])))

while True:
    system('cls')
    print('\n'.join(f'[{index+1}]\t{value[:-5]}' for index, value in enumerate(create_recipes_list)))
    print('> enter 0 to exit')
    
    try:
        id_ = input('\nNumber of Recipe: ')
    except BaseException:
        break
    
    if not id_.isdigit():
        continue
    id_ = int(id_)
    
    if id_ == 0:
        break
    if id_-1 in range(len(create_recipes_list)):
        recipe = json_load(base_path('create', create_recipes_list[id_-1]))
        if recipe['type'] in ('create:mechanical_crafting', 'create:sequenced_assembly'):
            recipe = (fabric_load_condition | forge_load_condition) | recipe
        else:
            recipe = _base | recipe
        
        try:
            mod_id = input('Mod ID: ')
        except BaseException:
            mod_id = ''
        
        if mod_id:
            recipe['forge:conditions'].append({"type": "forge:mod_loaded","mod_id": mod_id})
            recipe['fabric:load_conditions'][0]['values'] = ['create', mod_id]
        
        print('\n\ndata:\n')
        debug_print(dict_sort(recipe))
        print()
    
    input('Press any key to continue...')