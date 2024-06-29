from member_finder import MemberFinder
import pathlib
import cv2
memberFinder=MemberFinder()

frame = cv2.imread(str('result.png'))
holder=memberFinder.find_person_closest_to_point(frame,[226, 441])
if holder is not None:
	print('FOUND {}'.format(holder))
# for d in pathlib.Path('./frames').glob('*.png'):
# 	print(d)
# 	frame = cv2.imread(str(d))
# 	holder=memberFinder.findPersonClosestToPoint(frame,[202,426])
# 	if holder is not None:
# 		print('FOUND AT FRAME {} {}'.format(d,holder))
# 		break