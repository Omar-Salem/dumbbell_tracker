from memberFinder import MemberFinder
import pathlib
import cv2
memberFinder=MemberFinder()

for d in pathlib.Path('./frames').glob('*.png'):
	print(d)
	frame = cv2.imread(str(d))
	holder=memberFinder.findPersonClosestToPoint(frame,[202,426])
	if holder is not None:
		print('FOUND AT FRAME {} {}'.format(d,holder))
		break