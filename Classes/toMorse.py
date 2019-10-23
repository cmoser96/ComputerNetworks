import MorseCode as M

def to_morse(s):
	endstring = ''
	for c in s:
		endstring += M.MorseCode[c.upper()]
		endstring += ' '
	endstring += '.....'
	return endstring

if __name__ == "__main__":
	print(to_morse('Hello'))