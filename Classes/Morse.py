import MorseCode as M

def to_morse(s):
	endstring = ''
	for c in s:
		endstring += M.MorseCode[c.upper()]
		endstring += ' '
	endstring += '.....'
	return endstring

def from_morse(s):
	endstring = ''
	morse = {y:x for x,y in M.MorseCode.items()}
	letters = s.split(' ')
	for letter in letters:
		if(letter in morse):
			endstring += morse[letter]
	return endstring

if __name__ == "__main__":
	m = to_morse('Hello')
	print(m)
	e = from_morse(m)
	print(e)