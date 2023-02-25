from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# Define some global variables to store the player's character and inventory
character = {
    'name': 'Player',
    'class': 'Warrior',
    'level': 1,
    'experience': 0,
    'health': 10,
    'max_health': 10,
    'attack': 2,
    'defense': 1,
    'gold': 0
}

inventory = {
    'weapons': [],
    'armor': [],
    'items': []
}

# Define some sample enemies and quests
enemies = [
    {
        'name': 'Goblin',
        'health': 5,
        'attack': 1,
        'defense': 0,
        'gold': 2,
        'experience': 5
    },
    {
        'name': 'Orc',
        'health': 10,
        'attack': 2,
        'defense': 1,
        'gold': 5,
        'experience': 10
    },
    {
        'name': 'Dragon',
        'health': 20,
        'attack': 5,
        'defense': 3,
        'gold': 20,
        'experience': 50
    }
]

quests = [
    {
        'name': 'Defeat the Goblin',
        'description': 'Find and defeat the goblin in the forest',
        'requirements': {'level': 2},
        'rewards': {'gold': 5, 'experience': 10},
        'completed': False
    },
    {
        'name': 'Defeat the Orc',
        'description': 'Find and defeat the orc in the cave',
        'requirements': {'level': 5},
        'rewards': {'gold': 10, 'experience': 20},
        'completed': False
    }
]

# Define some utility functions for combat and leveling up
def attack(attacker, defender):
    damage = max(0, attacker['attack'] - defender['defense'])
    defender['health'] -= damage
    return damage

def level_up():
    character['level'] += 1
    character['max_health'] += 5
    character['health'] = character['max_health']
    character['attack'] += 1
    character['defense'] += 1

# Define the main routes for the RPG
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/character')
def character():
    return render_template('character.html', character=character)

@app.route('/inventory')
def view_inventory():
    return render_template('inventory.html', inventory=inventory)

@app.route('/quests')
def view_quests():
    return render_template('quests.html', quests=quests)

# Define routes for combat
@app.route('/combat')
def select_enemy():
    return render_template('select_enemy.html', enemies=enemies)

@app.route('/combat/<int:enemy_id>', methods=['GET', 'POST'])
def combat(enemy_id):
    # Find the selected enemy and get its stats
    enemy = enemies[enemy_id]
    
    if request.method == 'GET':
        # Display the combat screen
        return render_template('combat.html', enemy=enemy)
    else:
        # Handle the player's attack
        damage = attack(character, enemy)
        
        if enemy['health'] <= 0:
            # The enemy has been defeated
            character['gold'] += enemy['gold']
            character['experience'] += enemy['experience']
            return
        else:
            # Handle the enemy's counterattack
            damage = attack(enemy, character)
            
            if character['health'] <= 0:
                # The player has been defeated
                return render_template('game_over.html')
            else:
                # Return to the combat screen with updated stats
                return render_template('combat.html', enemy=enemy, damage=damage)
    
# Define routes for quests
@app.route('/quests/<int:quest_id>')
def view_quest(quest_id):
    quest = quests[quest_id]
    return render_template('view_quest.html', quest=quest)

@app.route('/quests/<int:quest_id>/complete')
def complete_quest(quest_id):
    quest = quests[quest_id]
    
    # Check if the player meets the requirements for the quest
    for requirement, value in quest['requirements'].items():
        if character[requirement] < value:
            # The player does not meet the requirement, so they cannot complete the quest
            return redirect('/quests')
    
    # Give the player the rewards for completing the quest
    for reward, value in quest['rewards'].items():
        character[reward] += value
    
    # Mark the quest as completed
    quest['completed'] = True
    
    return redirect('/quests')

# Define routes for leveling up
@app.route('/level_up')
def level_up_screen():
    return render_template('level_up.html')

@app.route('/level_up/<attribute>')
def increase_attribute(attribute):
    if attribute == 'health':
        character['max_health'] += 5
        character['health'] += 5
    else:
        character[attribute] += 1
    
    if character['experience'] >= 10 * character['level']:
        level_up()
    
    return redirect('/character')
