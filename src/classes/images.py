from enum import Enum
from pygame import image, Surface, Rect, transform, SRCALPHA

class Images(Enum):
    TrashCan = "assets/imgs/trash_can.png"
    Letter = "assets/imgs/letter.png"
    SubmitButton = "assets/imgs/submit_button.png"
    PauseButton = "assets/imgs/pause_button.png"
    Background1 = "assets/imgs/background_1.png"
    Background2 = "assets/imgs/background_2.png"
    Tutorial1 = "assets/imgs/tutorial_1.png"
    Tutorial2 = "assets/imgs/tutorial_2.png"
    ConveyorHead = "assets/imgs/conveyor_head.png"
    ConveyorJunction = "assets/imgs/conveyor_junction.png"
    QuestionBox = "assets/imgs/question_box.png"
    SubmitTable = "assets/imgs/submit_table.png"
    ScoreDisplay = "assets/imgs/score_display.png"
    Player = "assets/imgs/player.png"

class ImageLoader:
    _images: dict[Images, Surface] = {}
    
    @classmethod
    def load_images(cls):
        for img in Images:
            cls._images[img] = image.load(img.value).convert_alpha()
    
    @classmethod
    def get_frames(cls, name: Images,
                   segment_width: int,
                   new_width: int,
                   new_height: int,
                   indices: list[int] = []) -> list[Surface]:
        """
        Fetchs frames in spritesheet image,
        transform the fetched image to size: (width, height)
        All frames will be extracted if indices = []
        """
        assert name in cls._images.keys()
        img = cls._images[name]
        img_w, img_h = img.get_size()

        assert img_w / segment_width == img_w // segment_width

        frames = []
        for i in range(int(img_w / segment_width)):
            if len(indices) != 0 and not i in indices:
                continue

            frame = Surface((segment_width, img_h), SRCALPHA)
            frame.blit(img, (0, 0), Rect(i*segment_width, 0, segment_width, img_h))
            frame = transform.scale(frame, (new_width, new_height)).convert_alpha()

            frames.append(frame.convert_alpha())
        return frames

    @classmethod
    def get(cls, name: Images, w: int=-1, h: int=-1, scale: float=-1) -> Surface:
        """
        Fetchs Image corresponding to Images enum.
        Transforms the image to size (w, h) if both w and h are provided
        Scales the image by the factor "scale" if scale is provided
        (w and h are considered first)
        """
        assert name in cls._images.keys()
        img = cls._images[name]

        if w != -1 and h != -1:
            return transform.scale(img, (w, h))
        
        if scale != -1:
            return transform.scale_by(img, scale)

        return img