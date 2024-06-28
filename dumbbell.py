class Dumbbell:
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
        self.removedOn = None
        self.holder = None

    def get_cv2_empty_template_image(self):
        return self.empty_template_image

    def set_cv2_empty_template_image(self, cv2Image):
        self.empty_template_image = cv2Image

    def get_empty_template_file_path(self):
        return 'dumbbells/empty/{}Ks_{}.png'.format(self.weight, self.x1)