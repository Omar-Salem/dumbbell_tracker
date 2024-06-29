from datetime import datetime
from image_comparer import ImageComparer
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
        self.removed = False
        self.removed_on = None
        self.holder = None

    def get_cv2_empty_template_image(self):
        return self.empty_template_image

    def set_cv2_empty_template_image(self, cv2Image):
        self.empty_template_image = cv2Image

    def get_empty_template_file_path(self):
        return 'dumbbells/empty/{}Ks_{}.png'.format(self.weight, self.x1)
    
    def pick_up(self):
        self.removed = True
        self.removed_on = datetime.now()
    
    def put_back(self):
        self.removed = False
        self.removed_on = None
        self.holder = None

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
        empty_holder_template = self.get_cv2_empty_template_image()
        search_area = self.__crop(frame)  # restrict search area
        return self.imageComparer.check_images_similar(empty_holder_template, search_area)