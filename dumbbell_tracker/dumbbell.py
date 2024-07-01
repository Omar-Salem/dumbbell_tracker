from datetime import datetime
from image_comparer import ImageComparer
from member_finder import MemberFinder
import cv2
import os

class Dumbbell:
    imageComparer = ImageComparer()
    memberFinder=MemberFinder()
    image_dir='resources/dumbbells'
    holder_images_dir=os.path.join(image_dir, 'empty')
    dumbbell_images_dir=os.path.join(image_dir, 'full')

    def __init__(   
            self,
            weight,
            x1,
            y1,
            x2,
            y2,
    ):
        self.weight = weight
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.holder_image = None
        self.dumbbell_image = None
        self.removed = False
        self.removed_on = None
        self.put_back_on = None
        self.member = None

    def set_holder_template(self,frame):
        cropped_image = self.__crop(frame)
        cv2.imwrite(self.get_holder_image_file_path(), cropped_image)
        self.holder_image = cv2.imread(self.get_holder_image_file_path())

    def set_dumbbell_image(self,frame):
        cropped_image = self.__crop(frame)
        cv2.imwrite(self.get_dumbbell_image_file_path(), cropped_image)
        self.dumbbell_image = cv2.imread(self.get_dumbbell_image_file_path())

    def get_holder_image_file_path(self):
        return '{}/{}Ks_{}.png'.format(self.holder_images_dir,self.weight, self.x1)
    
    def get_dumbbell_image_file_path(self):
        return '{}/{}Ks_{}.png'.format(self.dumbbell_images_dir,self.weight, self.x1)

    def check_put_back(self,frame):
        empty_holder_visible = self.__is_holder_visible(frame)
        return self.removed and self.__get_seconds_passed_since_remove()>1 and not empty_holder_visible  
    
    def check_removed(self,frame):
        moved = self.__has_dumbbell_moved(frame)
        return moved and not self.removed 

    def remove(self,frame):
        self.removed = True
        self.removed_on = datetime.now()
        self.member=self.memberFinder.identify_member(frame)
    
    def put_back(self,frame):
        self.removed = False
        self.removed_on = None
        self.member = None
        self.put_back_on = datetime.now()
        self.set_dumbbell_image(frame)
    
    def get_label(self):
       return '{} {}Kg {}'.format(self.member, self.weight, self.__get_seconds_passed_since_remove())

    def __get_seconds_passed_since_put_back(self):
        return round( (datetime.now() - self.put_back_on).total_seconds())
       
    def __get_seconds_passed_since_remove(self):
        return round( (datetime.now() - self.removed_on).total_seconds())
    
    def __crop(self, image):
        return image[self.y1:self.y2, self.x1:self.x2]

    def __has_dumbbell_moved(self,frame):
        search_area = self.__crop(frame)  # restrict search area
        score = self.imageComparer.calculate_images_similarity_score(self.dumbbell_image, search_area)
       
        return score<0.5
    
    def __is_holder_visible(self,frame):
        search_area = self.__crop(frame)  # restrict search area
        score =  self.imageComparer.calculate_images_similarity_score(self.holder_image, search_area)
        print(score)
        return score>0.5