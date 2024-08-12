import random

def random_pick(liste:list[str]) -> str:
	return (liste[random.randint(0, len(liste)-1)])