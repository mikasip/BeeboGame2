QUESTS = {
    'quest1': {
        'id': 'quest1',
        'name': 'Help bartender',
        'dialog': 'I have no more ingredients for drinks. If you help me collect the ingredients, I will reward you!',
        'description': 'The Bubble Monsters have stolen all the grapes from the village. Help the bartender with his business and collect the grapes needed for drinks.',
        'done_dialog': 'Great! It looks like you have found enough grapes for me to start my business again! If you are willing to give the grapes, I will reward you!',
        'not_done_dialog': 'Please, get me the grapes as soon as possible!',
        'only_once': 'false',
        'mission': 
            {
                'type': 'collect',
                'text': 'Collect 10 grapes.',
                'item': ['Grape'],
                'file': ['grape'],
                'amount': [10],
            },
        'reward': {
            'gold': 200,
            'exp': 200,
            'items': []
        },
    },
    'quest-secret-room1': {
        'id': 'quest-secret-room1',
        'name': 'Help bartender',
        'dialog': 'I have no more ingredients for drinks. If you help me collect the ingredients, I will reward you!',
        'description': 'The Swamp Monsters have stolen all the grapes from the village. Help the bartender with his business and collect the grapes needed for drinks.',
        'done_dialog': 'Great! It looks like you have found enough grapes for me to start my business again! If you are willing to give the grapes, I will reward you!',
        'not_done_dialog': 'Please, get me the grapes as soon as possible!',
        'only_once': 'true',
        'mission': 
            {
                'type': 'collect',
                'text': 'Collect 10 grapes.',
                'item': ['Grape'],
                'file': ['grape'],
                'amount': [10],
            },
        'reward': {
            'gold': 200,
            'exp': 200,
            'items': []
        },
    },
    'quest-hall': {
        'id': 'quest-hall',
        'name': 'Earn the trust of Gulbur',
        'dialog': 'If you will earn my trust by showing how great warrior you are, I will reward you! Bring me ten daisies from Unfriendly Valley, be careful of the Horror Bubble Monsters!',
        'description': 'Bring ten daisies to Gulbur from Unfiendly Valley. The daisies are guarded by Horror Bubble Monsters.',
        'done_dialog': 'Ahh, it looks like you are a strong fighter. Here is key to secret underground maze, you will need it.',
        'not_done_dialog': 'Show me that you are the great warrior everyone claims you to be!',
        'only_once': 'true',
        'mission': 
            {
                'type': 'collect',
                'text': 'Collect 10 daisies.',
                'item': ['Daisy'],
                'file': ['daisy'],
                'amount': [10],
            },
        'reward': {
            'gold': 0,
            'exp': 0,
            'items': ['secret-room1-key']
        },
    },
    'farmer-quest': {
        'id': 'farmer-quest',
        'name': "Bring back the farmer's pigs" ,
        'dialog': 'Help! I have lost all of my pigs, they are running aroung the forest. Please bring them back to the yard.',
        'description': 'Bring 6 pigs back to farmers yard.',
        'done_dialog': 'Thank you so much! Please take these Scissors as reward.',
        'not_done_dialog': 'I am scared that I have lost my pigs forever!',
        'only_once': 'true',
        'mission': 
            {
                'type': 'bring',
                'text': 'Help farmer and bring his 6 pigs back to his yard.',
                'mob': 'pig',
                'amount': 6,
                'start_x': 860,
                'end_x': 1890,
                'start_y': 1280,
                'end_y': 1980,
            },
        'reward': {
            'gold': 200,
            'exp': 300,
            'items': ['scissors']
        },
    },
    'slime_quest': {
        'id': 'slime_quest',
        'name': "Collect slime from Slime Monsters" ,
        'dialog': "I am so facinated about the Slime Monsters' slime! I want to study the slime more deeply, but the Slime Monsters are too strong for me. Will you help me to collect it?",
        'description': 'Collect slime from Slime Monsters',
        'done_dialog': 'Yes! I knew I could trust you! I will reward you greatly!',
        'not_done_dialog': 'Slime, slime, slime...',
        'only_once': 'true',
        'mission': 
            {
                'type': 'collect',
                'text': 'Collect 20 Red Slime, 20 Blue Slime, 20 Yellow Slime and 10 Dotted Slime.',
                'item': ['Red Slime', 'Blue Slime', 'Yellow Slime', 'Dotted Slime'],
                'file': ['red_slime', 'blue_slime', 'yellow_slime', 'dotted_slime'],
                'amount': [20, 20, 20, 10],
            },
        'reward': {
            'items': [],
            'gold': 500,
            'exp': 1000,
        },
    },
    'spider_quest': {
        'id': 'spider_quest',
        'name': "Collect Green Spider Legs from the Green Spiders" ,
        'dialog': "I have a secret receipt for Potions of Fortune... I am only missing some Green Spider Legs to prepare those. Bring me 30 Green Spider Legs and I can start my business!",
        'description': 'Help the beebo in the Secret maze to start his business as a potion seller. Bring him 30 Green Spider Legs.',
        'done_dialog': 'Ahh, finally I can start my business!',
        'not_done_dialog': 'Green Spider Legs are the only ingredient missing from my potion cocktail.',
        'only_once': 'true',
        'mission': 
            {
                'type': 'collect',
                'text': 'Collect 30 Green Spider Legs',
                'item': ['Green Spider Leg'],
                'file': ['green_spider_leg'],
                'amount': [30],
            },
        'reward': {
            'items': [],
            'gold': 700,
            'exp': 700,
        },
    }
}