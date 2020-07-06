# 995 recursion depth
num = 0
def test(num):
	print(num)
	num+=1
	test(num)
test(num)
