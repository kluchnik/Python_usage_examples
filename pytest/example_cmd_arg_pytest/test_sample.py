''' Example pytest scenario  '''

def test_answer_1(cmdopt):
	print('=> cmdopt = {}'.format(cmdopt))
	assert True

def test_answer_2(cmdopt):
	if cmdopt == 'type1':
		print('=> first')
	elif cmdopt == 'type2':
		print('=> second')
	else:
		print('=> other')
	assert True
