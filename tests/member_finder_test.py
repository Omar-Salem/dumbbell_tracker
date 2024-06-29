import unittest
import cv2

from dumbbell_tracker.member_finder import MemberFinder


target=MemberFinder()

class TestCategorizeByAge(unittest.TestCase):
	def test_child(self):
		# Arrange
		frame=cv2.imread(str('picked_up.png'))
		
		# Act
		member=target.find_person_closest_to_point(frame,[226, 441])

		# Assert
		self.assertEqual("Omar Salem",member)

if __name__ == "__main__":
	unittest.main()