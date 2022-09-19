WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 768

LAYERS = {
	'FG': 12,
	'Entities': 11,
	'Ground': 10,
	'Canopy': 9,
	'Trees1': 8,
	'Lights1': 7,
	'Trees2': 6,
	'Trees3': 5,
	'Lights2': 4,
	'Trees4': 3,
	'BG1': 2,
	'BG2': 1,
	'BG3': 0
}

START_POS = {
	'Idle': (76, 52, 8, 38, 70),
	'Walk': (72, 52, 8, 47, 70),
	'Jump': (70, 52, 2, 38, 70),
	'Attack': (71, 52, 6, 119, 70),
	'Attack2': (70, 52, 6, 110, 57),
	'Death': (70, 52, 6, 109, 70),
	'Hit-Blink': (70, 52, 4, 109, 70),
	'Hit': (70, 52, 4, 109, 70),
	'Fall': (70, 52, 2, 48, 70)
}

ENEMY_POS = {
	'Idle': (81, 44, 4, 33, 84),
	'Run': (72, 52, 8, 47, 70),
	'Jump': (70, 52, 2, 38, 70),
	'Attack': (76, 44, 8, 96, 84),
	'Attack2': (70, 52, 6, 110, 57),
	'Death': (70, 52, 6, 109, 70),
	'Hit': (70, 52, 4, 109, 70),
	'Fall': (70, 52, 2, 48, 70)
}