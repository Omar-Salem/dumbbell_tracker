from datetime import datetime
from image_comparer import ImageComparer
import cv2

class Dumbbell:
    imageComparer = ImageComparer()
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
        self.empty_template_image = None
        self.full_template_image = None
        self.removed = False
        self.removed_on = None
        self.holder = None

    def set_empty_template(self,frame):
        cropped_image = self.__crop(frame)
        cv2.imwrite(self.get_empty_template_file_path(), cropped_image)
        self.empty_template_image = cv2.imread(self.get_empty_template_file_path())

    def set_full_template(self,frame):
        cropped_image = self.__crop(frame)
        cv2.imwrite(self.get_full_template_file_path(), cropped_image)
        self.full_template_image = cv2.imread(self.get_full_template_file_path())

    def get_empty_template_file_path(self):
        return '../resources/dumbbells/empty/{}Ks_{}.png'.format(self.weight, self.x1)
    
    def get_full_template_file_path(self):
        return '../resources/dumbbells/full/{}Ks_{}.png'.format(self.weight, self.x1)

    def pick_up(self):
        self.removed = True
        self.removed_on = datetime.now()
        self.full_template_image = None
    
    def put_back(self,frame):
        self.removed = False
        self.removed_on = None
        self.holder = None
        self.set_full_template(frame)

    def check_put_back(self,frame):
        empty_holder_visible = self.__is_place_holder_visible(frame)
        return self.removed and self.__get_seconds_passed_since_remove()>1 and not empty_holder_visible  
    
    def check_picked_up(self,frame):
        empty_holder_visible = self.__is_place_holder_visible(frame)
        return  empty_holder_visible and not self.removed
    
    def get_label(self):
       return '{} {}Kg {}'.format(self.holder, self.weight, self.__get_seconds_passed_since_remove())
    
    def __get_seconds_passed_since_remove(self):
        return round( (datetime.now() - self.removed_on).total_seconds())
    
    def __crop(self, image):
        return image[self.y1:self.y2, self.x1:self.x2]

    def __is_place_holder_visible(self,frame):
        empty_holder_template = self.empty_template_image
        search_area = self.__crop(frame)  # restrict search area
        return self.imageComparer.check_images_similar(empty_holder_template, search_area)