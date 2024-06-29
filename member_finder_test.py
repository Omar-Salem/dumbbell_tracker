from member_finder import MemberFinder
import pathlib
import cv2
memberFinder=MemberFinder()

frame = cv2.imread(str('picked_up.png'))
holder=memberFinder.find_person_closest_to_point(frame,[226, 441])
if holder is None:
	raise('holder null')
if holder !='Omar':
	raise(holder)