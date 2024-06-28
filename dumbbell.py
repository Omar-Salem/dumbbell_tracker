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
        self.emptyTemplateImage = None
        self.removed = False
        self.removedOn = None
        self.holder = None

    def getCV2EmptyTemplateImage(self):
        return self.emptyTemplateImage

    def setCV2EmptyTemplateImage(self, cv2Image):
        self.emptyTemplateImage = cv2Image

    def getEmptyTemplateFilePath(self):
        return 'dumbbells/empty/{}Ks_{}.png'.format(self.weight, self.x1)