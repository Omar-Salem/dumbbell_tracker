import unittest
import cv2

from dumbbell_tracker.member_finder import MemberFinder


target=MemberFinder()

class MemberFinderTest(unittest.TestCase):
	def member_identified(self):
		# Arrange
		frame=cv2.imread(str('picked_up.png'))
		
		# Act
		member=target.identify_member(frame)

		# Assert
		self.assertEqual("Omar Salem",member)

if __name__ == "__main__":
	unittest.main()